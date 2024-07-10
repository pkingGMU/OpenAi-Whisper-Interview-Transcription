## Run diarization.py and then run audio.py and match the output timings of both to create a new with the speaker labels with the transcription output line by line

# Imports
import os
from pyannote.audio import Pipeline
from pydub import AudioSegment
#import pickle as pk



## Convert mp3 file to wav using audio_file path if there is no wav file created
if not any(file.endswith('.wav') for file in os.listdir(file_path)):    
    sound = AudioSegment.from_mp3(audio_file)
    temp_file_name = file.split('.')[0]
    temp_file_path = os.path.join(file_path, temp_file_name+'.wav')
    sound.export(temp_file_path, format="wav")



## TODO: Run diarization.py as a function


## TODO: Run audio.py as a function

## TODO: Match the output of both functions line by line

# Load the diarization model

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
            if transcript_segment["end_time"] >= start_time and transcript_segment["start_time"] <= end_time:
                matched_text += transcript_segment["text"] + " "

        # Append speaker and matched text to aligned output
        aligned_text.append(f"Speaker {speaker}: {matched_text.strip()}")

    return aligned_text

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

    # Test combination
    transcription_data = [
    {"text": "Hello, how are you?", "start_time": 0.0, "end_time": 1.5},
    {"text": "I'm good, thank you.", "start_time": 2.0, "end_time": 4.0},
    {"text": "Nice weather today.", "start_time": 5.0, "end_time": 6.5},
    ]

    diarization_data = [
    {"speaker": "A", "start_time": 0.0, "end_time": 1.0},
    {"speaker": "B", "start_time": 2.0, "end_time": 3.5},
    {"speaker": "A", "start_time": 5.0, "end_time": 6.0},
    ]

    # Example usage
    aligned_segments = combine_diar_transcript(diarization_data, transcription_data)
    print (aligned_segments)

    # Output to TXT file
    output_filename = "aligned_output.txt"
    with open(output_filename, "w") as f:
        for segment in aligned_segments:
            f.write(segment + "\n")



## TODO: Run diarization.py as a function


## TODO: Run audio.py as a function

## TODO: Match the output of both functions line by line

# Load the diarization model

if __name__ == '__main__':
    main()
