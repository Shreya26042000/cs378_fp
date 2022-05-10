import datasets
from datasets import concatenate_datasets, load_dataset

# bookcorpus = load_dataset("bookcorpus", split="train")
# wiki = load_dataset("wikipedia", "20220301.en", split="train")
# wiki = wiki.remove_columns([col for col in wiki.column_names if col != "text"])  # only keep the 'text' column

# assert bookcorpus.features.type == wiki.features.type
# bert_dataset = concatenate_datasets([bookcorpus, wiki])

dataset_name = 'checklist_data/antonyms_dataset1.json'

dataset_id = ('snli', )
print(dataset_id)
# Load the raw data
snli_dataset = datasets.load_dataset(*dataset_id)
print(snli_dataset)
# test_dataset = dataset['test']
# # TODO: Can add training examples here
# max_samples = 10
# test_dataset = test_dataset.select(range(max_samples))

# Load from local json/jsonl file
labels = datasets.ClassLabel(names=['entailment', 'neutral', 'contradiction'])
new_dataset = datasets.load_dataset('json', data_files=dataset_name)
new_dataset = new_dataset.cast(snli_dataset['train'].features)

eval_split = 'train'
print(snli_dataset)
print(new_dataset)
concat_dataset = concatenate_datasets([snli_dataset['train'], new_dataset['train']])
# final_dataset = {'train': concat_dataset}
