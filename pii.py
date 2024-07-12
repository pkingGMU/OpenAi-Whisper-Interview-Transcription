# Remove PII with PII model
# Imports
import os
import pickle as pk




def remove_pii(txt_file):

    # Read the text file
    #with open(txt_file, 'r') as file:
    #    text = file.read()

    text = 'My name is John Doe and I live in New York. My phone number is 123-456-7890 and my email is bruh@gmail.com'

    with open("pii_model.pkl", "rb") as f:
        model = pk.load(f)

    to_replace = model(text)
    word_list = text.split(' ')

    print(to_replace)
    print(word_list)

    return True

remove_pii("a")