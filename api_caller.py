#What libraries would I be needing?
import requests
import time 
import pathlib
from bs4 import BeautifulSoup


#asks for users input 
print('=' * 30)
print('This is my first api call')

query = []
optional_q = input('Enter here main keywords and related terms: ').strip()
while not optional_q:
    optional_q = input('plz enter at least one keyword: ').strip()
additional_q = input('Enter additional terms you want to query: ').strip()
split_o = optional_q.split()
split_a = additional_q.split()
if len(split_o) == 1 or not additional_q:
    query.append('+OR+'.join(split_o))
elif len(split_o) >= 2:
    query.append('('+'+OR+'.join(split_o)+')')

if additional_q:
    if len(split_a) == 1:
        query.append('+OR+'.join(split_a))
    elif len(split_a) >= 2:
        query.append('('+'+OR+'.join(split_a)+')')


final_query = '+AND+'.join(query)

print(final_query)
#First part of the programm gets a XML file from pubmed 
base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

#Second part of the programm parses it 

#third part downloads the nesassery files 

