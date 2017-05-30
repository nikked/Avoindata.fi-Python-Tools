from util import etrs_to_wgs84, opt_to_csv, google_geocoder, file_util, csv_to_json
from geopy.distance import great_circle
import glob
import pprint


def main():
    # convert_opt_to_csv()
    # test_case()

    # jsonify_csv_geodata('./csv/Suomi_osoitteet_2017-05-15.csv')

    convert_csv_to_json()


def test_case():
    # 1019191118,421,16,2,7047819,382272,63.53895341875796,24.631605946925742,1,Kangasvierentie,,53,69440,001
    # ,Lestijärvi,

    northern = 7047819
    eastern = 382272

    address = 'Kangasvierentie 53 Lestijarvi'

    from_etrs = etrs_to_wgs84.etrs_to_wgs84(northern, eastern)
    from_google = google_geocoder.query_address_data(address)
    calculate_distance_between_coordinates(from_etrs, from_google)


def calculate_distance_between_coordinates(from_etrs, from_google):

    etrs = (from_etrs[0], from_etrs[1])
    google = (from_google[0], from_google[1])

    print(etrs)
    print(google)

    print(great_circle(etrs, google).meters)


def convert_csv_to_json():
    path = "./csv/*.csv"
    for fname in glob.glob(path):
        print('Now processing {}'.format({fname}))
        file_name = fname[6:-4]
        csv_to_json.godi_data(file_name)


def convert_opt_to_csv():
    path = "./opt/*.OPT"
    for fname in glob.glob(path):
        if 'Suomi_osoitteet_2017-05-15.csv' in fname:
            continue
        print('Now processing {}'.format({fname}))
        file_name = fname[6:-4]
        opt_to_csv.convert(file_name)


if __name__ == '__main__':
    main()
