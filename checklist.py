import checklist
# from checklist import Editor
# from checklist import Perturb

import datasets

default_datasets = {'qa': ('squad',), 'nli': ('snli',)}
# dataset_id = tuple(args.dataset.split(':')) if args.dataset is not None else \
    # default_datasets[args.task]

dataset_id = ('snli',)
# MNLI has two validation splits (one with matched domains and one with mismatched domains). Most datasets just have one "validation" split
print(dataset_id)
eval_split = 'validation_matched' if dataset_id == ('multi_nli',) else 'validation'
# Load the raw data
dataset = datasets.load_dataset(*dataset_id)

test_dataset = dataset['test']
# TODO: Can add training examples here
max_samples = 1000
test_dataset = test_dataset.select(range(max_samples))

print(test_dataset)