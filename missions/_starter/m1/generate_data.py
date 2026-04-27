"""Generate synthetic CloudTrail events for the starter dataset.

Run once:
    python generate_data.py > data/cloudtrail-sample.jsonl

The generated file contains:
    - ~190 routine events (S3 reads, KMS decrypts, EC2 describes from CI principal)
    - 1  ConsoleLogin from alice@acme.example in ap-northeast-1 (impossible region)
    - 8  ListBuckets / GetBucketAcl from bob@acme.example within 12 seconds (mass enum)
    - 1  CreateAccessKey by root (critical, single occurrence)

If you want different anomaly counts, edit and re-run. Tests assume defaults.
"""
from __future__ import annotations

import json
import random
import sys
from datetime import datetime, timedelta, timezone

random.seed(42)

START = datetime(2026, 4, 27, 8, 0, 0, tzinfo=timezone.utc)


def event(ts: datetime, name: str, user: str, user_type: str = "IAMUser",
          region: str = "ap-southeast-1", source_ip: str = "10.0.0.42",
          extra: dict | None = None) -> dict:
    ev = {
        "eventTime": ts.isoformat(),
        "eventName": name,
        "eventSource": f"{name.lower().split('list')[-1].split('get')[-1] or 'aws'}.amazonaws.com",
        "awsRegion": region,
        "sourceIPAddress": source_ip,
        "userIdentity": {"type": user_type, "userName": user},
    }
    if extra:
        ev.update(extra)
    return ev


def routine(ts_offset_s: int) -> dict:
    """Boring CI/CD-style activity."""
    actions = [
        ("GetObject",        "ci-deployer", "10.0.0.42"),
        ("ListBucket",       "ci-deployer", "10.0.0.42"),
        ("DescribeInstances","ci-deployer", "10.0.0.42"),
        ("Decrypt",          "ci-deployer", "10.0.0.42"),
        ("AssumeRole",       "ci-deployer", "10.0.0.42"),
        ("GetObject",        "alice@acme.example", "10.0.1.10"),
        ("DescribeInstances","alice@acme.example", "10.0.1.10"),
        ("Decrypt",          "bob@acme.example",   "10.0.1.20"),
        ("GetObject",        "bob@acme.example",   "10.0.1.20"),
        ("DescribeVolumes",  "bob@acme.example",   "10.0.1.20"),
    ]
    name, user, ip = random.choice(actions)
    return event(START + timedelta(seconds=ts_offset_s), name, user, source_ip=ip)


def write_all(out=sys.stdout):
    events: list[dict] = []

    # 190 routine events spread over ~3 hours
    for i in range(190):
        events.append(routine(ts_offset_s=random.randint(0, 3 * 3600)))

    # Anomaly 1 — alice ConsoleLogin from ap-northeast-1 (her known region is ap-southeast-1)
    events.append(event(
        START + timedelta(seconds=4200),
        "ConsoleLogin",
        "alice@acme.example",
        region="ap-northeast-1",
        source_ip="203.0.113.99",
    ))

    # Anomaly 2 — bob mass S3 enumeration: 8 calls in 12s
    base = START + timedelta(seconds=6000)
    enum_actions = ["ListBuckets", "GetBucketAcl", "GetBucketPolicy",
                    "ListBuckets", "GetBucketAcl", "GetBucketLocation",
                    "ListBuckets", "GetBucketAcl"]
    for i, name in enumerate(enum_actions):
        events.append(event(
            base + timedelta(seconds=i * 1.5),
            name, "bob@acme.example",
            source_ip="198.51.100.7",
        ))

    # Anomaly 3 — root creates access key (single critical event)
    events.append(event(
        START + timedelta(seconds=8800),
        "CreateAccessKey",
        "root",
        user_type="Root",
        source_ip="203.0.113.7",
    ))

    # Sort by timestamp so the file looks realistic
    events.sort(key=lambda e: e["eventTime"])

    for e in events:
        out.write(json.dumps(e) + "\n")


if __name__ == "__main__":
    write_all()
