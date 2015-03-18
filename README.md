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

```
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
```

The script will fetch all datasets published by the instance (either a country or an organization), and statistics of successful downloads per dataset and per year. The script reports the number of download events and the number of downloaded occurrences. Since only successful downloads are considered, these numbers may slightly differ from the numbers shown at the GBIF portal.
