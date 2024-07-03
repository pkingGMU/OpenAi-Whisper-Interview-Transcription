# Imports
from pyannote.audio import Pipeline


# Load the diarization model
pipeline = Pipeline.from_pretrained("config.yaml")
# Load the audio file and run the pipeline
diarization = pipeline("test_audio.wav")

print (f'{diarization}')

# Print to terminal for testing
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")