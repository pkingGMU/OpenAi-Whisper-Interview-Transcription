# Remove PII with PII model
# Imports
import os
from transformers import BertConfig, BertModel
from transformers import T5Config, T5Model
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import AutoConfig
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch





def remove_pii(txt_file):
    # Find the model and tokenizer
    

    root = os.path.dirname(os.path.abspath(__file__))

    #Assuming you have downloaded and placed the model files in a local directory
    local_model_dir = root + '/bert_models'

    # Read the text file
    #with open(txt_file, 'r') as file:
    #    text = file.read()

    text = 'My name is John Doe and I live in New York. My phone number is 123-456-7890 and my email is bruh@gmail.com'

    tokenizer = AutoTokenizer.from_pretrained(local_model_dir, local_files_only=True, cache_dir=local_model_dir)
    max_length = tokenizer.model_max_length
    # Tokenize the text ensuring it fits within max_length
    tokenized_texts = tokenizer.batch_encode_plus(
        [text], 
        max_length=max_length, 
        truncation=True, 
        return_tensors='pt', 
        pad_to_max_length=True
    )

    input_ids = tokenized_texts['input_ids']
    attention_mask = tokenized_texts['attention_mask']  


    # For demonstration, print each segment
    for i in range(input_ids.size(1)):  # Loop through segments (if any)
        segment_input_ids = input_ids[:, i]
        segment_attention_mask = attention_mask[:, i]

        # Example: Print segment tokens and attention mask
        tokens = tokenizer.convert_ids_to_tokens(segment_input_ids.squeeze().tolist())
        print(f"Segment {i + 1} tokens: {tokens}")
        print(f"Segment {i + 1} attention mask: {segment_attention_mask}")

    # Load the model
    model = AutoModelForMaskedLM.from_pretrained(local_model_dir, local_files_only=True, cache_dir=local_model_dir)

    model.eval()
    # Pass the tokenized input to the model
    with torch.no_grad():  # To save memory during inference
        outputs = model(input_ids, attention_mask=attention_mask)
    


    return outputs



def main():

    ## TODO: Some easy way to select files without using a file explorer
    # Have user input the file name and get the path from the input
    # Ask user for patient ID
    patient_id = input('Enter the name of the patient: ')

    # Get the path of the file by searching a specific directory
    ## TODO: Change root folder to cyberduck
    root = os.path.dirname(os.path.abspath(__file__))


    for folder in os.listdir(root):
        print(folder)

        if folder == patient_id:
            file_path = os.path.join(root, folder)
            break
        else:
            file_path = 'Didnt find the folder'

    for file in os.listdir(file_path):
        print(file)

        if file.endswith('.txt'):
            text_file = os.path.join(file_path, file)
            break
        else:
            text_file = 'Didnt find the file'

    print (text_file)

    print (remove_pii(text_file))

if __name__ == "__main__":
    main()