from util import file_util
import csv


# maakunta 2
# kunta 1
# kokonaan osoite 7 8
# postinumero (00000) 10


def process_csv():
    find_lacking_post_codes()


def find_lacking_post_codes():

    fin_data = file_util.open_csv('./csv/Suomi_osoitteet_2017-05-15.csv')

    postal_writer = csv_writer_generator('postal_codes')
    municipality_writer = csv_writer_generator('municipalities')
    province_writer = csv_writer_generator('provinces')
    address_writer = csv_writer_generator('addresses')

    for r in fin_data:
        if not r[2]:
            write_output_row(r, province_writer)
            continue

        if not r[2]:
            write_output_row(r, municipality_writer)
            continue

        if r[10] == '00000' or not r[10]:
            write_output_row(r, postal_writer)
            continue

        if not r[7] and not r[8]:
            write_output_row(r, address_writer)
            continue


def csv_writer_generator(file_name):
    f = csv.writer(open('./csv/mismatches/{}.csv'.format(file_name), 'w'))

    f.writerow(['building_code',
                'municipality',
                'province',
                'use',
                'northern_ETRSTM35FIN',
                'eastern_ETRSTM35FIN',
                # 'longitude_wgs84',
                # 'latitude_wgs84',
                'address_number',
                'street_finnish',
                'street_swedish',
                'house_number',
                'postal_code',
                'voting_area',
                'voting_area_name_finnish',
                'voting_area_name_swedish'
                ])

    return f


def write_output_row(r, filewriter):
    filewriter.writerow([
        r[0], r[1], r[2], r[3], r[4], r[5],
        r[6], r[7], r[8], r[9], str(r[10]),
        r[11], r[12], r[13]
    ])
