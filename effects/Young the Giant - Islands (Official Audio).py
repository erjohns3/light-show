import numpy as np
import sys

from effects.compiler import *


effects = {
    "specto young": {
        "length": 1,
        "beats": [
            grid_f(1, function=grid_visualizer, color=(0, 255, 0), song_path='songs/Young the Giant - Islands (Official Audio).ogg', grid_skip_top_fill=True, length=1),
        ],
    },


    "Young the Giant - Islands (Official Audio)": {
        "bpm": 124,
        "song_path": "songs/Young the Giant - Islands (Official Audio).ogg",
        "delay_lights": 0.3598709677419355,
        "skip_song": 0.0,
        "beats": [
            grid_f(1, function=grid_visualizer, color=(0, 255, 0), song_path='songs/Young the Giant - Islands (Official Audio).ogg', grid_skip_top_fill=True, length=100),
        ],
    }
}

# chatgpt prompt
# ```
#  librosa.feature.melspectrogram(*, y=None, sr=22050, S=None, n_fft=2048, hop_length=512, win_length=None, window='hann', center=True, pad_mode='constant', power=2.0, **kwargs)[source]

#     Compute a mel-scaled spectrogram.

#     If a spectrogram input S is provided, then it is mapped directly onto the mel basis by mel_f.dot(S).

#     If a time-series input y, sr is provided, then its magnitude spectrogram S is first computed, and then mapped onto the mel scale by mel_f.dot(S**power).

#     By default, power=2 operates on a power spectrum.

#     Parameters:

#         ynp.ndarray [shape=(…, n)] or None

#             audio time-series. Multi-channel is supported.
#         srnumber > 0 [scalar]

#             sampling rate of y
#         Snp.ndarray [shape=(…, d, t)]

#             spectrogram
#         n_fftint > 0 [scalar]

#             length of the FFT window
#         hop_lengthint > 0 [scalar]

#             number of samples between successive frames. See librosa.stft
#         win_lengthint <= n_fft [scalar]

#             Each frame of audio is windowed by window(). The window will be of length win_length and then padded with zeros to match n_fft. If unspecified, defaults to win_length = n_fft.
#         windowstring, tuple, number, function, or np.ndarray [shape=(n_fft,)]

#                 a window specification (string, tuple, or number); see scipy.signal.get_window

#                 a window function, such as scipy.signal.windows.hann

#                 a vector or array of length n_fft

#         centerboolean

#                 If True, the signal y is padded so that frame t is centered at y[t * hop_length].

#                 If False, then frame t begins at y[t * hop_length]

#         pad_modestring

#             If center=True, the padding mode to use at the edges of the signal. By default, STFT uses zero padding.
#         powerfloat > 0 [scalar]

#             Exponent for the magnitude melspectrogram. e.g., 1 for energy, 2 for power, etc.
#         **kwargsadditional keyword arguments for Mel filter bank parameters
#         n_melsint > 0 [scalar]

#             number of Mel bands to generate
#         fminfloat >= 0 [scalar]

#             lowest frequency (in Hz)
#         fmaxfloat >= 0 [scalar]

#             highest frequency (in Hz). If None, use fmax = sr / 2.0
#         htkbool [scalar]

#             use HTK formula instead of Slaney
#         norm{None, ‘slaney’, or number} [scalar]

#             If ‘slaney’, divide the triangular mel weights by the width of the mel band (area normalization). If numeric, use librosa.util.normalize to normalize each filter by to unit l_p norm. See librosa.util.normalize for a full description of supported norm values (including +-np.inf). Otherwise, leave all the triangles aiming for a peak value of 1.0
#         dtypenp.dtype

#             The data type of the output basis. By default, uses 32-bit (single-precision) floating point.

#     Returns:

#         Snp.ndarray [shape=(…, n_mels, t)]

#             Mel spectrogram
# ```

# write me a python function to output a 2d array representing the audio from an ogg filepath using librosa. the first dimensions index will represent a 1/48th of a second. The second dimension will be 32 long (index 0 is bass, index 31 is treble), and the elements will be between 0 and 19. This 0 to 19 value will represent how intense the audio is at that frequency. my sample rate for audio is 48000.


# def get_whole_spectogram(filepath, size=(20, 32)):
#     global spectogram_cache
#     the_hash = (filepath, size)
#     if the_hash not in spectogram_cache:
#         import librosa
#         from scipy.ndimage import zoom

#         y, sr = librosa.load(filepath)
#         print(librosa.feature.melspectrogram)
#         spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
#         log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
#         normalized_spectrogram = ((log_spectrogram - np.min(log_spectrogram)) / 
#                                   (np.max(log_spectrogram) - np.min(log_spectrogram))) * 255
#         resized_spectrogram = zoom(normalized_spectrogram, 
#                                    (size[0]/normalized_spectrogram.shape[0], 
#                                    size[1]/normalized_spectrogram.shape[1])).astype(int)
#         spectogram_cache[the_hash] = resized_spectrogram
#     return spectogram_cache[the_hash]