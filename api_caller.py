#What libraries would I be needing?
import requests
import time 
import pathlib
from bs4 import BeautifulSoup


#asks for users input 
print('=' * 30)
print('This is my first api call')

query = []
nonoptional_q = input('Enter the one keyword: ')
while not nonoptional_q:
    nonoptional_q = input('plz enter keyword: ')
split_o = [term.strip() for term in nonoptional_q.split(',')]    
if len(split_o) >= 2:
    query.append('('+' OR '.join(split_o)+')')
query.append(nonoptional_q)


while True:
    additional_q = input('Do you want to add additional keyword? If not enter nothing: ')
    if additional_q == '':
        break
    split_a = [term.strip() for term in additional_q.split(',')]
    if len(split_a) == 1:
        query.append(' AND '.join(split_a))
    elif len(split_a) >= 2:
        query.append('('+' OR '.join(split_a)+')')

final_query = ' AND '.join(query)
print(final_query)

#First part of the programm gets a XML file from pubmed 
base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'

p = {
    'db': 'pubmed',
    'term': final_query,
    'retmode': 'json',
    'retmax': 10,
    'datetype': 'pdat',
    'mindate': '2020/01/01',
    'maxdate': '2026/11/14'
}

# r = requests.get(base_url, params=p)
# r.raise_for_status()
# dic_r = r.json()
# print(dic_r) 

#Second part of the programm parses it 

#third part downloads the nesassery files 

