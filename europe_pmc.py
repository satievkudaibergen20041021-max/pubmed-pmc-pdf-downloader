# Libraries
import time 
from helpers import *
import secrets


# URL_links 
europe_pmc_url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'

def get_metadata_europe_pmc(base_url, headers, parameters):
    json_response_object = requester(base_url, headers, parameters).json()
    file_writer_json('history/europepmc_history/metadata_file' + time.strftime('%Y-%m-%d') + secrets.token_hex(4) + '.json', json_response_object)
    return json_response_object

def get_pmcid(json_response_object):
    list_pmcid = []
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




    
    