import ast
import string
import sys

def remove_punctuation(sentence):
    translator = str.maketrans('', '', string.punctuation.replace("'", ""))
    cleaned_init = sentence.translate(translator)
    return cleaned_init.lower()

def calculate(original, transcription):
    # Open original text
    with open(original, 'r') as file:
        file_contents = file.read()
    original_text = ast.literal_eval(file_contents)

    # Open transcription text
    with open(transcription, 'r') as file:
        file_contents = file.read()
    transcription_text = ast.literal_eval(file_contents)

    # Remove punctuations
    clean_original = [remove_punctuation(sentence) for sentence in original_text]
    clean_transcription = [remove_punctuation(sentence) for sentence in transcription_text]

    # Perform further calculations or comparisons as needed
    print("done")
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <path_to_original_file> <path_to_transcription_file>")
        sys.exit(1)

    original_file_path = sys.argv[1]
    transcription_file_path = sys.argv[2]

    calculate(original_file_path, transcription_file_path)
