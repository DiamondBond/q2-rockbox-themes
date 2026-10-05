#!/usr/bin/env python3
"""Find and repair palette BMPs whose V4/V5 header was cut down to 40 bytes.

    python3 tools/fix_bmps.py          # report only, exit 1 if any are found
    python3 tools/fix_bmps.py --fix    # rewrite them in place

Some theme bitmaps were saved with a BITMAPV4/V5 header whose size field
reads 40 and whose clrUsed was raised to cover the rest of the header. They
are self-consistent, so most viewers open them, but Rockbox reads the palette
at 14 + header size: it takes the colour masks and the 'sRGB' tag for the
palette. A 1-bit image then draws inverted (white boxes around icons) or as a
solid block (progress bars). The real palette is the last 1 << bpp entries
before the pixel data. --fix writes a plain 40-byte-header BMP with that
palette and the same pixel data.
"""
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def broken(d):
    """Return (bpp, clr_used, header size, data offset) if d is mangled."""
    if d[:2] != b'BM':
        return None
    off, = struct.unpack_from('<I', d, 10)
    hs, _, _, _, bpp = struct.unpack_from('<IiiHH', d, 14)
    clr, = struct.unpack_from('<I', d, 46)
    if bpp > 8:
        return None
    if clr > (1 << bpp) or b'BGRs' in d[14 + hs:off]:
        return bpp, clr, hs, off
    return None


def repair(d):
    bpp, _, _, off = broken(d)
    n = 1 << bpp
    palette = d[off - 4 * n:off]
    pixels = d[off:]
    info = bytearray(d[14:54])
    struct.pack_into('<I', info, 0, 40)        # biSize
    struct.pack_into('<I', info, 32, n)        # biClrUsed
    struct.pack_into('<I', info, 36, 0)        # biClrImportant
    new_off = 14 + 40 + len(palette)
    head = struct.pack('<2sIHHI', b'BM', new_off + len(pixels), 0, 0, new_off)
    return head + bytes(info) + palette + pixels


def main():
    fix = '--fix' in sys.argv[1:]
    found = 0
    for top in ('themes', 'my-setup'):
        for base, _, files in os.walk(os.path.join(ROOT, top)):
            for name in sorted(files):
                if not name.lower().endswith('.bmp'):
                    continue
                path = os.path.join(base, name)
                with open(path, 'rb') as f:
                    d = f.read()
                if not broken(d):
                    continue
                found += 1
                print(('fixed ' if fix else 'broken ') +
                      os.path.relpath(path, ROOT))
                if fix:
                    with open(path, 'wb') as f:
                        f.write(repair(d))
    print('%d mangled palette BMP(s)%s' % (found, ' fixed' if fix else ''))
    return 1 if found and not fix else 0


if __name__ == '__main__':
    sys.exit(main())
