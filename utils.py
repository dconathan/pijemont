import os
import yaml


def load_doc(filename,base_path):
    errs = []
    with open(os.path.join(base_path,filename)) as f:
        ref = yaml.load(f.read())
        ds = []
        for ext in ref.pop('extends',[]):
            r,e = load_doc(ext,base_path)
            ds += [r]
            errs += e
        for d in ds:
            ref = merge_dict(ref, d)
    errs = check_format(ref,'args' in ref[list(ref.keys())[0]])
    return ref,errs


def merge_dict(d1,d2,prefer=1):
    for k in d2:
        if k in d1:
            if type(d1[k]) == dict:
                d1[k] = merge_dict(d1[k],d2[k])
            if prefer == 2:
                d1[k] = d2[k]
        else:
            d1[k] = d2[k]
    return d1


def compare_dict_keys(d1, d2):
    """
    returns:

        [things in d1 not in d2], [things in d2 not in d1]
    """
    return [k for k in d1 if k not in d2], [k for k in d2 if k not in d1]
