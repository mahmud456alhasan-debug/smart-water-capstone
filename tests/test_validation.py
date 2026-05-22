from src.validation import validate_runoff_mm, validate_storage_mcm


def test_validate_runoff_fail_case():
    out = validate_runoff_mm(10.0, 15.0)
    assert not out["ok"]


def test_validate_storage_fail():
    out = validate_storage_mcm(10.0)
    assert not out["ok"]
