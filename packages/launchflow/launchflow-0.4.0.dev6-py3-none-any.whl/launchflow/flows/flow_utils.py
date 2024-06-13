import deepdiff


def compare_dicts(d1, d2):
    diff = deepdiff.DeepDiff(d1, d2, ignore_order=True)
    diff_keys = diff.affected_root_keys
    diff_strs = []
    for key in diff_keys:
        old_value = d1.get(key)
        new_value = d2.get(key)
        diff_strs.append(f"[cyan]{key}[/cyan]: {old_value} -> {new_value}")
    if diff_strs:
        return "    " + "\n    ".join(diff_strs)
    return ""
