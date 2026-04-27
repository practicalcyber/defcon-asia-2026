"""Tests for the lure schema egress filter.

PROVIDED — extend, do not delete.
"""
import pytest
from pydantic import ValidationError

from validators.lure_schema import LureBatch, LureVariant


GOOD = {
    "subject": "Action required: Q2 work pass compliance review",
    "sender_persona": "IT Compliance Unit, fictional ministry of work passes",
    "body": "Dear IT Manager,\n\nOur fictional ministry has flagged your account for a "
            "routine compliance review. Please verify your administrator credentials "
            "before the deadline. Failure to comply may result in suspension of work pass "
            "issuance privileges. Thank you for your prompt attention.",
    "cta_label": "Verify credentials",
    "plausibility_flags": ["fake urgency", "impersonation of authority"],
    "target_role": "IT Manager at SG mid-sized company",
    "is_fictional_target": True,
}


def test_good_lure_validates():
    LureVariant.model_validate(GOOD)


def test_inline_url_rejected():
    bad = {**GOOD, "body": GOOD["body"] + "\n\nClick: https://verify.example.com/x"}
    with pytest.raises(ValidationError):
        LureVariant.model_validate(bad)


def test_real_org_name_rejected():
    bad = {**GOOD, "body": GOOD["body"].replace("ministry", "DBS Bank ministry")}
    with pytest.raises(ValidationError):
        LureVariant.model_validate(bad)


def test_is_fictional_target_must_be_true():
    bad = {**GOOD, "is_fictional_target": False}
    with pytest.raises(ValidationError):
        LureVariant.model_validate(bad)


def test_empty_plausibility_flags_rejected():
    bad = {**GOOD, "plausibility_flags": []}
    with pytest.raises(ValidationError):
        LureVariant.model_validate(bad)


def test_batch_distinct_subjects():
    v1 = LureVariant.model_validate(GOOD)
    v2 = LureVariant.model_validate(GOOD)  # duplicate subject
    with pytest.raises(ValidationError):
        LureBatch(variants=[v1, v2])


def test_batch_accepts_distinct_subjects():
    v1 = LureVariant.model_validate(GOOD)
    v2 = LureVariant.model_validate({**GOOD, "subject": "Reminder: complete your annual training module"})
    LureBatch(variants=[v1, v2])  # no exception
