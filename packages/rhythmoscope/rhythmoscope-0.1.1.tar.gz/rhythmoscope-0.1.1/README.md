# RhythmoScope - Speech Rhythm Modulation Spectrum 

 RhythmoScope is a Python library for automatic speech rhythm modelisation. This project rely on the Envelope Modulation Spectrum (EMS) for analysing the main regularities of speech at different levels. This library is the result of my PhD thesis under the supervision of <a href="https://lnpl.univ-tlse2.fr/accueil/membres/corine-astesano-1">Corine Astésano</a> and <a href="https://www.irit.fr/~Jerome.Farinas/">Jérôme Farinas</a>. 


## 🛠 Installation

Rhythmoscope should work with Python 3.9 and above. The library can be installed through the following `pip` command:

```sh
pip install rhythmoscope
```
## 🔬 Basic usage

### EMS

As an example, we'll extract and plot the EMS of a speech signal from a .wav file (examples wav files can be found in `/examples/audios`):

```python
from rhythmoscope.ems import EMSExtractor
from rhythmoscope.envelope import LowPassEnvelope

Envelope = LowPassEnvelope(cut_frequency=10, order=3, initial_bandpass=(300, 1000)) # Define envelope extractor
Extractor = EMSExtractor(Envelope=Envelope, min_freq=0, max_freq=10) # Define EMS extractor parameters

EMS = Extractor.from_file("example.wav", start=0, end=4) # Extract EMS on the first 4 seconds of the audio

fig = EMS.plot()
fig.show()
```

It produce the following output which represent the Envelope Modulation Spectrum of a signal (examples wav files can be found in `/examples/audios`):

<div align="center">
    <img src="docs/img/EMS_example.png" alt="EMS_example" width="90%" vspace="5">
</div>

### Rhythm spectrogram

```python
from rhythmoscope.ems import EMSExtractor
from rhythmoscope.signal import RollingWindow
from rhythmoscope.spectrogram import RhythmSpectrogramExtractor

EMS = EMSExtractor(min_freq=0, max_freq=15) # Define EMS extractor parameters
Window = RollingWindow(window_size=3, hop_size=0.5) # Define parameters of the spectrogram rolling window (in seconds)

SpectroExtract = RhythmSpectrogramExtractor(EMS, Window) # Define Spectrogram extractore parameters
spectrogram = SpectroExtract.from_file("count.wav") # Extract spectrogram

fig = spectrogram.plot()
fig.show()
```

It produce the following output which represent the Rhythm Spectrogram of a signal:

<div align="center">
    <img src="docs/img/spectro.png" alt="Spectrogram_example" width="70%" vspace="5">
</div>

Each red line correspond to a regular rhythm at a given time. The rhythmic evolution in this example comes from the fact that the words spoken are mono-syllabic in the first half and bi-syllabic in the second.

## 🔗 Related work

- [Rhythm Formant Analysis](https://github.com/dafyddg/RFA) from Dafydd Gibbon
- [Temporal Modulation Spectrum Toolbox](https://github.com/LeoVarnet/TMST) (Matlab code) from Léo Varnet 

## 💬 Citation

If RhythmoScope has been useful to you, and you would like to cite, please refer to my PhD thesis:

```bibtex
@phdthesis{vaysse2023thesis,
  TITLE = {{Caract{\'e}risation automatique du rythme de la parole : application aux cancers des voies a{\'e}ro-digestives sup{\'e}rieures et {\`a} la maladie de Parkinson}},
  AUTHOR = {Vaysse, Robin},
  URL = {https://theses.hal.science/tel-04198849},
  NUMBER = {2023TOU30062},
  SCHOOL = {{Universit{\'e} Paul Sabatier - Toulouse III}},
  YEAR = {2023},
  MONTH = Mar,
  TYPE = {Theses},
  PDF = {https://theses.hal.science/tel-04198849/file/2023TOU30062b.pdf},
  HAL_ID = {tel-04198849},
  HAL_VERSION = {v1},
}
```

## 📝 License

RhythmoScope is a free and open-source software licensed under the [3-clause BSD license](https://github.com/VaysseRobin/RhythmoScope/blob/main/LICENSE).
