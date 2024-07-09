from pyannote.audio import Pipeline
from pydub import AudioSegment
import pickle as pk

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

    return new_snips




