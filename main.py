#Libraries
import requests
import time 
from email_validator import validate_email, EmailNotValidError
import xml.etree.ElementTree as ET

#Links and URLs
base_url_esearch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
base_url_elink = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
s3_amazonaws_base_url = "https://pmc-oa-opendata.s3.amazonaws.com/"

PMID_DICTIONARY_PATH =  ['esearchresult', 'idlist']
PMC_DICTIONARY_PATH = ['linksets', 0, 'linksetdbs', 0, 'links']


#First part asks user for keywords to search articles 

def users_query():
    query = []
    nonoptional_searchword = input('Enter main keyword or multiple related terms: ') # User enters main keyword and related terms separated by ','
    while not nonoptional_searchword:
        nonoptional_keyword = input('plz enter at least one keyword: ')
    formated_nonoptional_searchword = [term.strip() for term in nonoptional_searchword.split(',')]    
    if len(formated_nonoptional_searchword) >= 2:
        query.append('('+' OR '.join(formated_nonoptional_searchword)+')')
    query.append(nonoptional_searchword)

    while True:
        additional_searchword = input('Do you want to add additional keywords? If not enter nothing: ') # User can add aditional terms for search
        if additional_searchword == '':
            break
        formated_additional_searchword = [term.strip() for term in additional_searchword.split(',')]
        if len(formated_additional_searchword) == 1:
            query.append(' AND '.join(formated_additional_searchword))
        elif len(formated_additional_searchword) >= 2:
            query.append('('+' OR '.join(formated_additional_searchword)+')')

    final_query = ' AND '.join(query)
    with open('search_history.txt', 'a', encoding='utf-8') as f:
        f.write(str(final_query) + time.strftime(' %Y-%m-%d-%H-%M, ') + '\n')  # this file stores the history of your requests
    return final_query

def email_input(): # Need email in order not to get banned
    try_again = True
    while try_again:
        your_email = input('Enter your email here:').strip()
        try: 
            email_vald = validate_email(your_email)
        except EmailNotValidError:
            print("You've entered invalid email!")
            try_again = True
        else:
            try_again = False
    return your_email

#helper functions

def display_message(message):
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
    json_response_object = requester(base_url, param).json()
    first_key = id_path[0]
    value = json_response_object[first_key]
    for key in id_path[1:]:
        value = value[key]
    file_writer('id_history/dic_r_unified_file.txt' + time.strftime('%Y-%m-%d'), 'a', str(json_response_object))
    try:
        for iditem in value: 
            id_list.append(iditem)
    except KeyError: 
        display_message('dictionary keys were not found')
    except IndexError:
        display_message('Probably list is missing')
    except TypeError:
        display_message('keys are of an unapropriate type')
    if len(id_list) == 0:
        display_message('No ids were found')
    return id_list


# Checks version of pmc in ListObjectsV2


def get_id_version(s3_base_url, params3, item):
    json_response_object = requester(s3_base_url, params3)
    root = ET.fromstring(json_response_object.text)
    namespace = root.tag.split('}')[0].strip('{')
    ns = {'s3': namespace}
    id_tag = root.find('.//s3:CommonPrefixes/s3:Prefix', ns)
    if id_tag is None:
        raise ValueError(f'ID tag is missing in {item}')
    id_version = id_tag.text.strip()
    if not id_version:
        raise ValueError(f"ID's version is Empty: {item}")
    file_writer(f'xml_ids/{item}.txt', 'w', json_response_object.text)
    return id_version


# Main part

def main():
    m = display_message('This is my first API-call! \n Before presing Enter please make sure that spelling is correct.')
    users_search = users_query()
    users_email = email_input()

    pmid_parameters = {
    'db': 'pubmed',
    'term': users_search,
    'retmode': 'json',
    'retmax': 200,
    'tool': 'my_pubmed_downloader',
    'email': users_email,
    'datetype': 'pdat',
    'mindate': '2020/01/01',
    'maxdate': time.strftime('%Y/%m/%d')
    }
    m = display_message(f'Program is searching for:{users_search}')

    list_of_pmid = id_getter(base_url_esearch, pmid_parameters, PMID_DICTIONARY_PATH)

    m = display_message(f'Found {len(list_of_pmid)} number of ids')

    pmc_parameters = {
    'dbfrom': 'pubmed',
    'db': 'pmc',
    'id': ','.join(list_of_pmid),
    'linkname': 'pubmed_pmc',
    'retmode': 'json',
    'tool': 'my_pubmed_downloader',
    'email': users_email
    }
    list_of_pmc = id_getter(base_url_elink, pmc_parameters, PMC_DICTIONARY_PATH)

    m = display_message(f'Found {len(list_of_pmc)} number of ids')

    versions_of_ids = []
    for item in list_of_pmc:
        parameters_for_id_version = {
        'list-type': '2',
        'prefix': 'PMC' + item + '.',
        'delimiter': '/' }
        try:
            version_of_id = get_id_version(s3_amazonaws_base_url, parameters_for_id_version, item)
        except ValueError:
            display_message(f" ID version was not found for the {item}")
            continue
        versions_of_ids.append(version_of_id)

    for item in versions_of_ids:
        url_to_download_pdf = f"https://pmc-oa-opendata.s3.amazonaws.com/{item}{item.strip('/')}.pdf"
        try:
           pdf_r = requester(url_to_download_pdf)
        except requests.exceptions.RequestException:
            display_message(f'Pdf {item} was not found')
            continue
        with open(f"downloads/{item.strip('/')}.pdf", "wb") as pdf_f:
            pdf_f.write(pdf_r.content)
    
if __name__ == '__main__':
    main()