# club time


## example: goto for light show debugging on terminal (shelter)
python server.py --local --keyboard --reload --show shelter

# To get all songs from doorbell
```
scp -r pi@doorbell:/home/pi/light-show/songs .
```

## other features
To start with 5% volume locally (terminal UI). Starts on the show hooked, and reloads when you save in the directory
```python server.py --local --volume 7 --show butter --reload --skip 30```

To use the UI, the terminal output will output something like `serving at: `, just copy that link and paste into your web browser.

# To autogenerate
### Note that the --show parameter here fuzzy finds the filename
python server.py --local --autogen --enter --show shelter

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




* youtube-dl -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 "https://www.youtube.com/watch?v=rwCJvSKzQkc"


* python server.py --local --volume 7 --show butter
--reload --speed 1 --skip 80

* find port for python
sudo ss -lptn 'sport = :1337'


## todo songs
* joji: https://www.youtube.com/watch?v=PEBS2jbZce4


* https://www.youtube.com/watch?v=Luq2a3Q244U
   * a lot of the songs from it are here https://www.youtube.com/watch?v=FAsrHKXHh4o
