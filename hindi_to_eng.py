from transformers import MarianMTModel, MarianTokenizer
from connect import *

# Load MarianMT model and tokenizer
model_name = "Helsinki-NLP/opus-mt-hi-en"  # Hindi-to-English model
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_hi_to_en(text):
    """Translates Hindi text to English using MarianMT"""
    # Tokenize the Hindi input
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    # Generate translated text
    translated_tokens = model.generate(**inputs)

    # Decode and return the translated sentence
    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

# Example Usage
hindi_text = "एप्लेक स्कैब रोग क्या है?"
translated_text = translate_hi_to_en(hindi_text)

print("Hindi:", hindi_text)
print("English:", translated_text)
response=qa_chain.invoke({'query': translated_text})
print("RESULT: ", response["result"])
