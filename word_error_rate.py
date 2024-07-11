# Calculate word error rate (WER) between original transcription and processed transcription

# Import
import jiwer


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

# Test
# Original transcription
original = "hello world how are you"

# Processed transcription
processed = "hello worl how are you doing today"

calc_word_error_rate(original, processed)