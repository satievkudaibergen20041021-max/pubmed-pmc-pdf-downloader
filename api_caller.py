#Libraries
import requests
import time 
from email_validator import validate_email, EmailNotValidError
import xml.etree.ElementTree as ET

#Links and URLs
base_url_esearch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
base_url_elink = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
s3_base_url = "https://pmc-oa-opendata.s3.amazonaws.com/"


#asks for users input 

def users_query():
    query = []
    nonoptional_q = input('Enter main keyword or multiple related terms: ')
    while not nonoptional_q:
        nonoptional_q = input('plz enter at least one keyword: ')
    split_o = [term.strip() for term in nonoptional_q.split(',')]    
    if len(split_o) >= 2:
        query.append('('+' OR '.join(split_o)+')')
    query.append(nonoptional_q)

    while True:
        additional_q = input('Do you want to add additional keywords? If not enter nothing: ')
        if additional_q == '':
            break
        split_a = [term.strip() for term in additional_q.split(',')]
        if len(split_a) == 1:
            query.append(' AND '.join(split_a))
        elif len(split_a) >= 2:
            query.append('('+' OR '.join(split_a)+')')

    final_query = ' AND '.join(query)
    with open('search_history.txt', 'a', encoding='utf-8') as f:
        f.write(str(final_query) + time.strftime(' %Y-%m-%d-%H-%M, ') + '\n')  #history of your requests
    return final_query

def email_input():
    try_again = True
    while try_again:
        u_email = input('Enter your email here:').strip()
        try: 
            email_vald = validate_email(u_email)
        except EmailNotValidError:
            print("You've entered invalid email!")
            try_again = True
        else:
            try_again = False
    return u_email

#helper functions

def messenger(message):
    print('=' * 100)
    print(message)
    print('*' * 100)

def requester(base_url, parameters):
    time.sleep(1)
    r = requests.get(base_url, params=parameters)
    r.raise_for_status()
    return r

def file_writer(path_file, mod, file):
    with open(path_file, mod, encoding='utf-8') as f:
        f.write(file)
    
def file_reader(path_file):
    with open(path_file, 'r', encoding='utf-8') as f:
        return f.read()


#First part of the programm gets a json file from pubmed 


def getter_pmid(base_url_esearch, pmid_p):
    id_list = []
    dic_r = requester(base_url_esearch, pmid_p).json()
    file_writer('id_history/dic_r_file.txt' + time.strftime('%Y-%m-%d'), 'a', str(dic_r))
    try:
        for iditem in dic_r['esearchresult']['idlist']:
            id_list.append(iditem)
    except KeyError: 
        print('dictionary keys were not found')
    except IndexError:
        print('No ids were found')
    except TypeError:
        print('keys are of unknown type')
    file_writer('id_history/pmid_file.txt' + time.strftime('%Y-%m-%d'), 'a', str(id_list))
    if not id_list:
        raise Exception('No ids were found')
    return id_list


#Second part of the programm uses PMIDs to get PMCs


def getter_pmc(base_url_elink, pmc_p): 
    pmc_list = []
    dic_r = requester(base_url_elink, pmc_p).json()
    file_writer('id_history/dic_r_2_file.txt' + time.strftime('%Y-%m-%d'), 'a', str(dic_r))
    try:
        for iditem in dic_r['linksets'][0]['linksetdbs'][0]['links']: #need the other id list from the bottom
            pmc_list.append(iditem)
    except KeyError: 
        print('dictionary keys were not found')
    except IndexError:
        print('Probably list is missing')
    except TypeError:
        print('keys are of unapropriate type')
    file_writer('id_history/pmc_file.txt' + time.strftime('%Y-%m-%d'), 'a', str(pmc_list))
    if not pmc_list:
        raise Exception('No ids were found')
    return pmc_list


# third part cheks version of pmc in ListObjectsV2

s3_base_url = "https://pmc-oa-opendata.s3.amazonaws.com/"

def check_version(s3_base_url, params3, item):
    available_versions = []
    dic_r = requester(s3_base_url, params3)
    root = ET.fromstring(dic_r.text)
    namespace = root.tag.split('}')[0].strip('{')
    ns = {'s3': namespace}
    id_tag = root.find('.//s3:CommonPrefixes/s3:Prefix', ns)
    if id_tag is None:
        raise ValueError(f'ID version was not found for {item}')
    pdf_id = id_tag.text.strip()
    if not pdf_id:
        raise ValueError(f'ID version is Empty: {item}')
    available_versions.append(pdf_id)
    file_writer(f'xml_ids/{item}.txt', 'w', dic_r.text)
    return available_versions


 

# Main part

def main():
    m = messenger('This is my first API-call! \n Before presing Enter please make sure that spelling is correct.')
    your_query = users_query()
    your_email = email_input()

    pmid_p = {
    'db': 'pubmed',
    'term': your_query,
    'retmode': 'json',
    'retmax': 10,
    'tool': 'my_pubmed_downloader',
    'email': your_email,
    'datetype': 'pdat',
    'mindate': '2020/01/01',
    'maxdate': time.strftime('%Y/%m/%d')
}
    m = messenger(f'Program is searching for:{your_query}')

    pmid_var = getter_pmid(base_url_esearch, pmid_p)

    m = messenger(f'Successfuly found these id')
    pmc_p = {
    'dbfrom': 'pubmed',
    'db': 'pmc',
    'id': ','.join(pmid_var),
    'linkname': 'pubmed_pmc',
    'retmode': 'json',
    'tool': 'my_pubmed_downloader',
    'email': your_email
}
    pmc_var = getter_pmc(base_url_elink, pmc_p)

    for item in pmc_var:
        params3 = {
        'list-type': '2',
        'prefix': 'PMC' + item + '.',
        'delimiter': '/' }
        ver_var = check_version(s3_base_url, params3, item)

if __name__ == '__main__':
    main()