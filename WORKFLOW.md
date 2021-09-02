# Workflow
My internal workflow document, so I don't forget to do something when I'm creating new videos. It could alternatively serve as a workflow document for anyone who would like to produce videos the way that I do.

## Scene and script creation
1. clone `00-template/` into the new video folder
	- change the name accordingly
	- likely also remove the video idea from `IDEAS.md`
2. create all of the scenes in the video, along with the script
	- update `DESCRIPTION.md` with:
		- what the video is about
		- resources used
		- source code
		- music
3. run `build.py`, creating the video assets

## Recording audio
1. sample noise using `get_noise_profile`
2. record all of the voice lines using the `record` script in the `audio/` folder

## Cutting
- open Kdenlive and add the `audio/` and `video/` folder
- make sure that the `video/` folder is proxy, since we're cutting in 4K
- start adding the scenes, adding still frames to add correct spacing, along with the audio and subtitles

## Post-export
- update `DESCRIPTION.md` timestamps
- add a link to the new video to:
	- my website (`videos.py` script)
	- this repository's `README.md`

### Useful Kdenlive shortuts

| Key            | Action |
| ---            | ---    |
| `Ctrl+Shift+r` | cut    |
