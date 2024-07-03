## Run diarization.py and then run audio.py and match the output timings of both to create a new with the speaker labels with the transcription output line by line

## TODO: Run diarization.py as a function

## TODO: Run audio.py as a function

## TODO: Match the output of both functions line by line


time_range_text_dict = {}
# Loop over each turn (segment) in the diarization to fill in values in the dictionary
for turn in diarization:
    # Get the speaker label
    speaker = turn.track("speaker").label()
    # Get the start and end time of the turn
    start = turn.start
    end = turn.end

    # Map turn.start value to the closest value in our transcription object
    

    # Concatanate the start time and end time to create a range
    time_range = f"{start} - {end}"
    time_range_text_dict[time_range] = [speaker, text]




## TODO: Open a new txt file and write the output of both functions line by line