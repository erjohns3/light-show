# Club time

* Light show, patterns make the visualizer light up, all else black

## TLDR:

### Requirements
* Python 3.8+
* Install ffmpeg, and have avaliable on your path
* **WARNING** On Linux you need to run `pip install aubio` BEFORE the below command. All other OS's should be fine
* `pip install -r requirements.txt`

### TLDR: Running locally (not on the rasberry pi, just on your computer in your terminal)
* example 1, start the light show "shelter" locally (terminal UI). 
    * `python light_server.py --show shelter`
* example 2, start the show hooked with 7% volume locally (terminal UI), skip to beat 30.
    * `python light_server.py --volume 7 --show butter --skip 30`

## Using the UI 
To use the UI, the terminal commands above will output something like:
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
* label intensity of some lights and cleanup
    * get rid of white flashes alone
* add more variety
    * custom fades - linear, sine wave, exponential dropoff
    * andrew's idea: apply a custom fade to all effects in a scene.  could end at a different point too
    * chris's idea - changing some effects but not all - on non-high delta changes

## STRETCH TODO
* halloween
    * spooky lights for UI
    * make it spooky button
        * add "boo" sounds to drop
        * lights are all orange
* dvd logo bouncing around



## random commands that are useful
* pid of process for port: `sudo ss -lptn 'sport = :1337'`
* mp3 to ogg: `ffmpeg -i "input.mp3" -c:a libvorbis -q:a 4 "output.ogg"`
* cloc: `cloc . --exclude-dir="temp,old,experimental,songs,effects,__pycache__,.pytest_cache,testing,projectm,presets"`
* andrew: `python light_server.py --delay .285 --autogen shelter --volume 5`
* andrew: `python light_server.py --delay .285 --volume 5 --show "a breath"`


## ideas for lights
* look for inspiration:
  * https://www.youtube.com/watch?app=desktop&v=Jrb5PqiDMSY
* from tokyo vent
  * Flash  75 blue, 25 of, right to red 
  * 1 beat before drop the flash


# Autogeneration
### Putting a parameter after --autogen fuzzy finds the song filename
`python light_server.py --autogen shelter`

### No parameter autogenerates all songs
`python light_server.py --autogen`

### --autogen_mode options
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


# light calibration (gamma curve)
* For testing on rasp pi: `python light_server.py --terminal --no_curve --full_grid --skip_autogen`
* quadradic bezier: https://www.desmos.com/calculator/sef06jhcok
* cubic bezier: https://www.desmos.com/calculator/pbaugufzbr

#### grid
* red (tested with 100% blue)
  * 60 light -> 75 term
  * 31 light -> 50 term
  * 8 light  -> 25 term
  * MANUAL ATTEMPT OF ABOVE: https://www.desmos.com/calculator/7h0prkfihz
* green (tested with 100% red)
  * 52 light -> 75 term
  * 31 light -> 50 term
  * 10 light  -> 25 term
  * MANUAL ATTEMPT OF ABOVE: https://www.desmos.com/calculator/xwm9vz7xds
* blue (tested with 100% red)
  * 60 light -> 75 term
  * 17 light -> 50 term
  * 4 light  -> 25 term
  * MANUAL ATTEMPT OF ABOVE: https://www.desmos.com/calculator/o3mmcdahfd

#### floor
* red (tested with 100% blue)
* green (tested with 100% red)
* blue (tested with 100% red)


#### laser
Needs above x to trigger
Needs at least 29 to maintain slowest speed
needs 70 to activate, but then can go down to like 40?

## concepts in the code
simple_effects = [] !TODO

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

## setting up on new rasp pi
* you HAVE to install pulse (or else audio will suck i think)
* you have to compile SDL from source (unless updated) you need 2.0.16 i think (2.0.14 as of writing)

# Other
## stem stuff
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


## songs andrew might want to make shows to
* joji: https://www.youtube.com/watch?v=PEBS2jbZce4
* https://www.youtube.com/watch?v=Luq2a3Q244U
   * a lot of the songs from it are here https://www.youtube.com/watch?v=FAsrHKXHh4o


## benchmark
* python -m cProfile -s tottime light_server.py --local --show "dom dolla" --volume 0 > testing/temp.txt
* kernprof -lv light_server.py --local --show "rivers" --volume 0
  * line by line




# OLD STUFF THAT PROBABLY ISN'T NEEDED

#### older stuff
```
def bezier_quad_only_p1(t, p1):
    return 2 * (1 - t) * t * p1 + t**2

def bezier_full_quad(t, p0, p1, p2):
    return (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2

def compute_x_to_y_bezier_quad(p1):
    x_to_y_bezier = np.array(np.zeros((101)), np.double)
    resolution = 100000
    for i in range(resolution + 1):
        t = i / resolution
        x_to_y_bezier[round(bezier_quad_only_p1(t, p1[0]) * 100)] = bezier_quad_only_p1(t, p1[1]) * 100

    if any([value for value in x_to_y_bezier == None]):
        print_red(f'x_to_y_bezier: {x_to_y_bezier} has None values with {p1=}, exiting')
        exit()
    return x_to_y_bezier

grid_red_bezier = compute_x_to_y_bezier_quad_quad((0.4425, 0))
grid_green_bezier = compute_x_to_y_bezier_quad((0.6, 0))
grid_blue_bezier = compute_x_to_y_bezier_quad((0.5, 0))
```

* red (tested with 100% blue)
  * OLD
    * quadratic bezier with these two: https://www.desmos.com/calculator/sef06jhcok
      * p1 = (.4425, 0)
* green (tested with 100% red)
  * OLD
    * quadratic bezier with these two: https://www.desmos.com/calculator/ayyj9zmmuk
      * p1 = (.6, 0) 
* blue (tested with 100% red)
  * NEW:
    https://www.desmos.com/calculator/o3mmcdahfd
    p1 = (.932, 0.033)
    p2 = (.653, 0.935)


### old gamma stuff
```
scaled_grid_0_1 = grid_helpers.grid / 100
scaled_grid_0_1[:, :, 0] = np.power(scaled_grid_0_1[:, :, 0], 2)
scaled_grid_0_1[:, :, 1] = np.power(scaled_grid_0_1[:, :, 1], 2.3)
grid_helpers.grid[:, :, 2] = np.power(scaled_grid_0_1[:, :, 2], 2)
```


## errors 
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