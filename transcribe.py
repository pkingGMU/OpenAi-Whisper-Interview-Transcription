# Local Imports
import whisper as wh


def transcribe_audio(audio):
    # Allow user to select audio file from directory with file dialog
    

    # Load the model
    audio_model = wh.load_model('small')


    # Load the audio file
    audio = wh.load_audio(audio)

    # Convert the audio to a mel spectrogram
    #mel = wh.log_mel_spectrogram(audio).to(audio_model.device)

    # Detect the spoken language
    #_, probs = audio_model.detect_language(mel)
    #detected_language = max(probs, key=probs.get)
    #print(f"Detected language: {detected_language}")

    # Transcribe the audio 
    # Using fp32 since my Mac doesn't have a gpu
    result1 = audio_model.transcribe(audio, fp16=False)

    # Extract language from the transcription
    detected_language = result1['language']



    # TODO: Seperate speaker from text object
    


    # TODO: Implement the following code for detecting language and decoding audio


    # Decode the audio
    #options = wh.DecodingOptions()
    #result = wh.decode(audio_model, mel, options)



    # Write result1['text']  to a txt file naming it the patient_id
    #with open('MI#' + patient_id + detected_language +'.txt', 'w') as f:
    #    f.write(result1['text'])
    ## TODO: Implement a system to upload the txt file to a server so it never gets stored locally
    print ('Completed')

    transcription_data = []


    for segment in result1['segments']:
        transcription_data.append({
            "text": segment["text"],
            "start_time": segment["start"],
            "end_time": segment["end"]
    })

    return transcription_data