#!/usr/bin/env python3
"""Write docs/themes.json for the GitHub Pages grid.

    python3 tools/make_site.py

Reads tools/credits.json, checks every theme has its screenshots and zip, and
emits the data the site's app.js fetches. Run make_release.py first (it makes
the zips) and capture the screenshots into docs/shots/.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    credits = json.load(open(os.path.join(ROOT, 'tools', 'credits.json')))
    themes = []
    missing = []
    for d in sorted(os.listdir(os.path.join(ROOT, 'themes'))):
        c = credits.get(d)
        if not c:
            missing.append('%s: no credits entry' % d)
            continue
        for shot in ('wps', 'menu'):
            p = os.path.join(ROOT, 'docs', 'shots', '%s-%s.png' % (d, shot))
            if not os.path.isfile(p):
                missing.append(p)
        if not os.path.isfile(os.path.join(ROOT, 'docs', 'zips', d + '.zip')):
            missing.append('docs/zips/%s.zip' % d)
        themes.append(dict(dir=d, **c))
    if missing:
        print('\n'.join(missing), file=sys.stderr)
        sys.exit('%d missing files' % len(missing))
    out = os.path.join(ROOT, 'docs', 'themes.json')
    json.dump(themes, open(out, 'w'), indent=1, ensure_ascii=False)
    print('%s: %d themes' % (out, len(themes)))


if __name__ == '__main__':
    main()
