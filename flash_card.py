import csv
import random
import requests

def GenerateRequestURL(vocab, mw_api_key):
  return f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{vocab}?key={mw_api_key}'

def ConnectMWDictionary(vocab, mw_api_key):
  request_url = GenerateRequestURL(vocab, mw_api_key)

  params = {'word': vocab, 'key': mw_api_key}
  result = requests.get(url = request_url, params = params)
  if result.status_code != 200:
    return False
  
  return True, result.json()

def JsonResultParser(json_result):
  query_vocab = json_result[0]['meta']['id']
  part_of_speech = json_result[0]['fl']  
  definition = json_result[0]['shortdef'][:]
  return query_vocab, part_of_speech, definition

def QueryVocab(vocab, mw_api_key):
  status, json_result = ConnectMWDictionary(vocab, mw_api_key)
  if status == True:
    return True, JsonResultParser(json_result)
  return False

vocabs = []
mw_api_key = ''

# Load your Merriam-Webster API key
with open('your_mw_api_key') as mw_api_key_file:
  mw_api_key = mw_api_key_file.readline()


with open('vocab_list.csv') as vocab_list_file:
  vocab_list_csv = csv.reader(vocab_list_file)

  for vocab in vocab_list_csv:
    vocabs.append(vocab[0])


random.shuffle(vocabs)

for vocab in vocabs:
  status, (q, p, d) = QueryVocab(vocab, mw_api_key)
  if status == True:
    print(f'Q: {q} ({p}) \t\t Hit enter to display the answer')
    input()
    print(f'A: {d}', end='\r\n')

  else:
    print(f'Error: \"{vocabs}\" query FAILED')
  print("\n==================================================\n")



