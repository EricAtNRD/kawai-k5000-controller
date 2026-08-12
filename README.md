# Kawai K5000 Controller

![K5000 Controller Screenshot](images/screenshot_v1_6.png?raw=true)

This is a Max for Live MIDI Effect that acts as a "control panel" for the 
Kawai K5000S (or R) additive synthesizer that provides virtual knobs (that 
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
- **CC Listen**: the device follows CC sent *from* the synth, so moving a knob
  on the K5000S updates the matching dial in Live.
- **Xmit All**: pushes the current value of every active knob to the synth in
  one go, for re-syncing the hardware to the state of a Set. It appears as
  `Resend All` in Live's parameter and automation lists. *Please note*:  
  "Xmit All" staggers the sending of each knob value by 50ms.


## Requirements

- Ableton Live with Max for Live
- A Kawai K5000S or K5000R, connected via MIDI
- The device is a **MIDI Effect**.  Place it on a MIDI track whose output is 
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

This device's patcher still carries `appversion 6.1.10`: it has never been
re-saved by a newer Max, which is deliberate, as it keeps the file loadable by
older installs. As of maxdevtools `cbec332`, `maxdiff` crashes on such files:

```
KeyError: 'modernui'
```

`modernui` was added to the `appversion` block in Max 7, and
`maxdiff/patch_printer.py` reads it without a default. Until this is fixed
upstream, patch `get_appversion_string_short()` in
`~/maxdevtools/maxdiff/patch_printer.py` to tolerate the missing keys. E.g. skip
`architecture` and `modernui` when they are absent rather than indexing them
directly.

### Checking the parameter surface

A saved Live Set binds to a device's parameters by name, and stores automation
against their type and range. Changing any of those silently breaks every Set
that already uses the device.  For a device that has been in circulation
since 2015, this is worth guarding against mechanically.

`tools/param-surface-diff.py` compares the parameter surface of two `.amxd`
files and reports what actually differs:

```bash
python3 tools/param-surface-diff.py OLD.amxd "Kawai K5000 Controller.amxd"
```

It separates changes that break Set bindings: 
- `parameter_longname`
- `parameter_shortname`
- `parameter_type`
- the range fields
- `parameter_enum`
- `parameter_mapping_index`
- And any added or removed parameters

... from cosmetic ones such as `parameter_invisible`, and flags the former 
inline as `*** breaking ***`. It exits non-zero if the surface changed, so 
it can gate a release.

It should be run against the previous release before every commit that 
touches the device.  Both maxdiff and this tool answer different questions: 
maxdiff shows what changed in the patch, this shows whether that change is 
safe to ship.

### Release history in git

The tracked file is always `Kawai K5000 Controller.amxd`. Each public release is
a commit against that same path plus a tag (`v1.4`, `v1.5`, `v1.6`, …), so the
change between any two releases is a real diff rather than an unrelated file.

Note that a Max for Live device has no internal title field:  the name Live 
shows in the device header is taken from the filename. The tracked copy 
therefore displays without a version number. When publishing a release, 
rename the artifact to include the version (`Kawai K5000 Controller v1.6.amxd`) 
so it reads correctly in the device header.

The device is tracked **unfrozen**, and is published unfrozen too. Freezing exists
to bundle a device's dependencies into the `.amxd`, and this one has none. Its
`dependency_cache` is empty and every object in the patch is stock Max, with no
abstractions, externals, JS or assets. Freezing would bundle nothing while
requiring a re-save in Max, which rewrites the patcher's `appversion` and drops
compatibility with older installs for no gain.

There is therefore no build step. Publishing a release is:

```bash
cp "Kawai K5000 Controller.amxd" "Kawai K5000 Controller v1.6.amxd"
```

...and upload. Because nothing is transformed, the file on maxforlive.com stays
byte-identical to the tracked file at the matching tag.

### Release checklist
The steps below assume the previous release is reachable as a tag (`vPREV`) and
that the new build is sitting outside the repo as `Kawai K5000 Controller
vX.Y.amxd`. Substitute real version numbers as you go.

Note that the baseline for every comparison is pulled **out of git**, not from a
loose file on disk.  This guarantees you are diffing against exactly what
shipped. `git show` returns the stored blob untouched; the `textconv` driver
applies only to diffs, so the extracted file is byte-identical to the release.

```sh
git show vPREV:"Kawai K5000 Controller.amxd" > /tmp/prev.amxd
```

#### 1. Put the new device in place

```sh
cp "Kawai K5000 Controller vX.Y.amxd" "Kawai K5000 Controller.amxd"
```

#### 2. Set the version comment inside the patch
The device displays its own version from a plain comment box in the patcher, and
nothing validates it. A release whose file says one version and whose face says
another is an easy and very visible mistake.

Do **not** edit this in Max. Re-saving there also rewrites the patcher's
`appversion`, which this device deliberately keeps at 6.1.10 (see the maxdiff
known issue above). Edit the container directly instead:

```sh
python3 tools/set-device-version.py "Kawai K5000 Controller.amxd" X.Y
```

The tool substitutes the version string inside the `ptch` payload and fixes up
the chunk length, leaving every other byte untouched — so this shows up as a
one-line change rather than a reserialised file. It refuses to run unless it
finds exactly one `Version …` string, so it cannot silently edit the wrong
thing.

Confirm the result:

```sh
python3 ~/maxdevtools/maxdiff/amxd_textconv.py "Kawai K5000 Controller.amxd" \
  | grep '^Version'
```

It should print `Version X.Y`, matching the tag you are about to create.

#### 3. Review the patch change
```sh
git diff -- "Kawai K5000 Controller.amxd"
```

This is usually noisy: the `parameters:` block is written in the patcher's own
key order, which is not stable between saves, so unrelated reordering can swamp
the real change. To read past it, compare sorted summaries:

```bash
diff <(python3 ~/maxdevtools/maxdiff/amxd_textconv.py /tmp/prev.amxd | sort) \
     <(python3 ~/maxdevtools/maxdiff/amxd_textconv.py "Kawai K5000 Controller.amxd" | sort)
```

Expect to recognise every line. Two changes are routine and not worth alarm: the
patcher's saved window `rect`, which just records where the editing window sat,
and the version comment from step 2.

#### 4. Check the parameter surface
This is the step that protects existing users. A saved Live Set binds to the
device by `parameter_longname` and stores automation against each parameter's
type and range: so renaming, retyping or removing a parameter silently breaks
every Set already using the device, with no error and no obvious symptom.

```sh
python3 tools/param-surface-diff.py /tmp/prev.amxd "Kawai K5000 Controller.amxd"
```

Want:
```
RESULT: parameter surface intact.  Saved Sets bind as before.
```

If instead there is `*** breaking ***` on any line, stop and ask whether the
surface can be preserved.  Usually it can, by doing the work behind the existing
parameters rather than reshaping them. If the break really is necessary, it is a
deliberate release decision: state it in the changelog, and bundle it
with any other pending breaking changes so users absorb the disruption once.
There are known cosmetic wart fixes deliberately waiting for such a release.

Changes reported *without* the breaking flag (such as the 
`parameter_invisible` changes in `v1.5`) do not affect bindings and are safe 
to ship.

If a version was skipped publicly, also compare against the last **published**
tag, since that is what users are actually upgrading from.

#### 5. Load it in Live
Drop the device on a MIDI track and confirm it instantiates, the knobs move, and
CC reaches the synth. Everything above this point inspects JSON; a patch can
parse perfectly and still fail to open. This is the only step that proves the
device works.

#### 6. Update the changelog
```markdown
## [X.Y]: YYYY-MM-DD

- Bug / feature 1 description
- Bug / feature 2 description
```

#### 7. Commit and tag
Add explicit paths rather than `-A`, so unrelated work in the tree cannot ride
along into a release commit.

```sh
git add "Kawai K5000 Controller.amxd" CHANGELOG.md
git commit
git tag -a vX.Y -m "Version X.Y: <summary>"
```

#### 8. Publish

```sh
cp "Kawai K5000 Controller.amxd" "Kawai K5000 Controller vX.Y.amxd"
```

Upload that file. Nothing is built or transformed so the artifact on maxforlive.com stays byte-identical to the tracked device at tag `vX.Y`.
