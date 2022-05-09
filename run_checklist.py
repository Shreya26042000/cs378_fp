import checklist
import checklist.editor as Editor
import checklist.perturb as Perturb
import datasets
from nltk.corpus import wordnet as wn
import random
from antonyms import antonyms_list
from synonyms import synonyms_list
import json
import csv  
from pattern.en import comparative, superlative

# default_datasets = {'qa': ('squad',), 'nli': ('snli',)}
#         # dataset_id = tuple(args.dataset.split(':')) if args.dataset is not None else \
#         #     default_datasets[args.task]
# dataset_id = ('snli', )
# # MNLI has two validation splits (one with matched domains and one with mismatched domains). Most datasets just have one "validation" split
# print(dataset_id)
# eval_split = 'validation_matched' if dataset_id == ('multi_nli',) else 'validation'
# # Load the raw data
# dataset = datasets.load_dataset(*dataset_id)

# test_dataset = dataset['test']
# # TODO: Can add training examples here
# max_samples = 10
# test_dataset = test_dataset.select(range(max_samples))



def create_antonyms_lsit():
  ADJ, ADJ_SAT, ADV, NOUN, VERB = "a", "s", "r", "n", "v"
  count = 0

  for i in wn.all_synsets():
      if i.pos() in ['a', 's']: # If synset is adj or satelite-adj.
          for j in i.lemmas(): # Iterating through lemmas for each synset.
              if j.antonyms(): # If adj has antonym.
                if count%2 == 0:
                    # Prints the adj-antonym pair.
                    with open("checklist_data/antonyms.txt", "a") as f:
                      f.write('(\'' + j.name() + '\'' + ',\'' + j.antonyms()[0].name() + '\')')
                      f.write(',\n')
                count+=1

def create_antonyms_dataset():
  editor = Editor.Editor()
  editor.lexicons['antonym'] = antonyms_list
  editor.lexicons['name'] = editor.lexicons['first_name']
  out = editor.template('{name1} is not {antonym1[0]},{name1} is {antonym1[1]}')

  # editor.template creates a cross product of all choices for placeholders. Let's sample 10 examples from this
  random.shuffle(out.data)
  examples = out.data[:1000]

  for row in examples:
    data = row.split(',')
    with open('checklist_data/antonyms_dataset2.json', 'a', encoding='UTF8') as f:
        # write the data
        data = {'premise': data[0],
        'hypothesis': data[1],
        'label': 0} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

def create_synonyms_list():
  ADJ, ADJ_SAT, ADV, NOUN, VERB = "a", "s", "r", "n", "v"
  count = 0

  for i in wn.all_synsets():
      if i.pos() in ['a', 's']: # If synset is adj or satelite-adj.
        word = i.lemmas()[0].name()
        synonyms = set()
        for syn in wn.synsets(word, pos=wn.ADJ):
          for l in syn.lemmas():
            synonyms.add(l.name())
        synonyms.remove(word)
        if synonyms.__len__() > 0:
          with open("checklist_data/synonyms.txt", "a") as f:
            f.write('(\'' + word + '\'' + ',\'' + next(iter(synonyms)) + '\')')
            f.write(',\n')

def create_synonyms_dataset1():
  editor = Editor.Editor()
  random.shuffle(synonyms_list)
  editor.lexicons['synonym'] = synonyms_list[:2000]
  editor.lexicons['name'] = editor.lexicons['first_name']
  out = editor.template('{name1} is {synonym1[0]},{name1} is {synonym1[1]}')

  # editor.template creates a cross product of all choices for placeholders. Let's sample 10 examples from this
  random.shuffle(out.data)
  examples = out.data[:1000]

  for row in examples:
    data = row.split(',')
    with open('checklist_data/synonyms_dataset1.json', 'a', encoding='UTF8') as f:
        # write the data
        data = {'premise': data[0],
        'hypothesis': data[1],
        'label': 0} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

def create_synonyms_dataset2():
  editor = Editor.Editor()
  random.shuffle(synonyms_list)
  editor.lexicons['synonym'] = synonyms_list[:2000]
  editor.lexicons['name'] = editor.lexicons['first_name']
  out = editor.template('{name1} is {synonym1[0]},{name1} is not {synonym1[1]}')

  # editor.template creates a cross product of all choices for placeholders. Let's sample 10 examples from this
  random.shuffle(out.data)
  examples = out.data[:1000]

  for row in examples:
    data = row.split(',')
    with open('checklist_data/synonyms_dataset2.json', 'a', encoding='UTF8') as f:
        # write the data
        data = {'premise': data[0],
        'hypothesis': data[1],
        'label': 2} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

# superlatives_dataset1()
def superlatives_comparitives1():
  with open("checklist_data/adjectives.txt", "r") as f:
      arr = f.readlines()
      adjectives = list(map(str.strip, arr))
      adjectives = list(map(lambda x: (comparative(x), superlative(x)), adjectives))

  editor = Editor.Editor()
  random.shuffle(adjectives)
  editor.lexicons['adjective'] = adjectives[:500]
  editor.lexicons['name'] = editor.lexicons['first_name'][:100]
  out = editor.template('Among {name1} and {name2}, the {adjective1[1]} is {name1};{name1} is {adjective1[0]} than {name2}')
  random.shuffle(out.data)
  examples = out.data[:1000]
  for row in examples:
    data = row.split(';')
    with open('checklist_data/superlatives_dataset.json', 'a', encoding='UTF8') as f:
        # write the data
        data = {'premise': data[0],
        'hypothesis': data[1],
        'label': 0} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

# superlatives_dataset2()
def superlatives_comparitives2():
  with open("checklist_data/adjectives.txt", "r") as f:
      arr = f.readlines()
      adjectives = list(map(str.strip, arr))
      adjectives = list(map(lambda x: (comparative(x), superlative(x)), adjectives))

  editor = Editor.Editor()
  random.shuffle(adjectives)
  editor.lexicons['adjective'] = adjectives[:500]
  editor.lexicons['name'] = editor.lexicons['first_name'][:100]
  out = editor.template('Among {name1} and {name2}, the {adjective1[1]} is {name2};{name1} is {adjective1[0]} than {name2}')
  random.shuffle(out.data)
  examples = out.data[:1000]
  for row in examples:
    data = row.split(';')
    with open('checklist_data/superlatives_dataset2.json', 'a', encoding='UTF8') as f:
        # write the data
        data = {'premise': data[0],
        'hypothesis': data[1],
        'label': 2} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

superlatives_comparitives2()


