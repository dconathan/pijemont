from pijemont.utils import compare_dict_keys


def test_compare_dict_keys():
    k1, k2 = compare_dict_keys({}, {"hello": "world"})
    assert len(k1) == 0
    assert k2 == ["hello"]
    k1, k2 = compare_dict_keys({"hello": "world"}, {"hello": "world"})
    assert len(k1) == len(k2) == 0
    k1, k2 = compare_dict_keys({"foo": "bar"}, {"hello": "world"})
    assert k1 == ["foo"]
    assert k2 == ["hello"]