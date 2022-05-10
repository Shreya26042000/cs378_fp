import checklist
import checklist.editor as Editor
import checklist.perturb as Perturb
import datasets
from nltk.corpus import wordnet as wn
import random
import json
import csv
import spacy
from nltk.corpus.reader.chasen import test  
from transformers import *
from parrot import Parrot

editor = Editor.Editor()

dataset_id = ('snli', )
dataset = datasets.load_dataset(*dataset_id)
test_dataset = dataset['test']
max_samples = 20

test_dataset = test_dataset.shuffle(seed=42)
test_dataset = test_dataset.select(range(max_samples))

# print(test_dataset)
# for i in test_dataset:
#   print(i)

def add_dataset(test_dataset):
  for row in test_dataset:
    with open('contrast_data/original.json', 'a', encoding='UTF8') as f:
        # write the data
        # data = {'premise': data[0],
        # 'hypothesis': data[1],
        # 'label': 0} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(row)
        f.write(s + '\n')

# Add typos to the premsie
def add_typos_premise(test_dataset):
  for row in test_dataset:
    with open('contrast_data/typos_premise.json', 'a', encoding='UTF8') as f:
        # write the data
        premise = Perturb.Perturb.add_typos(row['premise'])
        data = {'premise': premise,
        'hypothesis': row['hypothesis'],
        'label': row['label']} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

#add typos to the hypothesis
def add_typos_hypothesis(test_dataset):
  for row in test_dataset:
    with open('contrast_data/typos_hypothesis.json', 'a', encoding='UTF8') as f:
        # write the data
        hypothesis = Perturb.Perturb.add_typos(row['hypothesis'])
        data = {'premise': row['premise'],
        'hypothesis': hypothesis,
        'label': row['label']} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

# Add contractions to premise and hypothesis
def add_contractions(test_dataset):
  for row in test_dataset:
    with open('contrast_data/add_contractions.json', 'a', encoding='UTF8') as f:
        # write the data
        premise = Perturb.Perturb.contract(row['premise'])
        hypothesis = Perturb.Perturb.contract(row['hypothesis'])
        data = {'premise': premise,
        'hypothesis': hypothesis,
        'label': row['label']} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

# Expand contractions to premise and hypothesis
def expand_contractions(test_dataset):
  for row in test_dataset:
    with open('contrast_data/expand_contractions.json', 'a', encoding='UTF8') as f:
        # write the data
        premise = Perturb.Perturb.expand_contractions(row['premise'])
        hypothesis = Perturb.Perturb.expand_contractions(row['hypothesis'])
        data = {'premise': premise,
        'hypothesis': hypothesis,
        'label': row['label']} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

def add_negation_hypothesis(test_dataset):
  for row in test_dataset:
    with open('contrast_data/negate_hypothesis.json', 'a', encoding='UTF8') as f1:
      with open('contrast_data/original.json', 'a', encoding='UTF8') as f2:
        # write the data
        nlp = spacy.load('en_core_web_sm')
        pdata = list(nlp.pipe([row['hypothesis']]))
        print(pdata)
        ret = []
        try:
          ret = Perturb.Perturb.perturb(pdata, Perturb.Perturb.add_negation)
          # premise = row['premise']
          label = row['label']
          if label == 0:
            label = 2
          elif label == 2:
            label = 0
          if ret.data != []:
            s = json.dumps(row)
            f2.write(s + '\n')
            data = {'premise': row['premise'],
            'hypothesis': ret.data[0][1],
            'label': label} 
            # 0 for entailment
            # 1 for neutral
            # 2 for contradiction
            s = json.dumps(data)
            f1.write(s + '\n')
        except:
          pass
        
def paraphrase_premise(test_dataset):
  model = PegasusForConditionalGeneration.from_pretrained("tuner007/pegasus_paraphrase")
  tokenizer = PegasusTokenizerFast.from_pretrained("tuner007/pegasus_paraphrase")
  for row in test_dataset:
    premise = row['premise']
    # tokenize the text to be form of a list of token IDs
    inputs = tokenizer([premise], truncation=True, padding="longest", return_tensors="pt")
    # generate the paraphrased sentences
    outputs = model.generate(
      **inputs,
      num_beams=5,
      num_return_sequences=1,
    )
    # decode the generated sentences using the tokenizer to get them back to text
    premise = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    print(premise)

def paraphrase_premise2(test_dataset):
  parrot = Parrot()
  for row in test_dataset:
    premise = row['premise']
    # tokenize the text to be form of a list of token IDs
    paraphrases = parrot.augment(input_phrase=premise)
    # for paraphrase in paraphrases:
    #   print(paraphrase)
    premise = next(iter(paraphrases))
    print(premise)

# Both seem pretty slow tbh, the first might be faster.
# first was probably slightly faster

paraphrase_premise2(test_dataset)
# add_negation_hypothesis(test_dataset)
# add_dataset(test_dataset)
# add_typos_premise(test_dataset)
# add_typos_hypothesis(test_dataset)
# add_contractions(test_dataset)
# expand_contractions(test_dataset)



