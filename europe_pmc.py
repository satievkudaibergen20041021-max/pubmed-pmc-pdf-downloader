# Libraries
import requests
import time 
import json
from email_validator import validate_email, EmailNotValidError
import xml.etree.ElementTree as ET
from helpers import *
from pypdf import PdfReader
from pypdf.errors import PdfReadError


# URL_links 
europe_pmc_url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'

def get_pmcid(base_url, headers, parameters):
    list_pmcid = []
    json_response_object = requester(base_url, headers, parameters).json()
    file_writer_json('history/europepmc_history/dic_r_unified_file' + time.strftime('%Y-%m-%d') + '.json', json_response_object)
    try:
        for article in json_response_object["resultList"]["result"]:
            article_pmcid = article.get("pmcid")
            if article_pmcid is None:
                continue
            list_pmcid.append(article_pmcid.removeprefix('PMC'))
    except KeyError as k: 
        display_message('dictionary keys were not found:', k)
    except IndexError as i:
        display_message('Probably list is missing:', i)
    except TypeError as t:
        display_message('keys are of an unapropriate type:', t)
    return list_pmcid




    
    