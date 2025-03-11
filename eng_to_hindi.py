#pip install transformers sentencepiece -q
from transformers import MarianMTModel, MarianTokenizer
from connect import *

model_name = "Helsinki-NLP/opus-mt-en-hi"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_en_to_hi(text):
    """Translates English text to Hindi using MarianMT"""
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    translated_tokens = model.generate(**inputs)

    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

english_text = "What is apple scab disease?"
translated_text = translate_en_to_hi(english_text)

print("English:", english_text)
print("Hindi:", translated_text)

#response=qa_chain.invoke({'query': translated_text})
#print("RESULT: ", response["result"])
