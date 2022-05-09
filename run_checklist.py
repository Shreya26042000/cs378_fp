import checklist
import checklist.editor as Editor
import checklist.perturb as Perturb
import datasets
from nltk.corpus import wordnet as wn
import random
from antonyms import antonyms_list
import json
import csv  

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

editor = Editor.Editor()
print (editor.lexicons.keys())
# print(test_dataset)

# for i in test_dataset:
#   print(i)

# ADJ, ADJ_SAT, ADV, NOUN, VERB = "a", "s", "r", "n", "v"
# count = 0

# for i in wn.all_synsets():
#     if i.pos() in ['a', 's']: # If synset is adj or satelite-adj.
#         for j in i.lemmas(): # Iterating through lemmas for each synset.
#             if j.antonyms(): # If adj has antonym.
#               if count%2 == 0:
#                   # Prints the adj-antonym pair.
#                   with open("checklist_data/antonyms.txt", "a") as f:
#                     # print(j.name(), j.antonyms()[0].name())
#                     f.write('(\'' + j.name() + '\'' + ',\'' + j.antonyms()[0].name() + '\')')
#                     f.write(',\n')
#               count+=1

editor.lexicons['antonym'] = antonyms_list[:10]
editor.lexicons['name'] = editor.lexicons['first_name'][:10]
out = editor.template('{name1} is {antonym1[0]},{name1} is {antonym1[1]},2')

# # editor.template creates a cross product of all choices for placeholders. Let's sample 10 examples from this
random.shuffle(out.data)
examples = out.data[:10]
for i in range(len(examples)):
    print ('contradiction ' + examples[i])


header = ['premise', 'hypothesis', 'label']

for row in examples:
  data = row.split(',')
  with open('checklist_data/antonyms_dataset.json', 'a', encoding='UTF8') as f:
      # write the data
      data = {'premise': data[0],
      'hypothesis': data[1],
      'label': data[2]}
      s = json.dumps(data)
      f.write(s + '\n')









