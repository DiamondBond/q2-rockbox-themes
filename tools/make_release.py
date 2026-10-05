#!/usr/bin/env python3
"""Build the Q2 theme release zip.

    python3 tools/make_release.py [version]

Writes dist/q2-rockbox-themes-<version>.zip: an INSTALL.txt, every theme in
themes/, and every font in fonts/, laid out to unzip onto the card's root.
Shipping all the fonts keeps this dumb and safe: no theme can fail to load
one, whatever it references.

Themes that share a file (an iconset, a backdrop) ship it once. If two
themes ship different files at the same path, the build fails rather than
letting one silently overwrite the other on the card.
"""
import hashlib
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def digest(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else '1.1'
    out = os.path.join(ROOT, 'dist', 'q2-rockbox-themes-%s.zip' % version)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    themes = count = fonts = 0
    seen = {}
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(ROOT, 'INSTALL.txt'), 'INSTALL.txt')
        for theme in sorted(os.listdir(os.path.join(ROOT, 'themes'))):
            themes += 1
            src = os.path.join(ROOT, 'themes', theme, '.rockbox')
            for base, _, files in os.walk(src):
                for name in sorted(files):
                    path = os.path.join(base, name)
                    arc = os.path.join('.rockbox', os.path.relpath(path, src))
                    if arc in seen:
                        if seen[arc][1] != digest(path):
                            sys.exit('%s: %s and %s differ' %
                                     (arc, seen[arc][0], theme))
                        continue
                    seen[arc] = (theme, digest(path))
                    z.write(path, arc)
                    count += 1
        for name in sorted(os.listdir(os.path.join(ROOT, 'fonts'))):
            if name.endswith('.fnt'):
                z.write(os.path.join(ROOT, 'fonts', name),
                        '.rockbox/fonts/' + name)
                fonts += 1
    print('%s: %d themes, %d files, %d fonts, %.1f MB' %
          (out, themes, count, fonts, os.path.getsize(out) / 1e6))


if __name__ == '__main__':
    main()
