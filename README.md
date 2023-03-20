# GBIF download stats

See how popular your published datasets are.

## Introduction

The GBIF API allows you to query the download statistics of your published datasets. This script demonstrates how to do this.

## Dependencies

This script uses Python (2.7.x) and the following modules:

- [datetime](https://docs.python.org/2.7/library/datetime.html): Part of the standard Python package.
- [json](https://docs.python.org/2/library/json.html): Part of the standard Python package.
- [pandas](http://pandas.pydata.org/): install with `pip install pandas`
- [python-dateutil](http://labix.org/python-dateutil): install with `pip install python-dateutil`
- [pytz](http://pytz.sourceforge.net/): install with `pip install pytz`
- [Requests](http://docs.python-requests.org/en/latest/): install with `pip install requests`

## Run the script

Usage:

```
python get_gbif_stats.py <filter_type> <instance_name> > output_file.txt
```

* `filter_type`: you can filter datasets either by `country`, `organization` or `installation`
* `instance_name`: depends on `filter_type`
  * for `country`: use the `ISO 639-1` (2 letter) country code, e.g. `BE`
  * for `organization`: use the publisher key, e.g. [`1cd669d0-80ea-11de-a9d0-f1765f95f18b`](https://www.gbif.org/publisher/1cd669d0-80ea-11de-a9d0-f1765f95f18b)
  * for `host`: use the GBIF installation key, e.g. [`9f25fd85-85dc-4dcd-a1b4-b31165442e2b`](https://www.gbif.org/installation/9f25fd85-85dc-4dcd-a1b4-b31165442e2b)

The script will fetch all datasets published by the instance and statistics of successful downloads per dataset and per year. The script reports the number of download events and the number of downloaded occurrences. Since only successful downloads are considered, these numbers may slightly differ from the numbers shown at the GBIF portal.
