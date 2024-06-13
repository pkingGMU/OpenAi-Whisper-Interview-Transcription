# Local Imports
import whisper as wh
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

# Allow user to select audio file from directory with file dialog
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()



# Ask user for ID of patient
patient_id = input('Enter the ID of the patient: ')

# Load the model
audio_model = wh.load_model('tiny')


# Load the audio file
audio = wh.load_audio(file_path)

# Convert the audio to a mel spectrogram
#mel = wh.log_mel_spectrogram(audio).to(audio_model.device)

# Detect the spoken language
#_, probs = audio_model.detect_language(mel)
#detected_language = max(probs, key=probs.get)
#print(f"Detected language: {detected_language}")

# Transcribe the audio 
# Using fp32 since my Mac doesn't have a gpu
result1 = audio_model.transcribe(file_path, fp16=False)

# Extract language from the transcription
detected_language = result1['language']


# TODO: Seperate speaker from text object


# TODO: Implement the following code for detecting language and decoding audio


# Decode the audio
#options = wh.DecodingOptions()
#result = wh.decode(audio_model, mel, options)



# Write result1['text']  to a txt file naming it the patient_id
with open('MI#' + patient_id + detected_language +'.txt', 'w') as f:
    f.write(result1['text'])


## TODO: Implement a system to upload the txt file to a server so it never gets stored locally




print ('Completed')