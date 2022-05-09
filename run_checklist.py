import checklist
import checklist.editor as Editor
import checklist.perturb as Perturb
import datasets
from nltk.corpus import wordnet as wn

default_datasets = {'qa': ('squad',), 'nli': ('snli',)}
        # dataset_id = tuple(args.dataset.split(':')) if args.dataset is not None else \
        #     default_datasets[args.task]
dataset_id = ('snli', )
# MNLI has two validation splits (one with matched domains and one with mismatched domains). Most datasets just have one "validation" split
print(dataset_id)
eval_split = 'validation_matched' if dataset_id == ('multi_nli',) else 'validation'
# Load the raw data
dataset = datasets.load_dataset(*dataset_id)

test_dataset = dataset['test']
# TODO: Can add training examples here
max_samples = 10
test_dataset = test_dataset.select(range(max_samples))

editor = Editor.Editor()
print (editor.lexicons.keys())
print(test_dataset)

# for i in test_dataset:
#   print(i)

ADJ, ADJ_SAT, ADV, NOUN, VERB = "a", "s", "r", "n", "v"

for i in wn.all_synsets():
    if i.pos() in ['a', 's']: # If synset is adj or satelite-adj.
        for j in i.lemmas(): # Iterating through lemmas for each synset.
            if j.antonyms(): # If adj has antonym.
                # Prints the adj-antonym pair.
                print(j.name(), j.antonyms()[0].name())












