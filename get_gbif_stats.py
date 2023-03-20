# -*- coding: utf-8 -*-

import requests
import sys
import json
from dateutil import parser
import pandas as pd

DOCUMENTATION_MESSAGE = """
usage: get_gbif_stats.py <filter_type> <instance_name>

    filter_type: you can filter datasets either by country or
                organization. To specify this, set this parameter
                to "country" or "organization".

    instance_name: if you have chosen filter_type "country", then
                    the instance_name should be the owining
                    organization's country given as a ISO 639-1
                    (2 letter) country code. If filter_type is
                    "organization", instance_name should be the
                    owning organization's UUID key.
"""

def fetch_dataset_datapage(key, offset, limit):
    """ fetch one page with download statistics from GBIF """
    params = {'limit': limit, 'offset': offset}
    r = requests.get('http://api.gbif.org/v1/occurrence/download/dataset/' + key, params=params)
    data = r.json()['results']
    return data

def fetch_dataset_data(key):
    """ fetch and merge all pages with download statistics for one dataset """
    more_results_to_find = True
    offset = 0
    limit = 100
    download_stats = []
    while more_results_to_find:
        page = fetch_dataset_datapage(key, offset, limit)
        download_stats += page
        offset += 100
        if len(page) == 0:
            more_results_to_find = False
        print(str(key) + ": " + str(offset))
    return download_stats

def get_downloaded_records(key):
    """ fetch and aggregate all download statistics for one dataset """
    raw_data = fetch_dataset_data(key)
    records = [x['numberRecords'] for x in raw_data]
    mod_dates = [parser.parse(x['download']['modified']) for x in raw_data]
    status_list = [x['download']['status'] for x in raw_data]
    data = pd.DataFrame({'numberRecords': records, 'mod_dates': mod_dates, 'status': status_list})
    total_nr_downloads = len(data)
    if total_nr_downloads > 0:
        data['year'] = data['mod_dates'].apply(lambda x: x.year)
        result = data
    else:
        result = None
    return result

def fetch_datasets(filter_type=None, instance_name=None):
    """ Fetch all datasets for this country """
    more_results_to_find = True
    offset = 0 # Done: 0, 
    limit = 20
    all_datasets = []
    while more_results_to_find:
        if filter_type == 'country':
            params = {'publishingCountry': instance_name, 'offset': offset, 'limit': limit, 'type': 'sampling_event'}
        elif filter_type == 'publisher':
            params = {'publishingOrg': instance_name, 'offset': offset, 'limit': limit, 'type': 'sampling_event'}
        elif filter_type == 'host':
            params = {'hostingOrg': instance_name, 'offset': offset, 'limit': limit, 'type': 'sampling_event'}
        r = requests.get('http://api.gbif.org/v1/dataset/search', params=params)
        datasets = r.json()['results']
        all_datasets += datasets
        offset += 20
        # if len(datasets) == 0:
        more_results_to_find = False
    return all_datasets

def write_stats(datasets):
    """ Fetch dataset stats and print csv report """
    IGNORE_PUBLISHERS = []
    all_data = []
    for ds in datasets:
        publisher = ds['publishingOrganizationTitle']
        if publisher not in IGNORE_PUBLISHERS:
            try:
                download_data = get_downloaded_records(ds['key'])
                if download_data is None:
                    print('no downloads for {0}'.format(ds['key']))
                else:
                    download_data['dataset_key'] = [ds['key']] * len(download_data)
                    all_data.append(download_data)
            except Exception as e:
                print('Problem with dataset {0}'.format(ds))
    all_df = pd.concat(all_data)
    tot_data_succeeded = all_df[(all_df['status'] == 'SUCCEEDED') | (all_df['status'] == 'FILE_ERASED')][['numberRecords', 'year', 'dataset_key']]
    result = tot_data_succeeded.groupby(['year', 'dataset_key']).agg({'numberRecords': {'recordsDownloaded': sum, 'downloadEvents': len}})
    print(result.to_csv())

def main():
    if len(sys.argv) != 3:
        print(DOCUMENTATION_MESSAGE)
        sys.exit(-1)
    filter_type = sys.argv[1]
    if filter_type not in ['country', 'publisher', 'host']:
        print('filter_type should be "country", "publisher" or "host"')
        sys.exit(-1)
    instance_name = sys.argv[2]
    datasets = fetch_datasets(filter_type=filter_type, instance_name=instance_name)
    write_stats(datasets)

if __name__ == '__main__':
    main()
