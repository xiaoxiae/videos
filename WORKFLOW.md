# Workflow
My internal workflow document, so I don't forget to do something when I'm creating new videos. It could alternatively serve as a workflow document for anyone who would like to produce videos the way that I do.

## Scene and script creation
- clone `00-template/` into the new video folder, change the name accordingly
	- likely also cross the video idea from `IDEAS.md`, since it's in active development
- create all of the scenes in the video, along with the script
	- periodically update `DESCRIPTION.md` with links to resources used
- run `build.py`, creating all of the parts of the video

## Recording audio
- sample noise using `get_noise_profile`
- record all of the voice lines using the `record` script in the `audio/` folder
	- do this in one session, so the voice setup sounds the same
- TODO: normalize all of the audio tracks

## Cutting
- open Kdenlive and add the `audio/` and `video/` folder
- make sure that the `video/` folder is proxy, since we're cutting in 4K
	- this is absolutely necessary, if you don't have terabytes of RAM
- start adding the scenes, adding still frames to add correct spacing, along with the audio and subtitles
	- don't forget the intro and outro!
- export and spam your friends for feedback

## Post-export
- update `DESCRIPTION.md` with timestamps
- TODO: YouTube process
- add a link to the new video to:
	- my website, updating the newest video in the process
	- this repository's `README.md`

### Useful Kdenlive shortuts

| Key            | Action |
| ---            | ---    |
| `Ctrl+Shift+r` | cut    |
