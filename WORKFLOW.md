# Workflow
My internal workflow document, so I don't forget to do something when I'm creating new videos.
It could alternatively serve as a workflow document for anyone who would like to produce videos the way that I do.

## Scene and script creation
1. clone an appropriate template into the new video folder
	- change the name accordingly
	- remove the video idea from `IDEAS.md` (if it's there)
2. create all of the scenes in the video, along with the script
	- update `DESCRIPTION.md` with:
		- what the video is about
		- resources used
		- source code
		- music
3. run `build.py`, creating the video assets (video segments and still videos at the end of each one)
	- scene classes that should be transparently rendered must start with `Transparent`

### Using VectorMagic
1. on Windows: convert the picture using basic settings, save to SVG
2. on Linux:
	- remove background
	- ungroup everything
	- convert everything to path (for good mesure, but it likely already is)
	- outset a few times, else it will be rendered incorrectly
		- might need to Edit > Preferences > Behavior and edit steps if it outsets by too much
		- there is a bug in InkScape that removes the color after outsetting; to fix this, edit the file such that each path has the following style format: `style="color:#000000;fill:#3a302c;-inkscape-stroke:none"` (removing fill and opacity in the process); use a Vim macro to do this

### Using OBS
- the profiles and scenes are all in the `OBS/` directory

## Recording audio
1. sample noise using `get_noise_profile`
2. record all of the voice lines using the `record` script in the `audio/` folder
3. run `build.py` to normalize the audio across all lines

## Cutting
- create a new KdenLive project, name it `video.kdenlive`
- open Kdenlive and add the `audio/` and `video/` folder
	- make sure that the `video/` folder is proxy, since we're cutting in 4K
- start adding the scenes, adding still 1s videos to add correct spacing, along with the **audio** and **subtitles**
- the voice audio should be **full**, the music audio should be apx. **-22 dB**

## Post-export
- update `DESCRIPTION.md` timestamps
- place the video (named `video.mp4`) to `export/`, along with a thumbnail (named `thumbnail.png`) and run `export/encode` for downscaling

## YouTube upload
1. step:
	- name
	- description
	- miniature
	- playlist
	- "show more":
		- language (english)
		- license (standard YouTube)
2. step:
	- subtitles: from file
	- final screen - import from the previous video
4. step:
	- make the video public

## Post-YouTube upload
- add a link to the new video to:
	- my website (`videos.py` script)
	- this repository's `README.md`
	- Patreon

### Useful Kdenlive shortuts

| Key            | Action |
| ---            | ---    |
| `Ctrl+Shift+r` | cut    |
