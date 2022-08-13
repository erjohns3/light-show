# club time

## example execution
To start with 5% volume locally (terminal UI). Starts on the show hooked, and reloads 1 second behind when you save any of the files in the directory
```python server.py --local --volume 7 --show butter --reload --skip 30```

To use the UI, the terminal output will output something like `serving at: `, just copy that link and paste into your web browser.

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
sudo ss -lptn 'sport = :8000'


## todo songs
* joji: https://www.youtube.com/watch?v=PEBS2jbZce4


* https://www.youtube.com/watch?v=Luq2a3Q244U
   * a lot of the songs from it are here https://www.youtube.com/watch?v=FAsrHKXHh4o



## to fix the terminal output scaling, here are some mappings:
* Green:
    * 1: 100%
    * .9: 95%
    * .5: 70%
    * .4: 60%
    * .3: 45%
    * .2: 30%
    * .15: 15%
    * .14: 10%
    * .13: 8%
    * .12: 5%
    * .11: 1%
    * .1: 0%

* Red:
    * 1: 100%
    * .9: 95%
    * .5: 70%
    * .4: 60%
    * .3: 40%
    * .25: 25%
    * .2: 10%
    * .14: 2%
    * .13: 1%
    * .12: 0%

* Blue:
    * 1: 100%
    * .9: 90%
    * .5: 65%
    * .4: 50%
    * .3: 35%
    * .25: 28%
    * .2: 20%
    * .14: 5%
    * .13: 3%
    * .12: 1%
    * .11: 0%