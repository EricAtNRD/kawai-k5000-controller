# Kawai K5000 Controller

This is a Max for Live MIDI Effect that acts as a "control panel" for the 
Kawaii K5000S (or R) additive synthizer that provides virtual knobs (that 
can be automated in Live) for most of the actual knobs on the K5000.  

All parameters should auto-map nicely to the Push or other controllers. 
On the Push there are three "banks" of parameters, so make sure not to miss 
the second and third pages!

Please note that each knob has *a switch* below to activate it. 
This allows you to only alter selected parameters in a stored patch.

Originally released in 2015. Listed on maxforlive.com:
<https://maxforlive.com/library/device/3194/kawai-k5000-controller>

Author: Eric Weik / [circumjacence.com](https://circumjacence.com)

---

## What it does

- 16 labelled knobs mapped to the K5000's MIDI CC parameters, each automatable
  from Live (as well as 3 other knobs for Port. / ModWh / ChAfterTouch)
- A per-knob **"active" toggle**, so only the parameters you care about transmit
  (helpful for randomizing or storing just a few changed values in a Live Set)
- **CC Listen** — the device follows CC sent *from* the synth, so moving a knob
  on the K5000S updates the matching dial in Live.
- **Xmit All** — pushes the current value of every active knob to the synth in
  one go, for re-syncing the hardware to the state of a Set. (It appears as
  `Resend All` in Live's parameter and automation lists.). *Please note*:  
  "Xmit All" staggers the sending of each knob value by 50ms.


## Requirements

- Ableton Live with Max for Live
- A Kawai K5000S or K5000R, connected via MIDI
- The device is a **MIDI Effect** — place it on a MIDI track whose output is
  routed to the K5000.

## Installation

Drop `Kawai K5000 Controller.amxd` onto a MIDI track in Live, or copy it into
your User Library under `Presets/MIDI Effects/Max MIDI Effect/`.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

---

## Development

### Readable diffs for `.amxd`

A `.amxd` is a binary container wrapping the patcher JSON, so git treats it as an
opaque blob by default. This repo is set up for Ableton's
[maxdiff](https://github.com/Ableton/maxdevtools/blob/main/maxdiff/README.md)
tool, which renders a condensed, readable summary of the patch instead.

`.gitattributes` is version controlled and already routes `.amxd` through a
`diff=amxd` driver. The driver itself is **per-clone** and is not (and cannot be)
version controlled, so after cloning:

1. Install the tools and make sure `python3` is 3.10 or newer:

   ```bash
   git clone https://github.com/Ableton/maxdevtools.git ~/maxdevtools
   ```

2. Add the text converters to `.git/config` in your clone:

   ```ini
   [diff "maxpat"]
     textconv = python3 ~/maxdevtools/maxdiff/maxpat_textconv.py
   [diff "amxd"]
     textconv = python3 ~/maxdevtools/maxdiff/amxd_textconv.py
     binary = true
   [diff "als"]
     textconv = python3 ~/maxdevtools/maxdiff/als_textconv.py
     binary = true
   ```

`git diff` will now show patch summaries rather than "Binary files differ".

To check a device outside of git:

```bash
python3 ~/maxdevtools/maxdiff/amxd_textconv.py "Kawai K5000 Controller.amxd"
```

Be aware that the `parameters:` block at the top of the summary is emitted in the
patcher's own key order, which is not stable between saves. It can therefore
produce a large block of pure reordering churn that is not a real change. To read
past it, compare sorted summaries:

```bash
diff <(python3 ~/maxdevtools/maxdiff/amxd_textconv.py OLD.amxd | sort) \
     <(python3 ~/maxdevtools/maxdiff/amxd_textconv.py NEW.amxd | sort)
```

#### Known issue: maxdiff and pre-Max 7 patchers

This device's patcher still carries `appversion 6.1.10` — it has never been
re-saved by a newer Max, which is deliberate, as it keeps the file loadable by
older installs. As of maxdevtools `cbec332`, `maxdiff` crashes on such files:

```
KeyError: 'modernui'
```

`modernui` was added to the `appversion` block in Max 7, and
`maxdiff/patch_printer.py` reads it without a default. Until this is fixed
upstream, patch `get_appversion_string_short()` in
`~/maxdevtools/maxdiff/patch_printer.py` to tolerate the missing keys — e.g. skip
`architecture` and `modernui` when they are absent rather than indexing them
directly.

### Checking the parameter surface

A saved Live Set binds to a device's parameters by name, and stores automation
against their type and range. Changing any of those silently breaks every Set
that already uses the device — which, for a device that has been in circulation
since 2015, is the one class of mistake worth guarding against mechanically.

`tools/param-surface-diff.py` compares the parameter surface of two `.amxd`
files and reports what actually differs:

```bash
python3 tools/param-surface-diff.py OLD.amxd "Kawai K5000 Controller.amxd"
```

It separates changes that break Set bindings — `parameter_longname`,
`parameter_shortname`, `parameter_type`, the range fields, `parameter_enum`,
`parameter_mapping_index`, and any added or removed parameter — from cosmetic
ones such as `parameter_invisible`, flagging the former inline as
`*** breaking ***`. It exits non-zero if the surface changed, so it can gate a
release.

Run it against the previous release before every commit that touches the device.
Both maxdiff and this tool answer different questions: maxdiff shows you what
changed in the patch, this shows you whether that change is safe to ship.

### Release history in git

The tracked file is always `Kawai K5000 Controller.amxd`. Each public release is
a commit against that same path plus a tag (`v1.4`, `v1.5`, `v1.6`, …), so the
change between any two releases is a real diff rather than an unrelated file.

Note that a Max for Live device has no internal title field — the name Live shows
in the device header is taken from the filename. The tracked copy therefore
displays without a version number. When publishing a release, rename the artifact
to include the version (`Kawai K5000 Controller v1.6.amxd`) so it reads correctly
in the device header.

The device is tracked **unfrozen**, and is published unfrozen too. Freezing exists
to bundle a device's dependencies into the `.amxd`, and this one has none — its
`dependency_cache` is empty and every object in the patch is stock Max, with no
abstractions, externals, JS or assets. Freezing would bundle nothing while
requiring a re-save in Max, which rewrites the patcher's `appversion` and drops
compatibility with older installs for no gain.

There is therefore no build step. Publishing a release is:

```bash
cp "Kawai K5000 Controller.amxd" "Kawai K5000 Controller v1.6.amxd"
```

…and upload. Because nothing is transformed, the file on maxforlive.com stays
byte-identical to the tracked file at the matching tag.

### Release checklist

1. Put the new device in place as `Kawai K5000 Controller.amxd`.
2. Review the patch change — `git diff`, or a sorted maxdiff comparison if the
   `parameters:` reordering churn gets in the way.
3. Check the parameter surface against the previous tag:
   ```bash
   python3 tools/param-surface-diff.py PREVIOUS.amxd "Kawai K5000 Controller.amxd"
   ```
   Anything marked `*** breaking ***` means saved Sets will not bind as before.
   That is a deliberate decision, not a detail — it belongs in the changelog and
   arguably in a major version bump.
4. Update `CHANGELOG.md`.
5. Commit, then tag `vX.Y`.
6. Copy to a versioned filename and upload.

## License

[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
(CC BY 4.0). See [LICENSE](LICENSE).
