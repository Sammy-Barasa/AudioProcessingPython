

import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
# import speech_recognition as sr
from cgitb import text
import speech_recognition as sr
import os
import string
import random
from Crypto.Cipher import AES

class AudioProcessor():
    def __init__(self):
        self.FRAMES_PER_BUFFER = 3200
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.seconds = 10
        self.CHUNKS = 1024
    
    def record_audio(self,file_name_to_wav):
        '''
        Record  audio 
        '''
        pa = pyaudio.PyAudio()

        stream = pa.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER
        )

        print('************started recording************************')

        seconds = self.seconds
        frames = [] # list to save recording frames
        time_tracking = 0
        second_count = 0
        
        # decrease counter while recording
        for i in range(0, int(self.RATE/self.FRAMES_PER_BUFFER*seconds)):
            data = stream.read(self.FRAMES_PER_BUFFER)
            frames.append(data)
            time_tracking += 1
            if time_tracking == self.RATE/self.FRAMES_PER_BUFFER:
                second_count += 1
                time_tracking = 0
                print(f'Time Left: {seconds - second_count} seconds')

        # close recording objects
        stream.stop_stream()
        stream.close()
        pa.terminate()
        print('************completed recording************************')
        
        obj = wave.open(file_name_to_wav, 'wb')
        obj.setnchannels(self.CHANNELS)
        obj.setsampwidth(pa.get_sample_size(self.FORMAT))
        obj.setframerate(self.RATE)
        obj.writeframes(b''.join(frames))
        obj.close()
        return file_name_to_wav
    
    def plot_wav_file(self,file_name_wav,name=None):
        '''
        Plot wav file
        '''
        f = wave.open(file_name_wav,'rb')

        sample_rate = f.getframerate()
        frames = f.getnframes()
        channels= f.getnchannels()
        sample_width = f.getsampwidth()
        data = f.readframes(-1)
        

        f.close()
        n= file_name_wav
        if name is not None:
            n = name 
        print(f"completed reading {n}\n")
        time_d = frames / sample_rate

        
        # if one channel use int16, if 2 use int32
        f_type = np.int16
        if channels==2:
            f_type=np.int32
        else:
            f_type = np.int16
             
        audio_array = np.frombuffer(data, dtype=f_type)

        time = np.linspace(0, time_d, num=frames)
       
        
        # Print file properies
        print("-----------------------------------------------------\n")
        print(f"           Properties of {n}               |\n")
        print("-----------------------------------------------------\n")
        print("    Property       |     Value               |\n")
        print("------------------------------------------------------\n")
        print(f" No of channels    |    {channels}                    |\n")
        print("------------------------------------------------------\n")
        print(f" Sample width      |    {sample_width}                    |\n")
        print("------------------------------------------------------\n")
        print(f" Frame/Sample rate |    {sample_rate}                |\n")
        print("------------------------------------------------------\n")
        print(f" No of frames      |    {frames}               |\n")
        print("------------------------------------------------------\n")
        print(f" Duration of audio |    {time_d}s    |\n")
        print("-------------------------------------------------------\n")
        
        
        # Plot
        plt.figure(figsize=(12, 5))
        plt.plot(time, audio_array)
        plt.ylabel('Signal Wave')
        plt.xlabel('Time (s)')
        
        plt.title(f'Plot for {n}')
        plt.show()
        
        return
    
    
    def play_recorded_audio(self,base_dir,file_name):
            '''
            Play recorded audio
            '''
            CHUNK = self.CHUNKS

            file_ = os.path.join(base_dir,file_name)

            wf = wave.open(file_, 'rb')

            # instantiate PyAudio (1)
            p = pyaudio.PyAudio()
            
            # open stream (2)
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            # read data
            data = wf.readframes(CHUNK)

            # play stream (3)
            while len(data) > 0:
                stream.write(data)
                data = wf.readframes(CHUNK)   
            return
        
    def write_text_file(self,base_dir,output_file_name,info):
        out_file_path = os.path.join(base_dir,output_file_name)
        f = open(f"{out_file_path}.txt",'w')
        print("Writing text")
        f.write(info)
        f.close()
        print('Completed writing text to output file ....')
        return
    
    def read_text_file(self,base_dir,input_file):
        file_path = os.path.join(base_dir,input_file)
        file_data = open(file_path,'rb')
        data_out = file_data.read()
        return data_out
    
    def transcribe_audio(self,base_dir,audio_path):
        
        
        r = sr.Recognizer()
        Audio_File = os.path.join(base_dir,audio_path)
        print(Audio_File)
        
        with sr.AudioFile(Audio_File) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
            
            print("Text recovered from the audio is:\n")
            print(text)
            self.write_text_file(base_dir,"Output",text)
            return
        
        
        
    def audio_encrypt(self,base_dir,audio_file):
        # make secret key
        AES_KEY = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))

        AES_IV = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
        
        # save key and vector
        self.write_text_file(base_dir,"AES_KEY",AES_KEY)
        self.write_text_file(base_dir,"AES_IV",AES_IV)
        
        # get the audio
        audio_file_path = os.path.join(base_dir,audio_file,)
        e_audio_file_path = os.path.join(base_dir,'dencrypted_audio_file.wav')
        with open(audio_file_path, 'rb') as filedata:
            audio_contents = filedata.read()
        print(f" Completed reading {audio_file} ...")
        
        # encrypt audio
        encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
        encrypted_audio = encryptor.encrypt(audio_contents)
        print(f" Completed encypting {audio_file} ...")
        
        
        # 
        
        obj = wave.open(e_audio_file_path, 'wb')
        obj.setnchannels(self.CHANNELS)
        obj.setsampwidth(2)
        obj.setframerate(self.RATE)
        obj.writeframes(b''.join(encrypted_audio))
        obj.close()
        print(" Completed saving encrypted_audio_file.wav ...")
        # save encrypted audio
        
        
    def audio_decrypt(self,base_dir,aes_key_file,aes_key_vector):
        
        aes_key = self.read_text_file(base_dir,aes_key_file).decode('ascii')

        aes_v = self.read_text_file(base_dir,aes_key_vector).decode('ascii')

        
        print(aes_key)
        encrypted_audio = os.path.join(base_dir,'encrypted_audio_file.wav')
        decrypted_audio_path = os.path.join(base_dir,'decrypted_audio_file.wav')
        fd=wave.open(encrypted_audio, 'rb')
        encrypted_contents = fd.readframes(-1)
            # print(encrypted_contents)
        
        #  decryptor object
        decryptor = AES.new(aes_key.encode("utf-8"), AES.MODE_CFB, aes_v.encode("utf-8"))
        decrypted_audio = decryptor.decrypt(encrypted_contents)
        
        
        obj = wave.open(decrypted_audio_path, 'wb')
        obj.setnchannels(self.CHANNELS)
        obj.setsampwidth(2)
        obj.setframerate(self.RATE)
        obj.writeframes(b''.join(decrypted_audio))
        obj.close()
        print(" Completed saving decrypted_audio_file.wav ...")
        return 