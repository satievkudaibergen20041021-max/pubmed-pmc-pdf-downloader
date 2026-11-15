#What libraries would I be needing?
import requests
import time 
import pathlib
from bs4 import BeautifulSoup
from email_validator import validate_email 
import xml.etree.ElementTree as ET

#asks for users input 

print('=' * 50)
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


your_email = input('Enter your email here:').strip()
email  = validate_email(your_email)


final_query = ' AND '.join(query)

print('=' * 50)
print(f'Program is searching for:{final_query}')
with open('Pubmed_api/search_history.txt', 'a', encoding='utf-8') as file:
    file.write(str(final_query))


#First part of the programm gets a json file from pubmed 

base_url_esearch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'

pmid_p = {
    'db': 'pubmed',
    'term': final_query,
    'retmode': 'json',
    'retmax': 3,
    'tool': 'my_pubmed_downloader',
    'email': your_email,
    'datetype': 'pdat',
    'mindate': '2020/01/01',
    'maxdate': time.strftime('%Y/%m/%d')
}

def requester(base_url, parameters):
    time.sleep(1)
    r = requests.get(base_url, params=parameters)
    r.raise_for_status()
    dic_r = r.json()
    return dic_r

def id_list_writer(path_file, mod, file):
    with open(path_file, mod, encoding='utf-8') as file:
        file.write(file)
    
def id_list_reader(path_file):
    with open(path_file, 'r', encoding='utf-8') as file:
        return file.read()
    
#This part searches for PMID 

def getter_pmid(base_url_esearch, pmid_p):
    id_list = []
    for iditem in requester(base_url_esearch, pmid_p)['esearchresult']['idlist']:
        id_list.append(iditem)
    id_list_writer('Pubmed_api/pmid_file.txt', 'w', id_list)

print('=' * 50)
print(f'Here are articles ids:{id_list_reader('Pubmed_api/pmid_file.txt')}')


#Second part of the programm uses PMIDs to get PMCs

base_url_elink = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'

pmc_p = {
    'dbfrom': 'pubmed',
    'db': 'pmc',
    'id': ','.join(id_list_reader('Pubmed_api/pmid_file.txt')),
    'linkname': 'pubmed_pmc',
    'retmode': 'json',
    'tool': 'my_pubmed_downloader',
    'email': your_email
}


def getter_pmc(base_url_elink, pmc_p): 
    pmc_list = []
    for iditem in requester(base_url_elink, pmc_p)['linksets'][0]['linksetdbs'][0]['links']: #need the other id list from the bottom
        pmc_list.append(iditem)
    id_list_writer('Pubmed_api/pmc_file.txt', 'w', pmc_list)


#third part downloads the nesassery files 

base_url_efetch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

efetch_p = {
    'db': 'pmc',
    'id': ','.join(id_list_reader('Pubmed_api/pmc_file.txt')),
    'retmode': 'xml',
    'tool': 'my_pubmed_downloader',
    'email': your_email
}

def xml_getter(base_url_efetch, efetch_p):
    r = requests.get(base_url_efetch, params=efetch_p)
    r.raise_for_status()
    id_list_writer('Pubmed_api/' + final_query, 'w', r)


def main():
    id_list = getter_pmid(base_url_esearch, pmid_p)
    pmc_list = getter_pmc(base_url_elink, pmc_p)
    xml_chunk = xml_getter(base_url_efetch, efetch_p)