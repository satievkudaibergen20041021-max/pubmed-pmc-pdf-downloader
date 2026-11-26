#Libraries
import time 
import xml.etree.ElementTree as ET
from helpers import *
import secrets

#Links and URLs
BASE_URL_ESEARCH = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
BASE_URL_ELINK = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
AMAZON_AWS_BASE_URL = "https://pmc-oa-opendata.s3.amazonaws.com/"
BASE_URL_ESUMMARY = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'

PMID_DICTIONARY_PATH =  ['esearchresult', 'idlist']
PMC_DICTIONARY_PATH = ['linksets', 0, 'linksetdbs', 0, 'links']



def id_getter(base_url, parameters, id_path):
    '''Finds id lists from requests'''
    id_list = []
    json_response_object = requester(base_url,parameters=parameters).json()
    file_writer_json('history/pubmed_history/id_list_file' + time.strftime('%Y-%m-%d') + secrets.token_hex(4) +'.json', json_response_object)
    try:
        first_key = id_path[0]
        value = json_response_object[first_key]
        for key in id_path[1:]:
            value = value[key]
        for iditem in value: 
            id_list.append(iditem)
    except KeyError as k: 
        display_message('An KeyError occured:', k)
    except IndexError as i:
        display_message('An IndexError occured:', i)
    except TypeError as t:
        display_message('An TypeError occured:', t)
    if len(id_list) == 0:
        display_message('No ids were found')
    return id_list


# Checks version of pmc in ListObjectsV2


def get_id_version(base_url, parameters, item):
    xml_response_object = requester(base_url, parameters=parameters)
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


def get_pubmed_metadata(base_url, parameters): 
    json_response_object = requester(base_url, parameters=parameters).json()
    file_writer_json('history/pubmed_history/metadata_file' + time.strftime('%Y-%m-%d') + secrets.token_hex(4) + '.json', json_response_object)
    return json_response_object