# club time

# TODO
* cubic bezier for custom curves
* label intensity of some lights and cleanup
    * get rid of white flashes alone
* add more variety
    * color wheel rotation
    * custom fades - linear, sine wave, exponential dropoff
    * andrew's idea: apply a custom fade to all effects in a scene.  could end at a different point too
    * chris's idea - changing some effects but not all - on non-high delta changes
* halloween
    * spooky lights for UI
    * make it spooky button
        * add "boo" sounds to drop
        * lights are all orange

# Running locally
## To get all songs from doorbell
`scp -r pi@doorbell:/home/pi/light-show/songs .`

## To push your songs TO the doorbell
`scp -r songs pi@doorbell:/home/pi/light-show/`

## example 1
`python server.py --local --keyboard --reload --show shelter`

## example 2
To start with 5% volume locally (terminal UI). Starts on the show hooked, and reloads when you save in the directory
`python server.py --local --keyboard --reload --volume 7 --show butter --skip 30`

## Using the UI 
`python server.py --local`
To use the UI, the terminal output will output something like `serving at: `, just copy that link and paste into your web browser.

# To autogenerate
### Note that the --show parameter here fuzzy finds the filename
`python server.py --local --autogen --show shelter`


## dont use this unless andrew
`python server.py --local --keyboard --delay .189 --autogen --volume 5 --show shelter`


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



## youtube download
`youtube-dl -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 "https://www.youtube.com/watch?v=rwCJvSKzQkc"`

## find pid of the process using the port
sudo ss -lptn 'sport = :1337'

## convert an mp3 to ogg
ffmpeg -i "input.mp3" -c:a libvorbis -q:a 4 "output.ogg"

## songs andrew might want to make shows to
* joji: https://www.youtube.com/watch?v=PEBS2jbZce4
* https://www.youtube.com/watch?v=Luq2a3Q244U
   * a lot of the songs from it are here https://www.youtube.com/watch?v=FAsrHKXHh4o
