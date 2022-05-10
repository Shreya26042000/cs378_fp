import checklist
import checklist.editor as Editor
import checklist.perturb as Perturb
import datasets
from nltk.corpus import wordnet as wn
import random
from antonyms import antonyms_list
from synonyms import synonyms_list
from years import years_list
from country_city import country_city_list
from countryinfo import CountryInfo
import json
import csv  
from pattern.en import comparative, superlative

def create_antonyms_list():
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

def create_antonyms_dataset1():
  editor = Editor.Editor()
  editor.lexicons['antonym'] = antonyms_list
  editor.lexicons['name'] = editor.lexicons['first_name']
  out = editor.template('{name1} is {antonym1[0]},{name1} is {antonym1[1]}')

  # editor.template creates a cross product of all choices for placeholders. Let's sample 10 examples from this
  random.shuffle(out.data)
  examples = out.data[:1000]

  for row in examples:
    data = row.split(',')
    with open('checklist_data/antonyms_dataset1.json', 'a', encoding='UTF8') as f:
        # write the data
        data = {'premise': data[0],
        'hypothesis': data[1],
        'label': 2} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

def create_antonyms_dataset2():
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
  editor.lexicons['adjective'] = adjectives
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
  editor.lexicons['adjective'] = adjectives
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

def generate_years():
  years = range(1950, 2023)
  random.randint(1, len(years) - 2)
  for i in range(1000):
    with open("checklist_data/years.txt", "a") as f:
      index1 = random.randint(0, len(years) - 2)
      index2 = random.randint(index1 + 1, len(years) - 1)
      year1 = years[index1]
      f.write('(\'' + str(years[index1]) + '\'' + ',\'' + str(years[index2]) + '\')')
      f.write(',\n')


# superlatives_dataset2()
def temporal_reasoning1():
  editor = Editor.Editor()
  random.shuffle(years_list)
  editor.lexicons['year'] = years_list
  editor.lexicons['name'] = editor.lexicons['first_name'][:100]
  out = editor.template('{name1} was born in {year1[0]} and {name2} was born in {year1[1]}.;{name1} was born earlier than {name2}')
  random.shuffle(out.data)
  examples = out.data[:1000]
  for row in examples:
    data = row.split(';')
    with open('checklist_data/temporal_dataset1.json', 'a', encoding='UTF8') as f:
        # write the data
        data = {'premise': data[0],
        'hypothesis': data[1],
        'label': 0} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

def temporal_reasoning2():
  editor = Editor.Editor()
  random.shuffle(years_list)
  editor.lexicons['year'] = years_list
  editor.lexicons['name'] = editor.lexicons['first_name'][:100]
  out = editor.template('{name1} was born in {year1[1]} and {name2} was born in {year1[0]}.;{name1} was born earlier than {name2}')
  random.shuffle(out.data)
  examples = out.data[:1000]
  for row in examples:
    data = row.split(';')
    with open('checklist_data/temporal_dataset2.json', 'a', encoding='UTF8') as f:
        # write the data
        data = {'premise': data[0],
        'hypothesis': data[1],
        'label': 2} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

def generate_countries():
  editor = Editor.Editor()
  # print (editor.lexicons['country'])
  country_city = []
  for country in editor.lexicons['country']:
    try:
      capital = CountryInfo(country).capital()
      country_city.append((country, capital))
    except:
      print(country)
  print(country_city)

def create_countries_dataset1():
  editor = Editor.Editor()
  random.shuffle(country_city_list)
  editor.lexicons['country_capital'] = country_city_list
  editor.lexicons['name'] = editor.lexicons['first_name']
  out = editor.template('{name1} lives in {country_capital1[1]}.;{name1} lives in {country_capital1[0]}')

  # editor.template creates a cross product of all choices for placeholders. Let's sample 10 examples from this
  random.shuffle(out.data)
  examples = out.data[:1000]
  
  for row in examples:
    data = row.split(';')
    with open('checklist_data/countries_dataset1.json', 'a', encoding='UTF8') as f:
        # write the data
        data = {'premise': data[0],
        'hypothesis': data[1],
        'label': 0} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

def create_countries_dataset2():
  editor = Editor.Editor()
  random.shuffle(country_city_list)
  editor.lexicons['country_capital'] = country_city_list
  editor.lexicons['name'] = editor.lexicons['first_name']
  out = editor.template('{name1} lives in {country_capital1[1]}.;{name1} lives in {country_capital2[0]}')

  # editor.template creates a cross product of all choices for placeholders. Let's sample 10 examples from this
  random.shuffle(out.data)
  examples = out.data[:1000]
  
  for row in examples:
    data = row.split(';')
    with open('checklist_data/countries_dataset2.json', 'a', encoding='UTF8') as f:
        # write the data
        data = {'premise': data[0],
        'hypothesis': data[1],
        'label': 2} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

def create_neutral():
  editor = Editor.Editor()
  editor.lexicons['name'] = editor.lexicons['first_name']
  out = editor.template('{name1} is {nationality1}.;{name2} is {nationality1}.')

  # editor.template creates a cross product of all choices for placeholders.
  random.shuffle(out.data)
  examples = out.data[:1000]

  for row in examples:
    data = row.split(';')
    with open('checklist_data/neutral_dataset1.json', 'a', encoding='UTF8') as f:
        # write the data
        data = {'premise': data[0],
        'hypothesis': data[1],
        'label': 1} 
        # 0 for entailment
        # 1 for neutral
        # 2 for contradiction
        s = json.dumps(data)
        f.write(s + '\n')

# create_countries_dataset2()
create_neutral()
# generate_countries()
# superlatives_comparitives2()
# generate_years()
# temporal_reasoning2()

