from pijemont.exceptions import PijemontKeyError, PijemontTypeError, PijemontInvalidType
from pijemont.formatter import check_format


def test_missing_type():
    errors = check_format({"values": {}}, False, False)
    assert len(errors) == 1
    assert str(PijemontKeyError("values", "type")) in errors


def test_missing_values():
    errors = check_format({"foo": {"type": "dict"}}, False, False)
    assert len(errors) == 1
    assert str(PijemontKeyError("foo", "values")) in errors


def test_invalid_values_dict():
    errors = check_format({"foo": {"type": "dict", "values": None}}, False, False)
    assert len(errors) == 1
    assert str(PijemontTypeError("foo.values", None, dict)) in errors


def test_invalid_type():
    errors = check_format({"foo": {"type": "bar"}}, False, False)
    assert len(errors) == 1
    assert str(PijemontInvalidType("foo", "bar"))


def test_container_types():
    for typ in ["dict", "oneof", "tuple"]:
        # missing type
        errors = check_format({"foo": {"type": typ, "values": {"bar": {}}}}, False, False)
        assert len(errors) == 1
        assert str(PijemontKeyError("foo.bar", "type")) in errors
        # missing values
        errors = check_format({"foo": {"type": typ, "values": {"bar": {"type": "dict"}}}}, False, False)
        assert len(errors) == 1
        assert str(PijemontKeyError("foo.bar", "values")) in errors
        # invalid values dict
        errors = check_format({"foo": {"type": typ, "values": {"bar": {"type": "dict", "values": None}}}}, False, False)
        assert len(errors) == 1
        assert str(PijemontTypeError("foo.bar.values", None, dict)) in errors
        # invalid type
        errors = check_format({"foo": {"type": typ, "values": {"bar": {"type": "baz"}}}}, False, False)
        assert len(errors) == 1
        assert str(PijemontInvalidType("foo.bar", "baz")) in errors


def test_list():
        # missing type
        errors = check_format({"foo": {"type": "list", "values": {}}}, False, False)
        assert len(errors) == 1
        assert str(PijemontKeyError("foo.values", "type")) in errors
        # invalid type
        errors = check_format({"foo": {"type": "list", "values": {"type": "foo"}}}, False, False)
        assert len(errors) == 1
        assert str(PijemontInvalidType("foo.values", "foo")) in errors


# TODO test "args" and "rets" ?

