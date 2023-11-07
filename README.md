# Club time
## TLDR:

### Requirements
* Install ffmpeg, and have avaliable on your path
* `pip install -r requirements.txt`

#### warning
on linux you need to "pip install aubio", on everything else, just "pip install -r requirements.txt"

### Running locally (not on the doorbell, just on your computer)
* example 1, start the light show "shelter" locally (terminal UI), and with arrow key support. 
    * `python light_server.py --local --keyboard --show shelter`
* example 2, start the show hooked with 5% volume locally (terminal UI). Starts with arrow key support.
    * `python light_server.py --local --keyboard --volume 7 --show butter --skip 30`

## Using the UI 
To use the UI, the terminal output will output something like:
```
Dj interface: http://YOUR_IP:9555/dj.html
Queue: http://YOUR_IP:9555
```
Just copy either into your browser, and you'll be able to control the show from there.

# TODO
* winamp:
  * check if passing `load_from_cache` to load_preset affects things. its only if the caching results in textures or something being deleted?
  * support windows
  * ask on the discord about low res rendering
  * milkdrop v2? not supported in projectM yet i think
* look for inspiration:
  * https://www.youtube.com/watch?app=desktop&v=Jrb5PqiDMSY
* check that --speed .5 follows --delay .189
* cubic bezier for custom curves
* label intensity of some lights and cleanup
    * get rid of white flashes alone
* add more variety
    * custom fades - linear, sine wave, exponential dropoff
    * andrew's idea: apply a custom fade to all effects in a scene.  could end at a different point too
    * chris's idea - changing some effects but not all - on non-high delta changes


#### stem stuff
* djmdContent looks like right table
  * from db: "/PIONEER/USBANLZ/6f8/d6979-9a49-430c-9d42-ba5122158a4c/ANLZ0000.DAT"
    * C:\Users\Ray\AppData\Roaming\Pioneer\rekordbox\share\PIONEER\USBANLZ
      * for fileformat https://github.com/dylanljones/pyrekordbox
      * https://pyrekordbox.readthedocs.io/en/stable/formats/anlz.html
* unencrypting db:
  * building sqlcipher
    * https://www.domstamand.com/compiling-sqlcipher-sqlite-encrypted-for-windows-using-visual-studio-2022/
    * C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat
    * T:\programming\random\sqlcipher\bld\sqlite3.exe
      * PRAGMA key = '402fd482c38817c35ffa8ffb8c7d93143b749e7d315df7a81732a1ff43608497';
      * .output decrypted_master.db
      * .exit



# To autogenerate
### Note that the --show parameter here fuzzy finds the filename
`python light_server.py --local --autogen shelter`

### to autogenerate everything for a party
`python light_server.py --local --autogen`

### autogen_mode options
* `both` [DEFAULT] - autogenerates both normal and laser modes
* `normal` - autogenerates normal
* `lasers` - autogenerates laser mode
* `simple` - autogenerates simple RBBB 1 bar for song

# Getting songs
### download song from youtube and make show file (auto finds BPM and offset)
`python youtube_helpers.py "YOUTUBE_URL_HERE"`

#### if you just want the song and dont want to generate show (unlikely), then run
`python youtube_helpers.py --no_show "YOUTUBE_URL_HERE"`

### To get all songs from doorbell
It should be pretty good about auto downloading specific songs with the --show parameter (run it and see what it says), but to download all songs, run:
`scp -r pi@doorbell:/home/pi/light-show/songs .`

### To push your songs TO the doorbell
`scp -r songs pi@doorbell:/home/pi/light-show/`

#### copy generated shows to doorbell
`scp -r effects/autogen_shows doorbell:/home/pi/light-show/effects/autogen_shows`

### youtube download on command line (don't use this)
`youtube-dl -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 "https://www.youtube.com/watch?v=rwCJvSKzQkc"`


## light calibration (gamma curve)

* For testing: `python light_server.py --terminal --no_gamma --full_grid --skip_autogen`

quadradic bezier: https://www.desmos.com/calculator/sef06jhcok

#### grid
* red (tested with 100% blue)
  * 25 light -> 50 term
  * 9 light  -> 25 term
    * quadratic bezier with these two: https://www.desmos.com/calculator/sef06jhcok
      * p1 = (.4425, 0)
* green (tested with 100% red)
  * 20 light -> 50 term
  * 6 light  -> 25 term
    * quadratic bezier with these two: https://www.desmos.com/calculator/ayyj9zmmuk
      * p1 = (.6, 0) 
* blue (tested with 100% red)
  * 25 light -> 50 term
  * 2 light  -> 25 term
    * quadratic bezier with these two: 
      * NEED BETTER
      * p1 = (.5, 0)

#### floor
* red (tested with 100% blue)
* green (tested with 100% red)
* blue (tested with 100% red)


### old gamma stuff
```
scaled_grid_0_1 = grid_helpers.grid / 100
scaled_grid_0_1[:, :, 0] = np.power(scaled_grid_0_1[:, :, 0], 2)
scaled_grid_0_1[:, :, 1] = np.power(scaled_grid_0_1[:, :, 1], 2.3)
grid_helpers.grid[:, :, 2] = np.power(scaled_grid_0_1[:, :, 2], 2)
```

## settiing up on new rasp pi
* you HAVE to install pulse (or else audio will suck i think)
* you have to compile SDL from source (unless updated) you need 2.0.16 i think (2.0.14 as of writing)


## andrew specific commands

`python light_server.py --local --keyboard --delay .189 --autogen shelter --volume 5`
`python light_server.py --local --keyboard --reload --delay .189 --volume 5 --show "a breath"`

## ideas for lights
* from tokyo vent
  * Flash  75 blue, 25 of, right to red 
  * 1 beat before drop the flash

## stretch todo
* visualizer: https://github.com/projectM-visualizer/projectm
  * milkdrop is the name of the old winamp one
* halloween
    * spooky lights for UI
    * make it spooky button
        * add "boo" sounds to drop
        * lights are all orange

## concepts in the code
simple_effects = [

]

effects_config = {
  effect_name: {
    'bpm': int,
    'song_path': str,
    'delay_lights': float,
    'skip_song': float,
    'beats': [components...]
  }
}

channels = LIGHT_COUNT floats describing what rgb lights to turn on 0-100
component = one effect in the beats array, either a complex or simple component

channel_lut = {
  effect_name: {
      'length': int,
      'loop': bool,
      'info': GridInfo OR [GridInfo...],
      'beats': [floats...], (compiled beats)
    }

}

# Other
## ideas for python audio feature extraction:
* https://github.com/Yaafe/Yaafe
* https://github.com/tyiannak/pyAudioAnalysis
    * doc is bit sparse, really just this: https://github.com/tyiannak/pyAudioAnalysis/wiki/2.-General
* https://github.com/librosa/librosa
* https://github.com/aubio/aubio/tree/master/python/demos
    * c library with python module


## random links
* DB C:\Users\Ray\AppData\Roaming\Pioneer\rekordbox
        db.serialize(function () {
            db.run("PRAGMA cipher_compatibility = 4");
            db.run("PRAGMA key = '402fd482c38817c35ffa8ffb8c7d93143b749e7d315df7a81732a1ff43608497'");
            db.each(`select 
                    h.created_at, 
                    ifnull(c.Title, '') as Track, 
                    ifnull(c.Subtitle, '') as Mix, 
                    ifnull(l.Name, '') as Label, 
                    ifnull(a.Name, '') as Artist
                    from djmdSongHistory as h
                    join djmdContent as c on h.ContentID = c.ID
                    left join djmdArtist as a on c.ArtistID = a.ID
                    left join djmdLabel as l on l.ID = c.LabelID
                    order by h.created_at desc
                    limit 1;`, function (err, row) {

                let artist = row['Artist'].toUpperCase();
                let track = row['Track'].toUpperCase();
                let label = row['Label'].toUpperCase();
                let remix = row['Mix'].toUpperCase();

                _this.currentTrackDetails['artist'] = artist;
                _this.currentTrackDetails['track'] = track;
                _this.currentTrackDetails['label'] = label;
                _this.currentTrackDetails['remix'] = remix;

            });
        });
        db.close();



* USE REKORDBOX 6.6.4
  * https://rekordbox.com/en/support/faq/v6/#faq-q600141
    * direct link: https://cdn.rekordbox.com/files/20220623164635/Install_rekordbox_x64_6_6_4.zip?_ga=2.16932921.1467977363.1685931086-1211040754.1685660184
* rekordbox hooks
  * https://github.com/Unreal-Dan/RekordBoxSongExporter
    * which is based on https://github.com/erikrichardlarson/unbox
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


## andrews zetai timing
* FINISHED AUTOGENERATING ALL (208) SHOWS IN DIRECTORY songs in 107.53671836853027 seconds


## compress png on linux
pngquant --quality=65-80 image.png

## benchmark
* python -m cProfile -s tottime light_server.py --local --show "dom dolla" --volume 0 > testing/temp.txt
* kernprof -lv light_server.py --local --show "rivers" --volume 0
  * line by line






aubio error on rasp pi


finished downloading https://www.youtube.com/watch?v=NSNcGYkp8v8 to /home/pi/light-show/songs/Wallows - OK (Official Video).ogg in 27.681249618530273 seconds
Exception in thread Thread-3:
Traceback (most recent call last):
  File "/usr/lib/python3.7/threading.py", line 917, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.7/threading.py", line 865, in run
    self._target(*self._args, **self._kwargs)
  File "light_server.py", line 303, in download_song
    src_bpm_offset_cache = autogen.get_src_bpm_offset(filepath, use_boundaries=True)
  File "/home/pi/light-show/autogen.py", line 126, in get_src_bpm_offset
    src = aubio.source(str(song_filepath), 0, hop_s)
RuntimeError: AUBIO ERROR: source_wavread: Failed opening /home/pi/light-show/songs/Wallows - OK (Official Video).ogg (could not find RIFF header)




doorbell light-show$ pip install --upgrade pip
WARNING: pip is being invoked by an old script wrapper. This will fail in a future version of pip.
Please see https://github.com/pypa/pip/issues/5599 for advice on fixing the underlying issue.
To avoid this problem you can invoke Python with '-m pip' instead of running pip directly.
/usr/lib/python3/dist-packages/secretstorage/dhcrypto.py:15: CryptographyDeprecationWarning: int_from_bytes is deprecated, use int.from_bytes instead
  from cryptography.utils import int_from_bytes
/usr/lib/python3/dist-packages/secretstorage/util.py:19: CryptographyDeprecationWarning: int_from_bytes is deprecated, use int.from_bytes instead
  from cryptography.utils import int_from_bytes
Defaulting to user installation because normal site-packages is not writeable
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Requirement already satisfied: pip in /home/pi/.local/lib/python3.7/site-packages (22.2.2)
Collecting pip
  Downloading pip-22.3.1-py3-none-any.whl (2.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 5.5 MB/s eta 0:00:00
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 22.2.2
    Uninstalling pip-22.2.2:
      Successfully uninstalled pip-22.2.2
  WARNING: The scripts pip, pip3, pip3.10 and pip3.7 are installed in '/home/pi/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.