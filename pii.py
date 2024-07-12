# Remove PII with PII model
# Imports

import pickle as pk
import os
import pickle as pk




def remove_pii(txt_file):

    # Read the text file
    #with open(txt_file, 'r') as file:
    #    text = file.read()

    text = """
    He is John Doe, who lives at 1234 Elm Street, Springfield, USA, is a software engineer at TechCorp Inc. His email address is john.doe@example.com, and his phone number is 555-123-4567. John’s date of birth is April 15, 1985, and his social security number is 987-65-4321. In his free time, John enjoys hiking and photography. He frequently shops at SuperMart and often uses his credit card ending in 1234 for purchases.
    """

    with open("pii_model.pkl", "rb") as f:
        model = pk.load(f)

    to_replace = model(text)

    replacement_dict = {}
    punctuation = [",","-",".","?","!"]
    text = text.lower()


    for replacement in to_replace:
        if replacement["word"] in punctuation:
            continue
        replacement_dict[replacement["word"]] = replacement["entity"].split("-")[1]

    for key, value in replacement_dict.items():
        text = text.replace(key,value)

    return text

print(remove_pii(""))