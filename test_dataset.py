import datasets
from datasets import concatenate_datasets, load_dataset

dataset_name = 'checklist_data/antonyms_dataset1.json'

dataset_id = ('snli', )
print(dataset_id)
# Load the raw data
snli_dataset = datasets.load_dataset(*dataset_id)
print(snli_dataset)

# Load from local json/jsonl file
labels = datasets.ClassLabel(names=['entailment', 'neutral', 'contradiction'])
new_dataset = datasets.load_dataset('json', data_files=dataset_name)
new_dataset = new_dataset.cast(snli_dataset['train'].features)

eval_split = 'train'
# print(snli_dataset)
# print(new_dataset)
concat_dataset = concatenate_datasets([snli_dataset['train'], new_dataset['train']])
# final_dataset = {'train': concat_dataset}
snli_dataset['train'] = concat_dataset 
print(snli_dataset)
