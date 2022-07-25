from email.policy import default
from audioProcessing import AudioProcessor


def main():
    
    ap = AudioProcessor()
    downloadedWav = "PinkPanther30.wav"
    recorded_fileName = "Recorded_audio.wav" # "Recorded_audio.wav" 
    trancribed_file ='OutputText.txt'
    encrypted_text_file= 'EncryptedText.txt'
    decrypted_txt_file = 'DecryptedText.txt'
    exampleFile ="example.wav"
    hillCypherOutput = "enc_hill.wav.crypt"
    decrypted_audio = "dec_hill.wav"
    
    
  
    while True:
        print("-----------------------------------------------------\n")
        print(f"                 User input options                 |\n")
        print("-----------------------------------------------------\n")
        print("  1   |   Plot downloaded wav file and see parameters|\n")
        print("------------------------------------------------------\n")
        print(f" 2   |   Record an audio                            |\n")
        print("------------------------------------------------------\n")
        print(f" 3   |   Play recorded audio,plot & view properties |\n")
        print("------------------------------------------------------\n")
        print(f" 4   |   Play downloaded audio,plot & view properties |\n")
        print("------------------------------------------------------\n")
        print(f" 5   |   Transcribe recorded audio                  |\n")
        print("------------------------------------------------------\n")
        print(f" 6   |   Encrypt transcribed text                   |\n")
        print("------------------------------------------------------\n")
        print(f" 7   |   Decrypt transcribed text                   |\n")
        print("-------------------------------------------------------\n")
        print(f" 8   |   Decrypt encrypted audio with hillCypher    |\n")
        print("-------------------------------------------------------\n")
        print(f" 9   |   Decrypt decrypted audio with hillCypher    |\n")
        print("-------------------------------------------------------\n")
        print(f" 10  |   Play decrypted audio,plot & view properties|\n")
        print("-------------------------------------------------------\n")
        print(f" 0   |   Exit the application                       |\n")
        print("-------------------------------------------------------\n")
        opt=int(input("Select your option and press <---]: \n"))

        print(f'You chose option: {opt}\n')       
        match opt:
            case 1:
                ap.plot_wav_file(downloadedWav)

            case 2:
                ap.record_audio(recorded_fileName)
                
            case 3:
                ap.play_recorded_audio(recorded_fileName)
                ap.plot_wav_file(recorded_fileName)
            
            case 4:
                ap.play_recorded_audio(downloadedWav)
                
            case 5:
                ap.transcribe_audio(recorded_fileName,trancribed_file)
                
            case 6:
                ap.file_encrypt(trancribed_file,encrypted_text_file)
                
            case 7:
                ap.file_decrypt(encrypted_text_file,decrypted_txt_file)
            case 8:
                ap.encrypt_hillCypher(exampleFile)
            case 9:
                ap.decrypt_hillCypher(hillCypherOutput)
            case 10:
                ap.play_recorded_audio(decrypted_audio)
            case 0:
                print("Exiting ...")
                break 
           
    return

if __name__=="__main__":
    main()