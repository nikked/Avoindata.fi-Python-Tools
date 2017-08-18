import glob
from util.prh_util import csv_to_json, test_geo_conversion
from scripts.postcodes import opt_to_csv


# A function to convert multiple OPT files to CSV
def convert_opt_to_csv():
    path = "./opt/*.OPT"
    for fname in glob.glob(path):
        print('Now processing {}'.format({fname}))
        file_name = fname[6:-4]
        opt_to_csv.convert(file_name)


# A function that creates an JSON version of data
def convert_csv_to_json():
    path = "./csv/*.csv"
    for fname in glob.glob(path):
        print('Now processing {}'.format({fname}))
        file_name = fname[6:-4]
        csv_to_json.godi_data(file_name)


#  Testing accuracy of geo conversion
def test_etrs_to_wgs84_conversion_accuracy():
    northern = 7047819
    eastern = 382272
    address = 'Kangasvierentie 53 Lestijarvi'

    test_geo_conversion.test(northern, eastern, address)
