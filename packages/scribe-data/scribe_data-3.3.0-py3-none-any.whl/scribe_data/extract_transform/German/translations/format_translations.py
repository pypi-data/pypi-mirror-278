"""
Format Translations
-------------------

Formats and translates the words queried from Wikidata using query_translations.sparql.
"""

# pylint: disable=invalid-name

import collections
import json

from tqdm.auto import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

with open("../../_translations/translations_queried.json", encoding="utf-8") as f:
    translations_list = json.load(f)

words = [translation_vals["word"] for translation_vals in translations_list]
words = list(set(words))

translations_formatted = {}

# Note that because of poor results we are not using "Helsinki-NLP/opus-mt-en-de"
model = AutoModelForSeq2SeqLM.from_pretrained("t5-large")
tokenizer = AutoTokenizer.from_pretrained("t5-large")

for w in tqdm(words, desc="Words translated", unit="word",):
    inputs = tokenizer.encode(f"translate English to German: {w}", return_tensors="pt")
    outputs = model.generate(inputs, max_length=40, num_beams=4, early_stopping=True)

    translations_formatted[w] = tokenizer.decode(outputs[0], skip_special_tokens=True)

translations_formatted = collections.OrderedDict(sorted(translations_formatted.items()))

with open("../formatted_data/translations.json", "w", encoding="utf-8",) as f:
    json.dump(translations_formatted, f, ensure_ascii=False, indent=0)

print(f"Wrote file translations.json with {len(translations_formatted)} translations.")
