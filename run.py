from audioProcessing import AudioProcessor
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent # current folder absolute path
ap = AudioProcessor()
fileName = "PinkPanter30.wav" # "Recorded_audio.wav"
recordName ="Recorded_audio2.wav"

file_path = os.path.join(BASE_DIR,fileName) # to create absolute path of the wav files to this directory
record_path = os.path.join(BASE_DIR,recordName)
# ap.plot_wav_file(file_path,name=fileName)
res = ap.record_audio(record_path)
ap.plot_wav_file(res,name=recordName)