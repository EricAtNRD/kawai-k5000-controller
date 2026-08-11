#!/usr/bin/env python3
"""Compare the Live parameter surface of two .amxd devices.

Saved Live Sets bind to parameter_longname and the parameter's type/range, so
any change to those is a breaking release. This reports what actually differs.

Usage:  param-surface-diff.py OLD.amxd NEW.amxd
"""

import json
import sys

# Changing any of these invalidates existing Set bindings.
BREAKING = {
    "parameter_longname",
    "parameter_shortname",
    "parameter_type",
    "parameter_mmin",
    "parameter_mmax",
    "parameter_range",
    "parameter_enum",
    "parameter_mapping_index",
}


def parameters(path):
    """Map parameter_longname -> (maxclass, parameter dict) for one device."""
    raw = open(path, "rb").read()
    patcher, _ = json.JSONDecoder().raw_decode(raw[32:].decode("utf-8", "replace"))
    found = {}

    def walk(p):
        for b in p.get("boxes", []):
            box = b["box"]
            valueof = box.get("saved_attribute_attributes", {}).get("valueof")
            if valueof:
                found[valueof.get("parameter_longname")] = (
                    box.get("maxclass"),
                    dict(valueof),
                )
            if "patcher" in box:
                walk(box["patcher"])

    walk(patcher["patcher"])
    return found


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    old_path, new_path = sys.argv[1], sys.argv[2]
    old, new = parameters(old_path), parameters(new_path)

    print(f"old: {old_path}  ({len(old)} parameters)")
    print(f"new: {new_path}  ({len(new)} parameters)")

    added, removed = sorted(set(new) - set(old)), sorted(set(old) - set(new))
    for name in removed:
        print(f"  REMOVED  {name}   *** breaking ***")
    for name in added:
        print(f"  ADDED    {name}")

    changed = breaking = 0
    for name in sorted(set(old) & set(new)):
        before, after = old[name][1], new[name][1]
        keys = set(before) | set(after)
        delta = {
            k: (before.get(k, "<absent>"), after.get(k, "<absent>"))
            for k in keys
            if before.get(k) != after.get(k)
        }
        if not delta:
            continue
        changed += 1
        hits = sorted(BREAKING & set(delta))
        breaking += bool(hits)
        flag = f"   *** breaking: {', '.join(hits)} ***" if hits else ""
        print(f"  CHANGED  {name} [{old[name][0]}]{flag}")
        for k in sorted(delta):
            was, now = delta[k]
            print(f"             {k}: {was!r} -> {now!r}")

    print()
    print(f"{changed} parameter(s) changed, {len(added)} added, {len(removed)} removed")
    if breaking or added or removed:
        print("RESULT: parameter surface CHANGED — treat as a breaking release.")
        return 1
    print("RESULT: parameter surface intact — saved Sets bind as before.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
