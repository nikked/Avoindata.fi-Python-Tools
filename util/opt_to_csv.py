import csv
from .etrs_to_wgs84 import etrs_to_wgs84


def convert(file_name):
    file_path = './opt/{}.OPT'.format(file_name)
    geo_data = open_opt_file(file_path)
    write_csv(geo_data, file_name)


def open_opt_file(file_path):
    # https://stackoverflow.com/questions/19699367/unicodedecodeerror-utf-8-codec-cant-decode-byte
    with open(file_path, 'r', encoding="ISO-8859-1") as opt_file:
        reader = csv.reader(opt_file, delimiter=";")
        return list(reader)


def write_csv(geo_data, file_name):
    f = csv.writer(open('./csv/{}.csv'.format(file_name), 'w'))

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

    for r in geo_data:

        etrs_lo = float(r[4])
        etrs_la = float(r[5])

        wgs84 = etrs_to_wgs84(etrs_lo, etrs_la)
        f.writerow([
            r[0], r[1], r[2], r[3], r[4], r[5],
            # wgs84[1],
            # wgs84[0],
            r[6], r[7], r[8], r[9], str(r[10]),
            r[11], r[12], r[13]
        ])


if __name__ == '__main__':
    print('Run this script as a module, not as a standalone.')
