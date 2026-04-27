"""Tests for the deterministic compose-policy gate.

These tests are PROVIDED so participants can see the validator working end-to-end.
You are encouraged to extend them — but do NOT delete the existing ones; they are
the contract for the policy engine.
"""
from pathlib import Path

import yaml

from validators.compose_policy import (
    p_no_host_network,
    p_no_host_path_mounts,
    p_no_privileged,
    p_no_public_port_bind,
    p_no_hardcoded_secrets,
    validate,
)

HERE = Path(__file__).parent.parent
SAFE_COMPOSE = HERE / "sandbox" / "docker-compose.yml"


def load(text: str) -> dict:
    return yaml.safe_load(text)


def test_safe_compose_passes():
    """The shipped sandbox/docker-compose.yml must pass all policies."""
    compose = yaml.safe_load(SAFE_COMPOSE.read_text())
    assert validate(compose) == []


def test_p001_catches_default_port_bind():
    compose = load("""
services:
  app:
    image: nginx
    ports:
      - "8080:80"
""")
    violations = p_no_public_port_bind(compose)
    assert len(violations) == 1
    assert violations[0].policy_id == "P001"


def test_p001_accepts_explicit_loopback():
    compose = load("""
services:
  app:
    image: nginx
    ports:
      - "127.0.0.1:8080:80"
""")
    assert p_no_public_port_bind(compose) == []


def test_p002_catches_privileged():
    compose = load("""
services:
  app:
    image: nginx
    privileged: true
""")
    violations = p_no_privileged(compose)
    assert len(violations) == 1
    assert violations[0].policy_id == "P002"


def test_p003_catches_host_network():
    compose = load("""
services:
  app:
    image: nginx
    network_mode: host
""")
    violations = p_no_host_network(compose)
    assert len(violations) == 1
    assert violations[0].policy_id == "P003"


def test_p004_catches_host_path_mount():
    compose = load("""
services:
  app:
    image: nginx
    volumes:
      - /etc:/host_etc:ro
""")
    violations = p_no_host_path_mounts(compose)
    assert len(violations) == 1
    assert violations[0].policy_id == "P004"


def test_p005_catches_hardcoded_secret():
    compose = load("""
services:
  app:
    image: nginx
    environment:
      DB_PASSWORD: hunter2
""")
    violations = p_no_hardcoded_secrets(compose)
    assert len(violations) == 1
    assert violations[0].policy_id == "P005"


def test_p005_accepts_var_reference():
    compose = load("""
services:
  app:
    image: nginx
    environment:
      DB_PASSWORD: ${DB_PASSWORD}
""")
    assert p_no_hardcoded_secrets(compose) == []
