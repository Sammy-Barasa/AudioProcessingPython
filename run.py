from audioProcessing import AudioProcessor
import os
from pathlib import Path

def main():
    BASE_DIR = Path(__file__).resolve().parent # current folder absolute path
    ap = AudioProcessor()
    fileName = "Recorded_audio.wav" # "Recorded_audio.wav" "PinkPanther30.wav"
    recordName ="Recorded_audio2.wav"

    file_path = os.path.join(BASE_DIR,fileName) # to create absolute path of the wav files to this directory
    record_path = os.path.join(BASE_DIR,recordName)
    ap.plot_wav_file(file_path,name=fileName)
    
    # record an audio
    # res = ap.record_audio(record_path)
    # ap.plot_wav_file(res,name=recordName)
    ap.play_recorded_audio(BASE_DIR,recordName)
    
    # transcribe audio
    
    # ap.transcribe_audio(BASE_DIR,recordName)
    # encrypt audio
    # ap.audio_encrypt(BASE_DIR,recordName)
    # ap.play_recorded_audio(BASE_DIR,"encrypted_audio_file.wav") dont play since it is not wav
    
    # ap.audio_decrypt(BASE_DIR,"AES_KEY.txt","AES_IV.txt")
    # decrypt audio
    
    # ap.audio_encrypt(BASE_DIR,"dencrypted_audio_file.wav")
    
    # play decrepted audio
    ap.play_recorded_audio(BASE_DIR,"decrypted_audio_file.wav")
    return

if __name__=="__main__":
    main()