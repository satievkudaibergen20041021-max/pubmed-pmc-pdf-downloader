#Libraries
import requests
import time 
from email_validator import validate_email, EmailNotValidError
import xml.etree.ElementTree as ET
from helpers import *


#Links and URLs
base_url_esearch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
base_url_elink = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
s3_amazonaws_base_url = "https://pmc-oa-opendata.s3.amazonaws.com/"

PMID_DICTIONARY_PATH =  ['esearchresult', 'idlist']
PMC_DICTIONARY_PATH = ['linksets', 0, 'linksetdbs', 0, 'links']



def id_getter(base_url, param, id_path):
    '''Finds id lists from requests'''
    id_list = []
    json_response_object = requester(base_url,parameters=param).json()
    file_writer_json('history/pubmed_history/dic_r_unified_file' + time.strftime('%Y-%m-%d') + '.json', json_response_object)
    first_key = id_path[0]
    value = json_response_object[first_key]
    for key in id_path[1:]:
        value = value[key]
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

