# Changelog

All notable changes to the Kawai K5000 Controller are documented here.

---

## [1.6]: 2026-08-11

**Key update:** if you've ever had automation on this device cause MIDI lag on
your K5000, this fixes it.

- Fixed knob changes causing MIDI CC floods, and the resulting lag. When using
  Live automation this was enough to completely saturate a 31.25kbaud MIDI 
  bus, at times producing hundreds or thousands of milliseconds of backlog.
  - The knobs are floating point and have to be folded to 7-bit MIDI CC values,
    so the device resent the same value repeatedly: a sweep through
    1.01, 1.02, 1.03 ... 1.1 transmitted the integer `1` ten times.
  - Values are now filtered to transmit only when the integer value changes.
- Fixed "Xmit All" not actually transmitting all active knobs.
  - Multiple `ctlout` objects firing from a single UI event get collapsed: only
    the last in each service window (~32ms on my system) reaches Live's MIDI
    stream. Automation was never affected, as it runs on the audio thread.
  - Each value is now staggered by 50ms, so a full transmit takes up to 800ms.
- Fixed two instances of the device in one Live Set interfering with each
  other's transmission tracking.
- Removed two orphaned `ctlout` objects that had no connections and never fired.


## [1.5]: 2015-09-05
Never published: folded into the 1.6 release.

- Removed the per-knob "active" toggles from setting
  `parameter_invisible` on all 19 of them. They cluttered the automation
  dropdown with no clear benefit.


## [1.4]: 2015-09-02

- The FF Bias and Harm Hi knobs were swapped: now fixed.
- Added the ability to listen for CC messages (so the controller can now reflect
  changes made via knobs on the K5000S).
- Added a "CC Listen" toggle (to turn the above feature on or off).
- Added modwheel and channel aftertouch knobs. It might seem redundant to have
  these as knobs, but I often use them in my patches (and I seem to recall they
  were used in many K5000 presets as well). It might be useful to have them 
  as knobs for automation or control via external surfaces / knobs.

[1.4]: https://maxforlive.com/library/device/3194/kawai-k5000-controller
