#!/usr/bin/env python3
"""Build the Q2 theme release zips.

    python3 tools/make_release.py [version]

Writes:
  - dist/q2-rockbox-themes-<version>.zip: an INSTALL.txt, every theme in
    themes/, and every font in fonts/, laid out to unzip onto the card's root.
  - docs/zips/<theme>.zip for every theme: just that theme's .rockbox tree
    plus the fonts it references (cfg "font:" and every %Fl in its skins).
    The docs site links these directly.

Shipping all the fonts in the full pack keeps it dumb and safe: no theme can
fail to load one, whatever it references. The per-theme zips stay small.

Themes that share a file (an iconset, a backdrop) ship it once in the full
pack. If two themes ship different files at the same path, the build fails
rather than letting one silently overwrite the other on the card.
"""
import hashlib
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIN_EXT = ('.wps', '.sbs', '.fms', '.rwps', '.rsbs')


def digest(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def theme_fonts(theme):
    """Font file names the theme references, from cfg and every %Fl tag."""
    refs = set()
    root = os.path.join(ROOT, 'themes', theme, '.rockbox')
    for base, _, files in os.walk(root):
        for name in files:
            if not name.endswith(SKIN_EXT + ('.cfg',)):
                continue
            text = open(os.path.join(base, name), encoding='utf-8',
                        errors='replace').read()
            for m in re.finditer(r'%Fl\(\s*\d+\s*,\s*([^,)]+)', text):
                refs.add(os.path.basename(m.group(1).strip()))
            for m in re.finditer(r'^font:\s*(\S.*?)\s*$', text, re.M):
                if m.group(1) != '-':
                    refs.add(os.path.basename(
                        m.group(1).replace('/.rockbox/', '').strip()))
    return refs


def font_files():
    d = os.path.join(ROOT, 'fonts')
    return {n: os.path.join(d, n) for n in sorted(os.listdir(d))
            if os.path.isfile(os.path.join(d, n))}


def build_pack(version, fonts):
    out = os.path.join(ROOT, 'dist', 'q2-rockbox-themes-%s.zip' % version)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    themes = count = nfonts = 0
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
        for name, path in fonts.items():
            z.write(path, '.rockbox/fonts/' + name)
            nfonts += 1
    print('%s: %d themes, %d files, %d fonts, %.1f MB' %
          (out, themes, count, nfonts, os.path.getsize(out) / 1e6))


def licence_files(fonts, needed):
    """Font licence texts to bundle with a per-theme zip."""
    def squash(s):
        return re.sub(r'[^a-z0-9]', '', s.lower())
    out = []
    for name, path in fonts.items():
        if not name.lower().endswith('.txt'):
            continue
        text = squash(open(path, encoding='utf-8', errors='replace').read())
        hit = False
        for n in needed:
            family = os.path.splitext(n)[0].split('-', 1)[-1].split('-')[0]
            if len(family) >= 5 and squash(family) in text:
                hit = True
        if hit:
            out.append(name)
    return out


def build_theme_zips(fonts):
    outdir = os.path.join(ROOT, 'docs', 'zips')
    os.makedirs(outdir, exist_ok=True)
    for old in os.listdir(outdir):
        if old.endswith('.zip'):
            os.remove(os.path.join(outdir, old))
    total = 0
    for theme in sorted(os.listdir(os.path.join(ROOT, 'themes'))):
        needed = theme_fonts(theme)
        missing = sorted(needed - set(fonts))
        if missing:
            sys.exit('%s references missing fonts: %s' %
                     (theme, ', '.join(missing)))
        out = os.path.join(outdir, theme + '.zip')
        src = os.path.join(ROOT, 'themes', theme, '.rockbox')
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
            for base, _, files in os.walk(src):
                for name in sorted(files):
                    path = os.path.join(base, name)
                    z.write(path, os.path.join(
                        '.rockbox', os.path.relpath(path, src)))
            for name in sorted(needed):
                z.write(fonts[name], '.rockbox/fonts/' + name)
            for name in licence_files(fonts, needed):
                z.write(fonts[name], '.rockbox/fonts/' + name)
        total += os.path.getsize(out)
    print('docs/zips: %d zips, %.1f MB' % (len(os.listdir(outdir)), total / 1e6))


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else '1.2'
    fonts = font_files()
    build_pack(version, fonts)
    build_theme_zips(fonts)


if __name__ == '__main__':
    main()
