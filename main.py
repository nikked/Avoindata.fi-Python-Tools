# from util.geo_util import opt_to_csv, csv_to_json, test_geo_conversion

# from scripts import find_mismatching_data
# from scripts.prh_data import *
from scripts.prh.prh_data import get_prh_data
from scripts.prh.make_csv_of_prh_data import make_csv_of_prh_data
from scripts.liitynta_katalogi import get_liitynta_katalogi_data


def main():
    # find_mismatching_data.process_csv()
    make_csv_of_prh_data()
    # get_liitynta_katalogi_data()

if __name__ == '__main__':
    main()
