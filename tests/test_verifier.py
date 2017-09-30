from verifier3 import check_format, FormatHelper, verify, VerifyHelper, PijemontKeyError, PijemontTypeError, PijemontArgError
from utils import compare_dict_keys
import pytest


# TODO test_formatter section
def test_missing_type():
    errors = check_format({"values": []})
    assert len(errors) == 1
    assert str(PijemontKeyError("input_dict", "type")) in errors


def test_missing_values():
    errors = check_format({"type": "dict"})
    assert len(errors) == 1
    assert str(PijemontKeyError("input_dict", "values")) in errors


def test_invalid_values_dict():
    errors = check_format({"type": "dict", "values": None})
    assert len(errors) == 1
    assert str(PijemontTypeError("values", None, dict)) in errors


# TODO test_verifier section
def test_invalid_input_dict():
    errors = verify(None, {"foo": {"type": "string"}})
    assert len(errors) == 1
    assert str(PijemontTypeError("input_dict", None, dict)) in errors


def test_extra_args():
    errors = verify({"foo": "bar", "baz": "buzz"}, {"foo": {"type": "string"}})
    assert len(errors) == 1
    assert str(PijemontArgError("input_dict", "baz", "foo")) in errors


# TODO test_utils section
def test_compare_dict_keys():
    k1, k2 = compare_dict_keys({}, {"hello": "world"})
    assert len(k1) == 0
    assert k2 == ["hello"]
    k1, k2 = compare_dict_keys({"hello": "world"}, {"hello": "world"})
    assert len(k1) == len(k2) == 0
    k1, k2 = compare_dict_keys({"foo": "bar"}, {"hello": "world"})
    assert k1 == ["foo"]
    assert k2 == ["hello"]



