# club time

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

Difference between intuitive and real:
100: 100
75: 40
50: 22
25: 8

(x*.9) ^ (2) from 0 to 1
https://www.wolframalpha.com/input?i=%28x*.9%29+%5E+%282%29+from+0+to+1
