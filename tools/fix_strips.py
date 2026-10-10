#!/usr/bin/env python3
"""Find and repair multi-frame bitmap strips whose height isn't a multiple of
their frame count.

    python3 tools/fix_strips.py          # report only, exit 1 if any are found
    python3 tools/fix_strips.py --fix    # rewrite them in place

%xl(id, file, n) splits a strip into n frames of height // n rows. The ports
scaled whole strips to fit 375x320, which left fractional frames: frame k
then starts k * fraction rows too early and icons show sliced or mixed
(the Adwaitapod battery). The scaling was linear, so resizing the strip to
n * round(h / n) puts every frame back on its own rows. Nearest-neighbour
keeps the magenta transparency key and palettes intact.
"""
import glob
import os
import re
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XL = re.compile(r'%xl\(\s*[^,]+,\s*([^,)]+?)\s*(?:,\s*-?\d+\s*,\s*-?\d+\s*)?'
                r'(?:,\s*(\d+)\s*)?\)')


def strips():
    """Yield (bmp path, frame counts) for every %xl with a frame count."""
    found = {}
    for skin in glob.glob(os.path.join(ROOT, 'themes/*/.rockbox/wps/*')):
        if os.path.splitext(skin)[1] not in ('.wps', '.sbs', '.fms'):
            continue
        base = os.path.splitext(skin)[0]
        for f, n in XL.findall(re.sub(r'(?m)^#.*', '', open(skin, errors='ignore').read())):
            p = os.path.join(base, f)
            if n and os.path.isfile(p):
                found.setdefault(p, set()).add(int(n))
    return sorted(found.items())


def main():
    fix = '--fix' in sys.argv
    bad = 0
    for p, ns in strips():
        im = Image.open(p)
        w, h = im.size
        if all(h % n == 0 for n in ns):
            continue
        rel = os.path.relpath(p, ROOT)
        if len(ns) > 1:
            print('%s: h=%d, loaded as %s frames, fix by hand' % (rel, h, sorted(ns)))
            bad += 1
            continue
        n = ns.pop()
        nh = n * max(1, round(h / n))
        print('%s: h=%d n=%d -> %d' % (rel, h, n, nh))
        bad += 1
        if fix:
            im.resize((w, nh), Image.Resampling.NEAREST).save(p)
    if bad and not fix:
        sys.exit(1)


if __name__ == '__main__':
    main()
