#What libraries would I be needing?
import requests
import time 
import pathlib
from bs4 import BeautifulSoup
from email_validator import validate_email 

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

#First part of the programm gets a json file from pubmed 

base_url_esearch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'

pmid_p = {
    'db': 'pubmed',
    'term': final_query,
    'retmode': 'json',
    'retmax': 10,
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
    return dic_r #need to create a file to append the results so I wont make repetitive requests

#This part searches for PMID 

def scroller_pmid(base_url_esearch, pmid_p):
    id_list = []
    for iditem in requester(base_url_esearch, pmid_p)['esearchresult']['idlist']:
        id_list.append(iditem)
    return id_list

print('=' * 50)
print(f'Here are articles ids:{id_list}')

#Second part of the programm uses PMIDs to get PMCs

base_url_elink = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'

pmc_p = {
    'dbfrom': 'pubmed',
    'db': 'pmc',
    'id': ','.join(id_list),
    'linkname': 'pubmed_pmc',
    'retmode': 'json',
    'tool': 'my_pubmed_downloader',
    'email': your_email
}


def scroller_pmc(base_url_elink, pmc_p): 
    pmc_list = []
    for iditem in requester(base_url_elink, pmc_p)['linksets']['ids']: #need the other id list from the bottom
        pmc_list.append(iditem)
    return pmc_list #should also save it to avoid repetetive calls 


def main():
    id_list = scroller_pmid(base_url_esearch, pmid_p)
    pmc_list = scroller_pmc(base_url_elink, pmc_p)

#third part downloads the nesassery files 

