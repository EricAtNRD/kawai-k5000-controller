#!/usr/bin/env python3
"""Rewrite the version line in a device's header comment, in place.

The device displays its version from a plain comment box in the patcher, so it
has to be edited by hand for every release. Doing that in Max would work, but
re-saving there also rewrites the patcher's `appversion` — this device still
reports 6.1.10, which is what keeps it loadable on older installs.

So this edits the container directly. An unfrozen .amxd is:

    'ampf' + <u32 LE 4> + 'mmmm'          12 bytes
    'meta' + <u32 LE 4> + <u32 LE 0>      12 bytes
    'ptch' + <u32 LE payload_len> + payload

The payload is the patcher JSON, so the edit is a byte substitution inside it
plus a fixed-up chunk length. Everything outside the replaced bytes is left
untouched, which keeps the resulting diff to the one line that changed.

Usage:  set-device-version.py DEVICE.amxd NEW_VERSION
        set-device-version.py "Kawai K5000 Controller.amxd" 1.6
"""

import re
import struct
import sys

PTCH_TAG_OFFSET = 24
PAYLOAD_OFFSET = 32


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    path, new_version = sys.argv[1], sys.argv[2]

    data = bytearray(open(path, "rb").read())
    if bytes(data[PTCH_TAG_OFFSET:PTCH_TAG_OFFSET + 4]) != b"ptch":
        sys.exit(f"{path}: no 'ptch' chunk at offset {PTCH_TAG_OFFSET} "
                 "— frozen device, or not an .amxd?")

    declared = struct.unpack("<I", data[28:32])[0]
    payload = bytes(data[PAYLOAD_OFFSET:PAYLOAD_OFFSET + declared])
    if len(payload) != declared:
        sys.exit(f"{path}: truncated — ptch declares {declared} bytes, "
                 f"found {len(payload)}")

    matches = re.findall(rb"Version [0-9][0-9A-Za-z.\-]*", payload)
    if len(matches) != 1:
        sys.exit(f"{path}: expected exactly one 'Version …' string, "
                 f"found {len(matches)}: {matches}")

    old = matches[0].decode()
    new = f"Version {new_version}"
    if old == new:
        print(f"{path}: already reads '{old}' — nothing to do")
        return 0

    payload = payload.replace(matches[0], new.encode(), 1)
    trailer = bytes(data[PAYLOAD_OFFSET + declared:])

    with open(path, "wb") as fh:
        fh.write(bytes(data[:28]))
        fh.write(struct.pack("<I", len(payload)))
        fh.write(payload)
        fh.write(trailer)

    print(f"{path}: '{old}' -> '{new}'")
    print(f"  ptch payload {declared} -> {len(payload)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
