import requests
import time 
import json
import xml.etree.ElementTree as ET
from email_validator import validate_email, EmailNotValidError

def users_query():
    query = []
    nonoptional_searchword = input('Enter main keyword or multiple related terms: ') # User enters main keyword and related terms separated by ','
    while not nonoptional_searchword:
        nonoptional_searchword = input('plz enter at least one keyword: ')
    formated_nonoptional_searchword = [term.strip() for term in nonoptional_searchword.split(',')]    
    if len(formated_nonoptional_searchword) >= 2:
        query.append('('+' OR '.join(formated_nonoptional_searchword)+')')
    else:
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


def display_message(*arg):
    '''just prints some important or unimportant messages'''
    print('=' * 100)
    print(*arg)
    print('*' * 100)


def requester(base_url, headers=None, parameters=None):
    '''As the name suggests it sends requests'''
    time.sleep(0.5)
    r = requests.get(base_url, headers=headers, params=parameters, timeout=30)
    r.raise_for_status()
    return r


def file_writer_str(path_file, mod, file):
    '''Saves the results of requests for maintainance reasons or id_lists'''
    with open(path_file, mod, encoding='utf-8') as f:
        f.write(file)


def file_writer_json(path_file, file):
    with open(path_file, "w", encoding="utf-8") as f:
        json.dump(file, f, indent=4, ensure_ascii=False)


def file_reader(path_file):
    '''Opens saved requests and id_lists'''
    with open(path_file, 'r', encoding='utf-8') as f:
        return f.read()


def get_id_version(s3_base_url, params3, item):
    xml_response_object = requester(s3_base_url, parameters=params3)
    root = ET.fromstring(xml_response_object.text)
    namespace = root.tag.split('}')[0].strip('{')
    ns = {'s3': namespace}
    id_tag = root.find('.//s3:CommonPrefixes/s3:Prefix', ns)
    if id_tag is None:
        raise ValueError(f'ID tag is missing in {item}')
    id_version = id_tag.text.strip()
    if not id_version:
        raise ValueError(f"ID's version is Empty: {item}")
    file_writer_str(f'xml_ids/{item}.txt', 'w', xml_response_object.text)
    return id_version