import requests
import time 
from email_validator import validate_email, EmailNotValidError
import xml.etree.ElementTree as ET

from helpers import *
from pumbed import *
from europe_pmc import *


from pypdf import PdfReader
from pypdf.errors import PdfReadError
from io import BytesIO


def main():
    display_message('Medical-articles API-caller v2.0! \n Before presing Enter please make sure that spelling is correct.')
    users_search = users_query()
    users_email = email_input()

    set_of_pmcid = set()

    pmid_parameters = {
        'db': 'pubmed',
        'term': users_search,
        'retmode': 'json',
        'retmax': 100,
        'tool': 'my_pubmed_downloader',
        'email': users_email,
        'datetype': 'pdat',
        'mindate': '2020/01/01',
        'maxdate': time.strftime('%Y/%m/%d')
    }
    display_message(f'Program is searching for: {users_search} in Pumbed')
    
    pubmed_pmid = id_getter(base_url_esearch, pmid_parameters, PMID_DICTIONARY_PATH)
    
    display_message(f'Found {len(pubmed_pmid)} number of ids in Pubmed')
    
    pmc_parameters = {
        'dbfrom': 'pubmed',
        'db': 'pmc',
        'id': ','.join(pubmed_pmid),
        'linkname': 'pubmed_pmc',
        'retmode': 'json',
        'tool': 'my_pubmed_downloader',
        'email': users_email
    }
    pubmed_pmcid = id_getter(base_url_elink, pmc_parameters, PMC_DICTIONARY_PATH)
    
    display_message(f'Found {len(pubmed_pmcid)} number of ids in Pubmed')

    for item in pubmed_pmcid:
        set_of_pmcid.add(item)

    display_message(f'Programm is searching for: {users_search} in Europe PMC')


    search_headers = {
        "User-Agent": f"PubMedResearchProject/2.0 (contact: {users_email})",
        "Accept": "application/json"
    }
    
    parameters_europe_pmc = {
        "query": f"{users_search} AND FIRST_PDATE:[2020-01-01 TO {time.strftime('%Y-%m-%d')}]",
        "format": "json",
        "resultType": "core",
        "pageSize": 100,
    }

    europe_pmcid = get_pmcid(europe_pmc_url, headers=search_headers, parameters=parameters_europe_pmc)

    display_message(f'Found {len(europe_pmcid)} number of ids in Europe PMC')

    for item in europe_pmcid:
        set_of_pmcid.add(item)

    display_message(f'Found {len(set_of_pmcid)} number if articles in total')

    versions_of_ids = []
    for item in set_of_pmcid:
        parameters_for_id_version = {
             'list-type': '2',
             'prefix': 'PMC' + item + '.',
             'delimiter': '/' 
        }
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
        try: 
            PdfReader(BytesIO(pdf_r.content))
        except PdfReadError:
            print(f'Invalid PDF file for: {item}')
            continue
        with open(f"downloads/{item.strip('/')}.pdf", "wb") as pdf_f:
            pdf_f.write(pdf_r.content)

    display_message('Done!')
if __name__ == "__main__":
    main()