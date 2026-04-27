"""Deterministic policy gate for docker-compose stacks.

Run:
    python -m validators.compose_policy sandbox/docker-compose.yml

Returns exit 0 if all policies pass, exit 1 with a diff-like report if any fail.

Each policy is a pure function: (compose_dict) -> list[Violation]. Add your own
by appending to POLICIES below. Tests in tests/test_compose_policy.py exercise
each policy in isolation.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import yaml


@dataclass
class Violation:
    policy_id: str
    service: str | None
    detail: str


# ---------------------------------------------------------------------------
# Policies (pure functions over the compose dict)
# ---------------------------------------------------------------------------

def p_no_public_port_bind(compose: dict) -> list[Violation]:
    """Every published port must bind to 127.0.0.1 explicitly."""
    out: list[Violation] = []
    for name, svc in (compose.get("services") or {}).items():
        for entry in svc.get("ports") or []:
            if isinstance(entry, str):
                # Acceptable forms:
                #   "127.0.0.1:8080:80"
                # Rejected:
                #   "8080:80", "0.0.0.0:8080:80", "::8080:80"
                parts = entry.split(":")
                if len(parts) < 3 or parts[0] not in ("127.0.0.1",):
                    out.append(Violation("P001", name, f"port mapping {entry!r} must bind to 127.0.0.1"))
            elif isinstance(entry, dict):
                host_ip = entry.get("host_ip")
                if host_ip != "127.0.0.1":
                    out.append(Violation("P001", name, f"port mapping {entry!r} must set host_ip: 127.0.0.1"))
    return out


def p_no_privileged(compose: dict) -> list[Violation]:
    """No privileged containers."""
    out: list[Violation] = []
    for name, svc in (compose.get("services") or {}).items():
        if svc.get("privileged"):
            out.append(Violation("P002", name, "privileged: true is not allowed"))
    return out


def p_no_host_network(compose: dict) -> list[Violation]:
    """No host network mode."""
    out: list[Violation] = []
    for name, svc in (compose.get("services") or {}).items():
        net = svc.get("network_mode")
        if net == "host":
            out.append(Violation("P003", name, "network_mode: host is not allowed"))
    return out


def p_no_host_path_mounts(compose: dict) -> list[Violation]:
    """Bind mounts of host paths are not allowed (named volumes are fine)."""
    out: list[Violation] = []
    for name, svc in (compose.get("services") or {}).items():
        for v in svc.get("volumes") or []:
            if isinstance(v, str):
                src = v.split(":")[0]
                if src.startswith("/") or src.startswith("."):
                    out.append(Violation("P004", name, f"host path mount {v!r} is not allowed"))
            elif isinstance(v, dict):
                if v.get("type") == "bind":
                    out.append(Violation("P004", name, f"bind mount {v!r} is not allowed"))
    return out


def p_no_hardcoded_secrets(compose: dict) -> list[Violation]:
    """Naive check for environment values that look like credentials."""
    out: list[Violation] = []
    suspect_keys = ("PASSWORD", "SECRET", "TOKEN", "API_KEY", "PRIVATE_KEY")
    for name, svc in (compose.get("services") or {}).items():
        env = svc.get("environment") or {}
        if isinstance(env, list):
            env = dict(item.split("=", 1) for item in env if "=" in item)
        for k, v in env.items():
            if any(s in k.upper() for s in suspect_keys):
                if v and not (isinstance(v, str) and v.startswith("$")):
                    out.append(Violation("P005", name, f"env {k!r} appears hardcoded; use ${{VAR}} reference"))
    return out


POLICIES: list[Callable[[dict], list[Violation]]] = [
    p_no_public_port_bind,
    p_no_privileged,
    p_no_host_network,
    p_no_host_path_mounts,
    p_no_hardcoded_secrets,
]


def validate(compose: dict) -> list[Violation]:
    out: list[Violation] = []
    for fn in POLICIES:
        out.extend(fn(compose))
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python -m validators.compose_policy <compose.yml>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    compose = yaml.safe_load(path.read_text())
    violations = validate(compose)
    if not violations:
        print(f"[OK] {path}: all policies pass")
        return 0
    print(f"[FAIL] {path}: {len(violations)} violation(s)")
    for v in violations:
        svc = f" [{v.service}]" if v.service else ""
        print(f"  - {v.policy_id}{svc}: {v.detail}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
