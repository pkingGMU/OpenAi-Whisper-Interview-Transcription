## Run diarization.py and then run audio.py and match the output timings of both to create a new with the speaker labels with the transcription output line by line

# Imports
import os
from pyannote.audio import Pipeline
from pydub import AudioSegment
import pickle as pk

# Local Imports
from transcribe import *
from diarization import *
from pii import *





def get_diarization(audio_file):

    #convert audio file from mp3 to wav
    sound = AudioSegment.from_mp3(audio_file)
    sound.export("audio.wav", format="wav")

    #get diarization model
    pipeline = Pipeline.from_pretrained("config.yaml")

    # Load the audio file and run the pipeline
    diarization = pipeline("audio.wav")

    """
    Save the start,end,and speaker (in order) for the snipping
    and ordering. It will be inside 2D tuple so the snips are ordered.
    """

    audio = AudioSegment.from_wav("audio.wav")
    snips = []
    audio_snips = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        snip = (turn.start,turn.end,speaker)
        snips.append(snip)

        #pydub works in miliseconds
        audio_snips = audio[(snip[0]*1000):(snip[1]*1000)]

    return audio_snips

def get_consolidated_audio_snips(snips):
    new_snips = []

    current_speaker = snips[0][2]
    start_index = 0

    for i in range(len(snips)):

        # loop from the starting index till a different speaker than the current is found
        if snips[i][2] != current_speaker:
            """ 
            once a different speaker than the current is found add a tuple consisting of start time
            of the snip at the starting index, till the end time of last snip to have the same speaker as start index
            (before the change), and finally have the speaker who spoke.
            """
            new_snips.append((snips[start_index][0], snips[i - 1][1], snips[start_index][2]))


            # update start index and current speaker.
            start_index = i
            current_speaker = snips[i][2]

    # Map turn.start value to the closest value in our transcription object



    return new_snips

def combine_diar_transcript(diarization_data, transcription_data):
    aligned_text = []

    # Iterate over diarization segments
    for diarization_segment in diarization_data:
        speaker = diarization_segment["speaker"]
        start_time = diarization_segment["start_time"]
        end_time = diarization_segment["end_time"]

        # Find corresponding text segment from transcription
        matched_text = ""
        for transcript_segment in transcription_data:
            if transcript_segment["end_time"] >= start_time - .1 and transcript_segment["start_time"] <= end_time +.1:
                matched_text += transcript_segment["text"] + " "
                transcription_data.remove(transcript_segment)
                

        # Append speaker and matched text to aligned output
        aligned_text.append(f"Speaker {speaker}: {matched_text.strip()}")
        
        print (transcription_data)

    return aligned_text

def combine_diar_transcript2(diarization_data, transcription_data):
    deidentified_aligned_text = []
    aligned_text = []

    for transcript_segment in transcription_data:
        start_time = transcript_segment["start_time"]
        end_time = transcript_segment["end_time"]


        # Find corresponding diarization
        for diarization_segment in diarization_data:
            matched_text = ""
            if end_time >= diarization_segment["start_time"] - .1 and start_time <= diarization_segment["end_time"] + .1:
                matched_text += transcript_segment["text"] + " "
                
                # Append speaker and matched text to aligned output
                speaker = diarization_segment["speaker"]
                d_start_time = round(diarization_segment["start_time"], 0)
                d_end_time = round(diarization_segment["end_time"], 0)
                # Remove PII with PII model
                deidentified_aligned_text.append(f"{speaker} \n({d_start_time},{d_end_time}): {remove_pii(matched_text.strip())}")
                aligned_text.append(f"{speaker} \n({d_start_time},{d_end_time}): {matched_text.strip()}")
                break


    return deidentified_aligned_text, aligned_text


def main():

    ## TODO: Some easy way to select files without using a file explorer
    # Have user input the file name and get the path from the input
    # Ask user for patient ID
    patient_id = input('Enter the name of the patient: ')

    # Get the path of the file by searching a specific directory
    ## TODO: Change root folder to cyberduck
    root = os.path.dirname(os.path.abspath(__file__))


    for folder in os.listdir(root):
        print(folder)

        if folder == patient_id:
            file_path = os.path.join(root, folder)
            break
        else:
            file_path = 'Didnt find the folder'

    for file in os.listdir(file_path):
        print(file)

        if file.endswith('.mp3'):
            audio_file = os.path.join(file_path, file)
            break
        else:
            audio_file = 'Didnt find the file'

    print (audio_file)

    ## Convert mp3 file to wav using audio_file path if there is no wav file created
    temp_file_name = file.split('.')[0]
    wav_file_path = os.path.join(file_path, temp_file_name+'.wav')

    if not any(file.endswith('.wav') for file in os.listdir(file_path)):    
        sound = AudioSegment.from_mp3(audio_file)
        sound.export(wav_file_path, format="wav")


    print(wav_file_path)
    
    ## Transcription

    #transcription_data = transcribe_audio(wav_file_path)

    ### DO NOT DELETE THIS IS WHAT WILL ACTUALLY RUN THE TRANSCRIPTION
    ########transcription_data = transcribe_audio(wav_file_path)
    with open("transcription_data.pkl","rb") as f:
        transcription_data = pk.load(f)

    #print (transcription_data)

    ## Diarization

    ### DO NOT DELETE THIS IS WHAT WILL ACTUALLY RUN THE DIARIZATION
    #######diarization_data = diarization_task(wav_file_path)
    with open("diarization_data.pkl","rb") as f:
        diarization_data = pk.load(f)
    #print(diarization_data)


    # Get allignment segments from combination
    deidentified_aligned_text, aligned_segments = combine_diar_transcript2(diarization_data, transcription_data)
    #print(aligned_segments)


    # Write txt file with allignmed segments
    output_folder = file_path
    output_filename_identifiable = os.path.join(output_folder, patient_id + "_raw_transcription"+ ".txt")
    output_filename_DE_ID = os.path.join(output_folder, patient_id + "_raw_transcription_DE"+ ".txt")
    
    with open(output_filename_identifiable, "w") as f:
        for segment in aligned_segments:
            f.write(segment + "\n")

    with open(output_filename_DE_ID, "w") as f:
        for segment in deidentified_aligned_text:
            f.write(segment + "\n")



# Load the diarization model

if __name__ == '__main__':
    main()
