# Calculate word error rate (WER) between original transcription and processed transcription

# Import
import jiwer
import os


def calc_word_error_rate(original, processed):
    
    # Jiwer Transpose parametersa
    transforms = jiwer.Compose(
        [
            jiwer.ExpandCommonEnglishContractions(),
            jiwer.RemoveEmptyStrings(),
            jiwer.ToLowerCase(),
            jiwer.RemoveMultipleSpaces(),
            jiwer.Strip(),
            jiwer.RemovePunctuation(),
            jiwer.ReduceToListOfListOfWords(),
        ]
    )

    # Reference
    reference = original

    # Hypothesis
    hypothesis = processed



    # Calculate WER
    wer = jiwer.wer(
                reference,
                hypothesis,
                truth_transform=transforms,
                hypothesis_transform=transforms,
            )
    print(f"Word Error Rate (WER) :", wer)


def main ():
   
    # Ask user for subject this wish to compare error rate
    subject = input("Enter the subject ID: ")

    # Path for root
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Path for subject raw
    original_path = os.path.join(root, 'output', subject, 'LE_12_raw_transcription_DE.txt')

    with open (original_path, 'r') as f:
        original = f.read()
    print (original_path)

    # Path for subject processed
    processed_path = os.path.join(root, 'output', subject, 'LE_12_processed_transcription_DE.txt')

    with open (processed_path, 'r') as f:
        processed = (f.read())
    print (processed_path)


    calc_word_error_rate(original, processed)

if __name__ == "__main__":
    main()