# from util.geo_util import opt_to_csv, csv_to_json, test_geo_conversion

# from scripts.postcodes import find_mismatching_data
# from scripts.prh_data import *
from scripts.prh.get_prh_data import get_prh_data
from scripts.prh.make_csv_of_prh_data import make_csv_of_prh_data
from scripts.liityntakatalogi import get_liitynta_katalogi_data
from scripts.postcodes import locations_converters


def main():

    # Postcodes
    # https://www.avoindata.fi/data/fi/dataset/postcodes
    # find_mismatching_data.process_csv()
    # locations_converters.convert_opt_to_csv()

    # PRH company data
    # https://avoindata.prh.fi/ytj.html
    # get_prh_data()
    make_csv_of_prh_data()

    # Liityntakatalogi
    # https://liityntakatalogi.suomi.fi/organization
    # get_liitynta_katalogi_data()


if __name__ == '__main__':
    main()
