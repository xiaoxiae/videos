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
3. run `./build`, creating the video assets
	- don't forget @fade decorators where needed!
	- scene classes that should be transparently rendered must start with `Transparent`!

### Using OBS
- the profiles and scenes are all in the `OBS/` directory

## Recording audio
1. sample noise using `get_noise_profile`
2. record all of the voice lines using the `record` script in the `audio/` folder
3. run `./normalize` to normalize the audio across all lines

## Cutting
- create a new KdenLive project, name it `video.kdenlive`
- open Kdenlive and add the `audio/` and `video/` folder
	- make sure that the `video/` folder is proxy, since we're cutting in 4K
	- also make sure that the resolution matches the video files (`Project > Project Settings > 4K UHD 2160p 60 fps`), though adding the video folder should prompt this
	- use 3 video and 3 audio tracks
- start adding the scenes
- the voice audio should be **full**, the music audio should be apx. **-25 dB** (there is an effect to do this)
- to create a freeze frame, use the next segment and a **freeze** modifier (without any parameters)

## Post-render
- update `DESCRIPTION.md` timestamps
- place the video (named `video.mp4`) to `export/`, along with a thumbnail (named `thumbnail.png`) and run `export/encode` for downscaling
	- the thumbnail can be extracted using `ffmpeg -i <input file> -vf "select=eq(n\,0)" -q:v 3 thumbnail.png`

## YouTube upload
1. step:
	- name
	- description
	- miniature/thumbnail
	- playlist
	- "show more":
		- language (English)
		- license (standard YouTube)
2. step:
	- subtitles: from file (with timing)
	- final screen (non-shorts) - import from the previous video
4. step:
	- make the video public (planned release at some time)

## Post-YouTube upload
- add a link to the new video to:
	- my website (`videos.py` script)
	- this repository's `README.md`
	- Patreon (again planned release)


# Other

## Changing a video name
- YouTube
- README of this repo
- Website (+ delete videos folder)
