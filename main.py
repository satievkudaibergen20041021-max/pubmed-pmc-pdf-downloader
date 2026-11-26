import requests
import time 

from helpers import *
from pumbed import *
from europe_pmc import *


from pypdf import PdfReader
from pypdf.errors import PdfReadError
from io import BytesIO

import json

def main():
    display_message('Medical-articles API-caller v2.0! \n Before presing Enter please make sure that spelling is correct.')
    users_search = users_query()
    users_email = email_input()
    users_choice_of_database = ask_which_database_to_use()
    users_choice_of_type_of_data = ask_for_metadata_or_pdf()

    set_of_pmcid = set()



    if users_choice_of_database == 'Pubmed' or users_choice_of_database == 'BOTH': 
        search_volume_pubmed: int = input('Enter the number of articles you need from Pubmed: ')
        set_of_pubmed_pmcid = set()

        pmid_parameters = {
        'db': 'pubmed',
        'term': users_search,
        'retmode': 'json',
        'retmax': search_volume_pubmed,
        'tool': 'my_pubmed_downloader',
        'email': users_email,
        'datetype': 'pdat',
        'mindate': '2020/01/01',
        'maxdate': time.strftime('%Y/%m/%d')
        }

        display_message(f'Program is searching for: {users_search} in Pumbed')
    
        pubmed_pmid = id_getter(BASE_URL_ESEARCH, pmid_parameters, PMID_DICTIONARY_PATH)
    
        display_message(f'Found {len(pubmed_pmid)} number of PMID in Pubmed')

        if users_choice_of_type_of_data == 'Metadata':

            metadata_params = {
                "db": "pubmed",
                "id": ','.join(pubmed_pmid),
                "retmode": "json"
            }
            pubmed_metadata = get_pubmed_metadata(BASE_URL_ESUMMARY, metadata_params)

            display_message(f'Found {len(pubmed_metadata['result']) - 1} number of articles in Pubmed')

        elif users_choice_of_type_of_data == 'Articles (pdf)':
            
            pmc_parameters = {
            'dbfrom': 'pubmed',
            'db': 'pmc',
            'id': ','.join(pubmed_pmid),
            'linkname': 'pubmed_pmc',
            'retmode': 'json',
            'tool': 'my_pubmed_downloader',
            'email': users_email
            }

            pubmed_pmcid = id_getter(BASE_URL_ELINK, pmc_parameters, PMC_DICTIONARY_PATH)
    
            display_message(f'Found {len(pubmed_pmcid)} number of PMCID in Pubmed')

            for item in pubmed_pmcid:
                set_of_pubmed_pmcid.add(item)

            display_message(f'{len(set_of_pubmed_pmcid)} number of ids were left after duplicates have been removed ')

            set_of_pmcid.update(set_of_pubmed_pmcid)



    if users_choice_of_database == 'Europe PMC' or users_choice_of_database == 'BOTH':

        search_volume_europe: int = input('Enter the number of articles you need from Europe PMC: ')

        display_message(f'Programm is searching for: {users_search} in Europe PMC')

        list_of_europe_pmcid = []
        
        search_headers = {
        "User-Agent": f"PubMedResearchProject/2.0 (contact: {users_email})",
        "Accept": "application/json"
        }
    
        parameters_europe_pmc = {
        "query": f"{users_search} AND FIRST_PDATE:[2020-01-01 TO {time.strftime('%Y-%m-%d')}]",
        "format": "json",
        "resultType": "core",
        "pageSize": search_volume_europe,
        }

        europe_pmcid_metadata = get_metadata_europe_pmc(europe_pmc_url, headers=search_headers, parameters=parameters_europe_pmc)
        python_object_metadata = json.loads(europe_pmcid_metadata)
        display_message(f'Found {python_object_metadata["hitCount"]} number of articles in Europe PMC')

        if users_choice_of_type_of_data == 'Articles (pdf)':
            europe_pmc_ids = get_pmcid(europe_pmcid_metadata) 
            for item in europe_pmc_ids:
                list_of_europe_pmcid.append(item)

            display_message(f'Found {len(list_of_europe_pmcid)} number of ids in Europe PMC')

            set_of_europe_pmcid = set(list_of_europe_pmcid)

            display_message(f'{len(set_of_europe_pmcid)} number of ids were left after duplicates have been removed')

            set_of_pmcid.update(set_of_europe_pmcid)



    if users_choice_of_type_of_data == 'Articles (pdf)':

        display_message(f'Found {len(set_of_pmcid)} number if articles in total')

        versions_of_ids = []
        for item in set_of_pmcid:
            parameters_for_id_version = {
             'list-type': '2',
             'prefix': 'PMC' + item + '.',
             'delimiter': '/' 
            }
            try:
                version_of_id = get_id_version(AMAZON_AWS_BASE_URL, parameters_for_id_version, item)
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