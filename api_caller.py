#Libraries
import requests
import time 
from email_validator import validate_email, EmailNotValidError
import xml.etree.ElementTree as ET

#Links and URLs
base_url_esearch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
base_url_elink = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
s3_base_url = "https://pmc-oa-opendata.s3.amazonaws.com/"

pmid_path =  ['esearchresult', 'idlist']
pmc_path = ['linksets', 0, 'linksetdbs', 0, 'links']


#First part asks user fro keywords for searching articles 

def users_query():
    query = []
    nonoptional_q = input('Enter main keyword or multiple related terms: ') # User enters main keyword and related terms separated by ','
    while not nonoptional_q:
        nonoptional_q = input('plz enter at least one keyword: ')
    split_o = [term.strip() for term in nonoptional_q.split(',')]    
    if len(split_o) >= 2:
        query.append('('+' OR '.join(split_o)+')')
    query.append(nonoptional_q)

    while True:
        additional_q = input('Do you want to add additional keywords? If not enter nothing: ') # User can add aditional terms for search
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

def email_input(): # Need email in order not to get banned
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
    '''just prints some important or unimportant messages'''
    print('=' * 100)
    print(message)
    print('*' * 100)

def requester(base_url, parameters=None):
    '''As the name suggests it sends requests'''
    time.sleep(1)
    r = requests.get(base_url, params=parameters, timeout=7)
    r.raise_for_status()
    return r

def file_writer(path_file, mod, file):
    '''Saves the results of requests for maintainance reasons or id_lists'''
    with open(path_file, mod, encoding='utf-8') as f:
        f.write(file)
    
def file_reader(path_file):
    '''Opens saved requests and id_lists'''
    with open(path_file, 'r', encoding='utf-8') as f:
        return f.read()


def id_getter(base_url, param, id_path):
    '''Finds id lists from requests'''
    id_list = []
    dic_r = requester(base_url, param).json()
    first_key = id_path[0]
    value = dic_r[first_key]
    for key in id_path[1:]:
        value = value[key]
    file_writer('id_history/dic_r_unified_file.txt' + time.strftime('%Y-%m-%d'), 'a', str(dic_r))
    try:
        for iditem in value: 
            id_list.append(iditem)
    except KeyError: 
        messenger('dictionary keys were not found')
    except IndexError:
        messenger('Probably list is missing')
    except TypeError:
        messenger('keys are of an unapropriate type')
    if len(id_list) == 0:
        messenger('no ids were found')
    return id_list


# third part cheks version of pmc in ListObjectsV2


def get_ver_id(s3_base_url, params3, item):
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
    file_writer(f'xml_ids/{item}.txt', 'w', dic_r.text)
    return pdf_id


# Main part

def main():
    m = messenger('This is my first API-call! \n Before presing Enter please make sure that spelling is correct.')
    your_query = users_query()
    your_email = email_input()

    pmid_p = {
    'db': 'pubmed',
    'term': your_query,
    'retmode': 'json',
    'retmax': 500,
    'tool': 'my_pubmed_downloader',
    'email': your_email,
    'datetype': 'pdat',
    'mindate': '2020/01/01',
    'maxdate': time.strftime('%Y/%m/%d')
}
    m = messenger(f'Program is searching for:{your_query}')

    pmid_var = id_getter(base_url_esearch, pmid_p, pmid_path)

    m = messenger(f'Found {len(pmid_var)} number of ids')

    pmc_p = {
    'dbfrom': 'pubmed',
    'db': 'pmc',
    'id': ','.join(pmid_var),
    'linkname': 'pubmed_pmc',
    'retmode': 'json',
    'tool': 'my_pubmed_downloader',
    'email': your_email
}
    pmc_var = id_getter(base_url_elink, pmc_p, pmc_path)

    m = messenger(f'Found {len(pmc_var)} number of ids')

    version_ids = []
    for item in pmc_var:
        params3 = {
        'list-type': '2',
        'prefix': 'PMC' + item + '.',
        'delimiter': '/' }
        try:
            ver_var = get_ver_id(s3_base_url, params3, item)
        except ValueError:
            messenger(f" ID version was not found for the {item}")
            continue
        version_ids.append(ver_var)

    for item in version_ids:
        pdf_url = f"https://pmc-oa-opendata.s3.amazonaws.com/{item}{item.strip('/')}.pdf"
        try:
           pdf_r = requester(pdf_url)
        except requests.exceptions.RequestException:
            messenger(f'Pdf {item} was not found')
            continue
        with open(f"downloads/{item.strip('/')}.pdf", "wb") as pdf_f:
            pdf_f.write(pdf_r.content)
    
if __name__ == '__main__':
    main()