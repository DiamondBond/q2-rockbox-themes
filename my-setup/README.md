# my-setup: the H2 setup on the Q2

The user's Eros Q / Hifiwalker H2 Rockbox setup, ported to the Shanling Q2
port. Install by copying onto the card's root:

    cp config.cfg    /run/media/diamond/Q2/.rockbox/config.cfg
    cp shortcuts.txt /run/media/diamond/Q2/.rockbox/shortcuts.txt
    cp -r eqs        /run/media/diamond/Q2/.rockbox/eqs

## Changes from the H2 config

- Dropped `roll_off` (filter roll-off; the Q2's CS43131 has no such setting)
  and `headphone lineout select` (Eros Q codec only).
- `brightness: 55` (of the H2's 255) became `5` on the Q2's 1..20. Adjust in
  Settings > Display if it is too dim.
- Paths are single-volume: `/<microSD0>/Music/` became `/Music/`.
- `pause on headphone unplug: pause` is new; Q2 headphone detection landed
  2026-10-06.
- WPS/SBS/backdrop point at the ported LookAtMe, whose font is
  `16-Inter-Bold.fnt` (the H2 ran `16-SFPro-Bold-CJK.fnt` through the theme's
  Inter mapping).
- The quick screen's bottom item became Gain (`dac_power_mode`) in place of
  the H2's Filter; the Shortcuts menu gained a Gain entry too.

## Notes

- Shutdown (hold Play, or the Shutdown shortcut) exits to Q2 Pod but keeps
  Rockbox as the default. Settings > System > Boot stock OS makes Q2 Pod the
  default instead.
- Reboot (`/sbin/reboot`) is untested on the Q2.
- EQ presets in `eqs/` were copied from the H2 unchanged; `chu3.cfg` matches
  the EQ already in `config.cfg`.
