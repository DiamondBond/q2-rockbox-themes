#!/usr/bin/env python3
"""Build the Q2 theme release zip from themes/ and the fonts they load.

    python3 tools/make_release.py [version]

Writes dist/q2-rockbox-themes-<version>.zip: an INSTALL.txt and a .rockbox/
tree that can be unzipped onto the card's root.
"""
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIN_SUFFIXES = ('.wps', '.sbs', '.rwps', '.fms', '.rsbs')
FONT_REF = re.compile(r'/(?:\.rockbox/)?fonts/([^%\s;]+)')


def used_fonts():
    used = set()
    for theme in os.listdir(os.path.join(ROOT, 'themes')):
        for base, _, files in os.walk(os.path.join(ROOT, 'themes', theme)):
            for name in files:
                if name.endswith(SKIN_SUFFIXES + ('.cfg',)):
                    text = open(os.path.join(base, name), errors='ignore').read()
                    used.update(FONT_REF.findall(text))
    return used


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else '1.0'
    out = os.path.join(ROOT, 'dist', 'q2-rockbox-themes-%s.zip' % version)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fonts = used_fonts()
    count = 0
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(ROOT, 'INSTALL.txt'), 'INSTALL.txt')
        for theme in sorted(os.listdir(os.path.join(ROOT, 'themes'))):
            src = os.path.join(ROOT, 'themes', theme, '.rockbox')
            for base, _, files in os.walk(src):
                for name in files:
                    path = os.path.join(base, name)
                    z.write(path, os.path.join('.rockbox',
                                               os.path.relpath(path, src)))
                    count += 1
        for font in sorted(fonts):
            path = os.path.join(ROOT, 'fonts', font)
            if os.path.exists(path):
                z.write(path, '.rockbox/fonts/' + font)
            else:
                print('missing font:', font, file=sys.stderr)
    print('%s: %d theme files, %d fonts, %.1f MB' %
          (out, count, len(fonts), os.path.getsize(out) / 1e6))


if __name__ == '__main__':
    main()
