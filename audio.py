# Local Imports
import whisper as wh

# Ask user for ID of patient
patient_id = input('Enter the ID of the patient: ')

# Load the model
audio_model = wh.load_model('tiny')

# Load the audio file
#audio = wh.load_audio('test_audio.mp3')
result1 = audio_model.transcribe('test_audio.mp3')


# TODO: Implement the following code for detecting language and decoding audio
# Convert the audio to a mel spectrogram
#mel = wh.log_mel_spectrogram(audio).to(audio_model.device)

# Detect the spoken language
#_, probs = audio_model.detect_language(mel)
#print(f"Detected language: {max(probs, key=probs.get)}")

# Decode the audio
#options = wh.DecodingOptions()
#result = wh.decode(audio_model, mel, options)



# Write result1['text']  to a txt file naming it the patient_id
with open(patient_id + '.txt', 'w') as f:
    f.write(result1['text'])

print ('Completed')