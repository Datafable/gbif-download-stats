# -*- coding: utf-8 -*-

import requests
import json
import dateutil
from pytz import timezone
import datetime
import pandas as pd

PUBLISHED_COUNTRY = 'belgium'

def fetch_dataset_datapage(key, offset, limit):
    """ fetch one page with download statistics from GBIF """
    params = {'limit': limit, 'offset': offset}
    r = requests.get('http://api.gbif.org/v0.9/occurrence/download/dataset/' + key, params=params)
    data = r.json()['results']
    return data

def fetch_dataset_data(key):
    """ fetch and merge all pages with download statistics for one dataset """
    more_results_to_find = True
    offset = 0
    limit = 20
    download_stats = []
    while more_results_to_find:
        page = fetch_dataset_datapage(key, offset, limit)
        download_stats += page
        offset += 20
        if len(page) == 0:
            more_results_to_find = False
    return download_stats

def is_in_year(datetime_string, year):
    """ convert naive timestamp to non-naive and compare """
    dt = dateutil.parser.parse(datetime_string)
    tz = timezone('UTC')
    beginning_of_year = datetime.datetime(year, 1, 1, 0, 0, 0, 0, tzinfo=tz)
    start_of_next_year = datetime.datetime(year + 1, 1, 1, 0, 0, 0, 0, tzinfo=tz)
    return beginning_of_year <= dt < start_of_next_year

def get_downloaded_records(key):
    """ fetch and aggregate all download statistics for one dataset """
    raw_data = fetch_dataset_data(key)
    records = [x['numberRecords'] for x in raw_data]
    mod_dates = [x['download']['modified'] for x in raw_data]
    status_list = [x['download']['status'] for x in raw_data]
    in_2013 = [is_in_year(x, 2013) for x in mod_dates]
    in_2014 = [is_in_year(x, 2014) for x in mod_dates]
    data = pd.DataFrame({'numberRecords': records, 'mod_dates': mod_dates, 'in_2013': in_2013, 'in_2014': in_2014, 'status': status_list})
    total_nr_downloaded_records = data['numberRecords'].sum()
    total_nr_downloads = len(data)
    if total_nr_downloads > 0:
        data_in_2013 = data[data['in_2013'] == True]
        data_in_2014 = data[data['in_2014'] == True]
        # total succeeded
        tot_data_succeeded = data[data['status'] == 'SUCCEEDED']
        downloaded_records_succeeded = tot_data_succeeded ['numberRecords'].sum()
        nr_downloads_succeeded = len(tot_data_succeeded)
        # succeeded in 2013
        data_succeeded_in_2013 = data_in_2013[data_in_2013['status'] == 'SUCCEEDED']
        downloaded_records_succeeded_in_2013 = data_succeeded_in_2013['numberRecords'].sum()
        nr_downloads_succeeded_in_2013 = len(data_succeeded_in_2013)
        # succeeded in 2014
        data_succeeded_in_2014 = data_in_2014[data_in_2014['status'] == 'SUCCEEDED']
        downloaded_records_succeeded_in_2014 = data_succeeded_in_2014['numberRecords'].sum()
        nr_downloads_succeeded_in_2014 = len(data_succeeded_in_2014)
    else:
        downloaded_records_succeeded = 0
        nr_downloads_succeeded = 0
        downloaded_records_succeeded_in_2013 = 0
        nr_downloads_succeeded_in_2013 = 0
        downloaded_records_succeeded_in_2014 = 0
        nr_downloads_succeeded_in_2014 = 0
    return {'total_downloads': nr_downloads_succeeded,
            'total_records_downloaded': downloaded_records_succeeded,
            'downloads_succeeded_in_2013': nr_downloads_succeeded_in_2013,
            'records_succeeded_in_2013': downloaded_records_succeeded_in_2013,
            'downloads_succeeded_in_2014': nr_downloads_succeeded_in_2014,
            'records_succeeded_in_2014': downloaded_records_succeeded_in_2014}

def fetch_datasets_for_country(country):
    """ Fetch all datasets for this country """
    more_results_to_find = True
    offset = 0
    limit = 20
    all_datasets = []
    while more_results_to_find:
        params = {'publishing_country': country, 'offset': offset, 'limit': limit, 'type': 'occurrence'}
        r = requests.get('http://api.gbif.org/v0.9/dataset/search', params=params)
        datasets = r.json()['results']
        all_datasets += datasets
        offset += 20
        if len(datasets) == 0:
            more_results_to_find = False
    return all_datasets

def write_stats(datasets):
    """ Fetch dataset stats and print csv report """
    print 'publisher\tdataset_key\tdataset_title\ttotal_nr_downloads\ttotal_nr_downloaded_records\tsucceeded_downloads_2013\tsucceeded_records_2013\tsucceeded_downloads_2014\tsucceeded_records_2014'
    IGNORE_PUBLISHERS = ['PANGAEA - Publishing Network for Geoscientific and Environmental Data', 'GEO-Tag der Artenvielfalt']
    for ds in datasets:
        publisher = ds['owningOrganizationTitle']
        if publisher not in IGNORE_PUBLISHERS:
            try:
                download_data = get_downloaded_records(ds['key'])
                printable_data = [
                          publisher, ds['key'], 
                          ds['title'], 
                          str(download_data['total_downloads']), 
                          str(download_data['total_records_downloaded']), 
                          str(download_data['downloads_succeeded_in_2013']), 
                          str(download_data['records_succeeded_in_2013']), 
                          str(download_data['downloads_succeeded_in_2014']), 
                          str(download_data['records_succeeded_in_2014'])
                    ] 
                print '\t'.join(printable_data)
            except Exception as e:
                print 'Problem with dataset {0}'.format(ds)

def main():
    datasets = fetch_datasets_for_country(PUBLISHED_COUNTRY)
    write_stats(datasets)

if __name__ == '__main__':
    main()
