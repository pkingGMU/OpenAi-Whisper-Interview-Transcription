from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained("config.yaml")
diarization = pipeline("test_audio.wav")


for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")