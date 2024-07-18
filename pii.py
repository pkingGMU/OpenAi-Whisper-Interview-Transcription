# Remove PII with PII model
# Imports

import pickle as pk
import os
import pickle as pk
import re



def remove_pii(text):

    with open("pii_model.pkl", "rb") as f:
        model = pk.load(f)

    to_replace = model(text)

    replacement_dict = {}
    punctuation = [",","-",".","?","!"]
    text = text.lower()


    for replacement in to_replace:
        if replacement["word"] in punctuation:
            continue

        if replacement["word"] not in replacement_dict.keys():

            replacement_dict[replacement["word"]] = replacement["entity"].split("-")[1]

    for key, value in replacement_dict.items():
        text = text.replace(key,value)


    #get rid of straggling numbers
    labels = list(set(replacement_dict.values()))

    cleaned_text = text
    for label in labels:

        pattern = r'(?<=\b(' + label + r'))\d+'
        cleaned_text = re.sub(pattern, '', cleaned_text)

        pattern = r'(?<=\b(' + label + r'))\S+'
        #cleaned_text = re.sub(pattern, '', cleaned_text)
    return cleaned_text

