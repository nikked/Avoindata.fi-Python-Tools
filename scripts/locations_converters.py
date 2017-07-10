import glob
from ..util import opt_to_csv, csv_to_json, test_geo_conversion


def convert_opt_to_csv():
    path = "./opt/*.OPT"
    for fname in glob.glob(path):
        if 'Suomi_osoitteet_2017-05-15.csv' in fname:
            continue
        print('Now processing {}'.format({fname}))
        file_name = fname[6:-4]
        opt_to_csv.convert(file_name)


def convert_csv_to_json():
    path = "./csv/*.csv"
    for fname in glob.glob(path):
        print('Now processing {}'.format({fname}))
        file_name = fname[6:-4]
        csv_to_json.godi_data(file_name)


def test_etrs_to_wgs84_conversion_accuracy():
    # 1019191118,421,16,2,7047819,382272,63.53895341875796,24.631605946925742,1,Kangasvierentie,,53,69440,001
    # ,Lestijärvi,

    northern = 7047819
    eastern = 382272
    address = 'Kangasvierentie 53 Lestijarvi'

    test_geo_conversion.test(northern, eastern, address)
