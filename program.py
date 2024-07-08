## Run diarization.py and then run audio.py and match the output timings of both to create a new with the speaker labels with the transcription output line by line

# Imports
import os



## TODO: Some easy way to select files without using a file explorer
# Have user input the file name and get the path from the input
# Ask user for patient ID
patient_id = input('Enter the name of the patient: ') + '.wav'

# Get the path of the file by searching a specific directory
## TODO: Change root folder to cyberduck
root = r"/Users/patrick/Git Hub/Deep-Speech-Mac-Test/"

for file in os.listdir(root):
    

    print(file)

    if file == patient_id:
        file_path = os.path.join(root, file)
        break
    else:
        file_path = 'Didnt find the file'

print (file_path)


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