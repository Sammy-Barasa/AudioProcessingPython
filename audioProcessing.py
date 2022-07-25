

import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
from cgitb import text
import speech_recognition as sr
import os
import string
import random
from Crypto.Cipher import AES
from sympy.crypto.crypto import encipher_hill, decipher_hill
from cryptography.fernet import Fernet
from sympy import Matrix

class AudioProcessor():
    def __init__(self):
        self.FRAMES_PER_BUFFER = 3200
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 16000
        self.seconds = 10
        self.CHUNKS = 1024
        self.BASE_DIR = Path(__file__).resolve().parent # current folder absolute path
        self.key = Matrix([[1,]]) # hillcypher encrption key
    
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
            if time_tracking == (self.RATE)/(self.FRAMES_PER_BUFFER):
                second_count += 1
                time_tracking = 0
                print(f'Time Left: {seconds - second_count} seconds')

        # close recording objects
        stream.stop_stream()
        stream.close()
        pa.terminate()
        print('************completed recording************************')
        
        obj = wave.open(os.path.join(self.BASE_DIR,file_name_to_wav), 'wb')
        obj.setnchannels(self.CHANNELS)
        obj.setsampwidth(pa.get_sample_size(self.FORMAT))
        obj.setframerate(self.RATE)
        obj.writeframes(b''.join(frames))
        obj.close()
        print("Recordingwas successfull .....\n")
        return file_name_to_wav
    
    def plot_wav_file(self,file_name_wav,name=None):
        '''
        Plot wav file
        '''
        f = wave.open(os.path.join(self.BASE_DIR,file_name_wav),'rb')

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
        print(f" Frame values      |    {audio_array}|\n")
        print("-------------------------------------------------------\n")
        
        
        # Plot
        plt.figure(figsize=(12, 5))
        plt.plot(time, audio_array)
        plt.ylabel('Signal Wave')
        plt.xlabel('Time (s)')
        
        plt.title(f'Plot for {n}')
        plt.show()
        
        return
    
    
    def play_recorded_audio(self,file_name):
            '''
            Play recorded audio
            '''
            CHUNK = self.CHUNKS

            file_ = os.path.join(self.BASE_DIR,file_name)

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
        
    def write_text_file(self,output_file_name,info):
        out_file_path = os.path.join(self.BASE_DIR,output_file_name)
        f = open(f"{out_file_path}",'w')
        print("Writing text")
        f.write(info)
        f.close()
        print('Completed writing text to output file ....')
        return
    
    def read_text_file(self,input_file):
        file_path = os.path.join(self.BASE_DIR,input_file)
        file_data = open(file_path,'rb')
        data_out = file_data.read()
        return data_out
    
    def transcribe_audio(self,audio_path,out_put_text_file):
        
        
        r = sr.Recognizer()
        Audio_File = os.path.join(self.BASE_DIR,audio_path)
        print(Audio_File)
        
        with sr.AudioFile(Audio_File) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
            
            print("Text recovered from the audio is:\n")
            print(f"\033[1;36m {text}")
            self.write_text_file(out_put_text_file,text)
            return        
        
    def file_encrypt(self,transcribed_file,encrypted_text_file):

        # generate encryption key
        key = Fernet.generate_key()
        # write the encryption key to a file called fileKey.key
        file_key = open(os.path.join(self.BASE_DIR,'Key_file.key'),'wb')
        file_key.write(key)
        
        file_key = open(os.path.join(self.BASE_DIR,'Key_file.key'),'rb')
        key = file_key.read()

        # use generated key
        fernet = Fernet(key)
        
        #open original text file for encryption.
        file = open(os.path.join(self.BASE_DIR,transcribed_file))
        original = file.read()

        # covert text file to bytes for encryption
        original_bytes = original.encode()

        #encrypt the file
        encrypt_file = fernet.encrypt(original_bytes)

        # write encrypted data to a text file.
        encrypted_text = open(os.path.join(self.BASE_DIR,encrypted_text_file),'wb')
        encrypted_text.write(encrypt_file)
        

    
    def file_decrypt(self,encrypted_text_file,decrypted_txt_file):
         #decrypt file and store in a different text file
        enc_file = open(os.path.join(self.BASE_DIR,encrypted_text_file),'rb')
        encrypted_data = enc_file.read()
        file_key = open(os.path.join(self.BASE_DIR,'Key_file.key'),'rb')
        key = file_key.read()
        fernet = Fernet(key)

        decrypted_data = fernet.decrypt(encrypted_data)
        with open(os.path.join(self.BASE_DIR,decrypted_txt_file),'wb') as dec_text:
            # decrypt_message = decrypted_data.decode()
            dec_text.write(decrypted_data)
            
    
    def encrypt_hillCypher(self,file_wav):
        
        with open(os.path.join(self.BASE_DIR,file_wav), "rb") as f:
            x = f.read().hex()

        key=self.key

        # Encryption
        print("Encrypting .... ")
        ciphertext = ""
        for i in x:
            if i.isalpha():
                ciphertext+=encipher_hill(i,key)
            else:
                ciphertext+=i
                
        print("Completed Encrypting ..... ")
        print(type(ciphertext))
        print(len(ciphertext))
        with open(os.path.join(self.BASE_DIR,"enc_hill.wav.crypt"), "w") as f:
            f.write(ciphertext)

        print("Encrypted File Completed")
    
    def decrypt_hillCypher(self,encrypted_file):
        print("Starting Decryption .... ")
        # Decryption
        with open(os.path.join(self.BASE_DIR,"enc_hill.wav.crypt"), "r") as f:
            ciphertext=f.read()
        
        print(len(ciphertext))
        pt = ""
        for i in ciphertext:
            if i.isalpha():
                pt+=decipher_hill(i,self.key)
            else:
                pt+=i

        with open(os.path.join(self.BASE_DIR,"dec_hill.wav"), "wb") as f:
            f.write(bytes().fromhex(pt))
        print("Completed Decryption")
        print("--------------------------------------------")

    def audio_encrypt(self,audio_file):
        # make secret key
        AES_KEY = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))

        AES_IV = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
        
        # save key and vector
        self.write_text_file("AES_KEY",AES_KEY)
        self.write_text_file("AES_IV",AES_IV)
        
        # get the audio
        audio_file_path = os.path.join(self.BASE_DIR,audio_file,)
        e_audio_file_path = os.path.join(self.BASE_DIR,'encrypted_audio_file.wav')
        with open(audio_file_path, 'rb') as filedata:
            audio_contents = filedata.read()
        print(f" Completed reading {audio_file} ...")
        
        # encrypt audio
        encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
        encrypted_audio = encryptor.encrypt(audio_contents) # type bytes result
        print(f" Completed encypting {audio_file} ...")
        
        print("encrypted audio is of type: ",type(encrypted_audio))
        # save encrypted audio
        
        obj = wave.open(e_audio_file_path, 'wb')
        obj.setnchannels(self.CHANNELS)
        obj.setsampwidth(2)
        obj.setframerate(self.RATE)
        obj.writeframes(''.join(encrypted_audio).encode('utf-8') + '\n') # joining the list of byte string
        obj.close()
        print(" Completed saving encrypted_audio_file.wav ...")
        # completed saving encrypted audio
        return
        
        
    def audio_decrypt(self,aes_key_file,aes_key_vector):
        
        aes_key = self.read_text_file(aes_key_file).decode('ascii')

        aes_v = self.read_text_file(aes_key_vector).decode('ascii')

        
        print(aes_key)
        encrypted_audio = os.path.join(self.BASE_DIR,'encrypted_audio_file.wav')
        decrypted_audio_path = os.path.join(self.BASE_DIR,'decrypted_audio_file.wav')
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