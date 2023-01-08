# Club time
## TLDR:
### Requirements
Install ffmpeg, and have avaliable on your path
`pip install -r requirements.txt`

### Running locally (not on the doorbell, just on your computer)
#### example 1
`python light_server.py --local --keyboard --show shelter`

#### example 2
To start with 5% volume locally (terminal UI). Starts on the show hooked
`python light_server.py --local --keyboard --volume 7 --show butter --skip 30`

## Using the UI 
`python light_server.py --local`
To use the UI, the terminal output will output something like `serving at: `, just copy that link and paste into your web browser.

# TODO
* cubic bezier for custom curves
* label intensity of some lights and cleanup
    * get rid of white flashes alone
* add more variety
    * custom fades - linear, sine wave, exponential dropoff
    * andrew's idea: apply a custom fade to all effects in a scene.  could end at a different point too
    * chris's idea - changing some effects but not all - on non-high delta changes


# Getting songs
It should be pretty good about auto downloading specific songs with the --show parameter, but you can also copy on mass from the doorbell with the below commands

## To get all songs from doorbell
`scp -r pi@doorbell:/home/pi/light-show/songs .`

## To push your songs TO the doorbell
`scp -r songs pi@doorbell:/home/pi/light-show/`


# To autogenerate
### Note that the --show parameter here fuzzy finds the filename
`python light_server.py --local --autogen shelter`

## to autogenerate everything for a party
`python light_light_server.py --local --autogen all --autogen_mode both`

### autogen_mode options
* `default` - autogenerates normal
* `lasers` - autogenerates laser mode
* `both` - autogenerates both normal and laser modes
* `simple` - autogenerates simple RBBB 1 bar for song

### copy generated shows to doorbell
`scp -r effects/autogen_shows doorbell:/home/pi/light-show/effects/autogen_shows`

## download song from youtube and make show file (auto finds BPM and offset)
`python youtube_helpers.py --show "YOUTUBE_URL_HERE"`


### youtube download on command line (don't use this)
`youtube-dl -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 "https://www.youtube.com/watch?v=rwCJvSKzQkc"`


# andrew specific commands

`python light_server.py --local --keyboard --delay .189 --autogen shelter --volume 5`
`python light_server.py --local --keyboard --reload --delay .189 --volume 5 --show "a breath"`

# stretch todo
* halloween
    * spooky lights for UI
    * make it spooky button
        * add "boo" sounds to drop
        * lights are all orange

# Other
## ideas for python audio feature extraction:
* https://github.com/Yaafe/Yaafe
* https://github.com/tyiannak/pyAudioAnalysis
    * doc is bit sparse, really just this: https://github.com/tyiannak/pyAudioAnalysis/wiki/2.-General
* https://github.com/librosa/librosa
* https://github.com/aubio/aubio/tree/master/python/demos
    * c library with python module


## random links
* identifying strongest beat
    * https://stackoverflow.com/questions/54718744/python-audio-analysis-find-real-time-values-of-the-strongest-beat-in-each-meter

* tap beat for bpm
    * https://www.all8.com/tools/bpm.htm

* fixing octave error (double or half bpm instead of dead on)
    * https://stackoverflow.com/questions/61621282/how-can-we-improve-tempo-detection-accuracy-in-librosa

## find pid of the process using the port
sudo ss -lptn 'sport = :1337'

## convert an mp3 to ogg
ffmpeg -i "input.mp3" -c:a libvorbis -q:a 4 "output.ogg"

## songs andrew might want to make shows to
* joji: https://www.youtube.com/watch?v=PEBS2jbZce4
* https://www.youtube.com/watch?v=Luq2a3Q244U
   * a lot of the songs from it are here https://www.youtube.com/watch?v=FAsrHKXHh4o
