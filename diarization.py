# Imports
from pyannote.audio import Pipeline
import onnxruntime
import pickle as pk

def diarization_task(audio_file):

    # Load the diarization model
    pipeline = Pipeline.from_pretrained("config.yaml")
    # Load the audio file and run the pipeline
    diarization = pipeline(audio_file)

    #print (f'{diarization}')

    """ 
   # Assuming your pickle file is named 'data.pickle'
    pickle_file_path = 'diarization.pkl'

    # Step 1: Open the pickle file in binary read mode
    with open(pickle_file_path, 'rb') as f:
    # Step 2: Load the data from the pickle file
        diarization = pk.load(f)
    """

    diarization_segments = []
    #Print to terminal for testing
    for turn, _, speaker in diarization.itertracks(yield_label=True):

        diarization_segments.append({
            "start_time": turn.start,
            "end_time": turn.end,
            "speaker": speaker
        })

    return diarization_segments
        #print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
    
    