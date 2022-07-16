
import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np

class AudioProcessor():
    def __init__(self):
        self.FRAMES_PER_BUFFER = 3200
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 16000
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
        data = f.readframes(-1)
        

        f.close()
        n= name or file_name_wav
        print(f"completed reading {n}")
        time_d = frames / sample_rate

        print(f"Channels: {channels}")
        # if one channel use int16, if 2 use int32
        f_type = np.int16
        if channels==2:
            f_type=np.int32
        else:
            f_type = np.int16
             
        audio_array = np.frombuffer(data, dtype=f_type)

        time = np.linspace(0, time_d, num=frames)
        print(time)
        
        # Print file properies
        print("-----------------------------------------------------\n")
        print("    Property       |     Value               |\n")
        print("------------------------------------------------------\n")
        print(f" No of channels    |    {channels}                    |\n")
        print("------------------------------------------------------\n")
        print(f" Frame/Sample rate |    {sample_rate}                |\n")
        print("------------------------------------------------------\n")
        print(f" No of frames      |    {frames}               |\n")
        print("------------------------------------------------------\n")
        print(f" Duration of audio |    {time_d}    |\n")
        print("-------------------------------------------------------\n")
        
        # Plot
        plt.figure(figsize=(15, 5))
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

            file_ = file_name

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
   