# Using pyannote.audio for diarization
# This will give timestamps that will be used to transcribe with audio.py

# Imports
from pyannote.core import Annotation

# Load RTTM file into a pyannote Annotation object
annotation = Annotation.extrude("audio.rttm")

# Visualize speaker turns
annotation.plot()

# Evaluate diarization performance against ground truth (if available)
# Assuming reference_rttm is the ground truth RTTM file
reference_annotation = Annotation.from_rttm("reference.rttm")
der = annotation.diarization_error_rate(reference_annotation)
print(f"DER: {der}")

# Access segments programmatically
for segment in annotation.itersegments():
    start, end, speaker = segment.start, segment.end, segment.track.label
    print(f"Speaker {speaker}: start={start:.2f}s, end={end:.2f}s")