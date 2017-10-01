from pijemont.exceptions import PijemontKeyError, PijemontTypeError, PijemontArgError, PijemontCastError
from pijemont.formatter import check_format
from pijemont.verifier import verify


def test_invalid_input_dict():
    ref = {"foo": {"type": "string"}}
    check_format(ref, False)
    errors = verify(None, ref, False)
    assert len(errors) == 1
    assert str(PijemontTypeError("input", None, dict)) in errors


def test_extra_args():
    ref = {"foo": {"type": "string"}}
    check_format(ref, False)
    errors = verify({"foo": "bar", "baz": "buzz"}, ref, False)
    assert len(errors) == 1
    assert str(PijemontArgError("input", "baz", "foo")) in errors


def test_optional():
    # no default set, missing arg
    ref = {"foo": {"type": "int"}}
    check_format(ref, False)
    errors = verify({}, ref, False)
    assert len(errors) == 1
    assert str(PijemontKeyError("input", "foo")) in errors
    # no defaults, optional
    ref = {"foo": {"type": "int", "optional": True}}
    check_format(ref, False)
    result = verify({}, ref)
    assert result == {}


def test_defaults():
    # default int
    ref = {"foo": {"type": "int", "default": 1}}
    check_format(ref, False)
    result = verify({}, ref)
    assert result == {"foo": 1}
    assert isinstance(result["foo"], int)
    # default float
    ref = {"foo": {"type": "float", "default": 1.5}}
    check_format(ref, False)
    result = verify({}, ref)
    assert result == {"foo": 1.5}
    assert isinstance(result["foo"], float)
    # default string
    ref = {"foo": {"type": "string", "default": "bar"}}
    check_format(ref, False)
    result = verify({}, ref)
    assert result == {"foo": "bar"}
    assert isinstance(result["foo"], str)


def test_list():
    ref = {"foo": {"type": "list", "values": {"type": "int"}}}
    check_format(ref)
    result = verify({"foo": []}, ref)
    assert result == {"foo": []}
    result = verify({"foo": [4, 5, 6]}, ref)
    assert result == {"foo": [4, 5, 6]}
    errors = verify({"foo": [4, 5, "a"]}, ref, False)
    assert len(errors) == 1
    try:
        int("a")
    except Exception as e:
        assert str(PijemontCastError("foo.2", "int", e)) in errors

