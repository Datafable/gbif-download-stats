# GBIF download stats

See how popular your published datasets are.

# Introduction

The GBIF API allows you to query the download statistics of your published datasets. This script demonstrates how to do this.

# Dependencies

This script uses Python (2.7.x) and the following modules:

- [datetime](https://docs.python.org/2.7/library/datetime.html): Part of the standard Python package.
- [json](https://docs.python.org/2/library/json.html): Part of the standard Python package.
- [pandas](http://pandas.pydata.org/): install with `pip install pandas`
- [python-dateutil](http://labix.org/python-dateutil): install with `pip install python-dateutil`
- [pytz](http://pytz.sourceforge.net/): install with `pip install pytz`
- [Requests](http://docs.python-requests.org/en/latest/): install with `pip install requests`

# Run the script

run `python get_gbif_stats.py > out.tsv`

The script will fetch all datasets published by a Belgian publisher, and print the download statistics for 2013 and 2014.

If you're not interested in the Belgian datasets, change the value of variable `PUBLISHED_COUNTRY`. A list of all valid names can be found [here](http://www.gbif.org/country).

The script reports on the number of downloads and the number of occurrences downloaded in 2013, 2014 and overall. It only counts `succeeded` downloads (which is why it may slightly differ from the number of downloads that is reported on the GBIF portal).
