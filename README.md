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

Originally released in 2015 on maxforlive.com:
<https://maxforlive.com/library/device/3194/kawai-k5000-controller>

*If you just want to download and use the device, [maxforlive.com](https://maxforlive.com/library/device/3194/kawai-k5000-controller) is the easiest method.* 
This repo is more development-oriented.

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

## Development

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)

---
