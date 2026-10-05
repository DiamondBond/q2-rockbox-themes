# Q2 Rockbox themes

Unofficial ports of Rockbox themes to the **Shanling Q2** (375x320), for the
[Shanling Q2 Rockbox port](https://github.com/DiamondBond/rockbox) running
under [Q2 Pod](https://github.com/DiamondBond/q2-pod) V8.3 or later.

These come from themes.rockbox.org, mainly for the Eros Q / Hifiwalker H2
(320x240). Each theme was re-mapped to 375x320 rather than scaled, and kept
clear of the Q2's rounded glass corners. The ports are young: author and
licence credits are still being completed, and a theme may still have a
rough edge. Reports are welcome in the issues.

## Install

1. Download `q2-rockbox-themes-1.1.zip` from
   [Releases](https://github.com/DiamondBond/q2-rockbox-themes/releases).
2. Unzip it onto the card's root, next to `.rockbox`. It merges the themes
   into the existing `.rockbox`.
3. On the player: Settings > Theme Settings > Browse Theme Files, pick one.

## Repository layout

- `themes/<name>/.rockbox/` — one theme each, ready to copy over the card's
  `.rockbox`.
- `fonts/` — the fonts the themes use.
- `my-setup/` — the Q2 port's own config, EQ presets and shortcuts (one
  user's setup, kept here as an example, not a default).
- `tools/make_release.py` — builds the release zip from the sources above.

## Credits and licences

Themes are by their original authors on themes.rockbox.org; this repo only
ports them to the Q2. If you are an author and want a different credit, a
licence note, or removal, please open an issue.
