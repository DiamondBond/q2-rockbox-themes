# Q2 Rockbox themes

Unofficial ports of Rockbox themes to the **Shanling Q2** (375x320), for the
[Shanling Q2 Rockbox port](https://github.com/DiamondBond/q2-rockbox) running
under [Q2 Pod](https://github.com/DiamondBond/q2-pod) V8.3 or later.

Browse the collection, with screenshots and per-theme downloads, at
**https://diamondbond.github.io/q2-rockbox-themes/**.

These come from themes.rockbox.org, mainly for the iPod Classic and the
Eros Q / Hifiwalker H2 (both 320x240). Each theme was re-mapped to 375x320
rather than scaled, and kept clear of the Q2's rounded glass corners. Reports
are welcome in the issues.

## Install

1. Download `q2-rockbox-themes-1.2.zip` from
   [Releases](https://github.com/DiamondBond/q2-rockbox-themes/releases).
2. Unzip it onto the card's root, next to `.rockbox`. It merges the themes
   into the existing `.rockbox`.
3. On the player: Settings > Theme Settings > Browse Theme Files, pick one.

Single themes can be downloaded from the site; their zips live in `docs/zips/`
and unzip the same way.

## Repository layout

- `themes/<name>/.rockbox/` — one theme each, ready to copy over the card's
  `.rockbox`.
- `fonts/` — every font the themes use.
- `my-setup/` — the Q2 port's own config, EQ presets and shortcuts (one
  user's setup, kept here as an example, not a default).
- `docs/` — the GitHub Pages site: `index.html`, screenshots in `shots/` and
  the per-theme zips in `zips/`.
- `tools/credits.json` — author, licence and source for every theme.
- `tools/make_release.py` — builds the full release zip and the per-theme
  zips; `tools/make_site.py` — writes `docs/themes.json` for the site.

## Credits and licences

Themes are by their original authors on themes.rockbox.org; this repo only
ports them to the Q2. `tools/credits.json` lists each author, licence and
source theme, and the site shows them on every card. If you are an author and
want a different credit, a licence note, or removal, please open an issue.
