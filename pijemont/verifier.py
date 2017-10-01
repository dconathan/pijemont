from pijemont.base import PijemontHelper
from pijemont.exceptions import PijemontKeyError, PijemontTypeError, PijemontInvalidType, PijemontArgError, \
    PijemontCastError, PijemontOneOfError, PijemontException
from pijemont.types import DICT, LIST, TUPLE, ONEOF, NUM, INT, STRING, ANY, FILE, BOOL, CAST_TYPES
from pijemont.utils import compare_dict_keys


class VerifyHelper(PijemontHelper):
    def _default(self, input_element, name, key, reference_dict):
        if "default" in reference_dict:
            input_element[key] = reference_dict["default"]
        elif not reference_dict.get("optional", False):
            self.handle_error(PijemontKeyError(name, key))
        return input_element

    def _verify(self, name, input_element, reference_dict):
        if reference_dict["type"] in DICT:
            if not isinstance(input_element, dict):
                self.handle_error(PijemontTypeError(name, input_element, dict))
            else:
                input_keys, ref_keys = compare_dict_keys(input_element, reference_dict["values"])
                if input_keys:
                    self.handle_error(PijemontArgError(name, input_keys, reference_dict["values"].keys()))
                else:
                    for k in ref_keys:
                        input_element = self._default(input_element, name, k, reference_dict["values"][k])
                    for k, v in input_element.items():
                        input_element[k] = self._verify("{}.{}".format(name, k), v, reference_dict["values"][k])

        elif reference_dict["type"] in LIST:
            if not isinstance(input_element, list):
                self.handle_error(PijemontTypeError(name, input_element, list))
            else:
                for i, x in enumerate(input_element):
                    input_element[i] = self._verify("{}.{}".format(name, i), input_element[i], reference_dict["values"])

        elif reference_dict["type"] in TUPLE:
            if not isinstance(input_element, (list, tuple)):
                self.handle_error(PijemontTypeError(name, input_element, [list, tuple]))
            else:
                temp = list(input_element)
                for i, x in enumerate(input_element):
                    temp[i] = self._verify("{}.{}".format(name, i), input_element[i], reference_dict["values"])
                input_element = tuple(temp)

        elif reference_dict["type"] in BOOL:
            if not isinstance(input_element, bool):
                self.handle_error(PijemontTypeError(name, input_element, bool))

        elif reference_dict["type"] in CAST_TYPES:
            input_element = self._cast(name, input_element, reference_dict["type"])

        elif reference_dict["type"] in ONEOF:
            count = 0
            for k in reference_dict["values"]:
                if k in input_element:
                    count += 1
                if count == 0:
                    input_element = self._default(input_element, name, k, reference_dict["values"][k])
                elif count > 1:
                    self.handle_error(PijemontOneOfError(name))

        elif reference_dict["type"] in ANY | FILE:
            pass

        else:
            self.handle_error(PijemontInvalidType(name, reference_dict["type"]))

        return input_element

    def _cast(self, name, obj, typ):
        try:
            if typ in NUM:
                obj = float(obj)
            elif typ in INT:
                obj = int(obj)
            elif typ in STRING:
                obj = str(obj)
        except Exception as e:
            self.handle_error(PijemontCastError(name, typ, e))
        finally:
            return obj


def verify(input_dict, reference_dict, raise_on_error=True):
    reference_dict = {"type": "dict", "values": reference_dict}
    verify_helper = VerifyHelper()
    result = verify_helper._verify("input", input_dict, reference_dict)
    if verify_helper.errors:
        if raise_on_error:
            if len(verify_helper.errors) == 1:
                message = "There was 1 error while verifying the input_dict: "
            else:
                message = "There were {} errors while verifying the input_dict:\n  - ".format(len(verify_helper.errors))
            message += "\n  - ".join(verify_helper.errors)
            raise PijemontException(message)
        else:
            return verify_helper.errors
    else:
        return result
