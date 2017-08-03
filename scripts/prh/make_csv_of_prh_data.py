import json
import csv
from glob import glob
import os.path


# def make_csv_of_prh_data(year):
#     pattern = os.path.join('./data/json/prh_data/{}'.format(year), '*.json')

#     with open('./data/csv/prh/{}.csv'.format(year), 'w', encoding='utf-8') as csv_file:
#         csv_writer = csv.writer(csv_file, delimiter=';')

#         write_title(csv_writer)

#         for file_path in glob(pattern):
#             print('Now processing: {}'.format(file_path))
#             write_dict(csv_writer, file_path)

def make_csv_of_prh_data():
    # pattern = os.path.join('./data/json/prh_data/{}'.format(year), '*.json')

    source = './data/json/prh_data/**/*.json'

    with open('./data/csv/prh/output.csv', 'w', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')

        write_title(csv_writer)
        # https://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
        for file_path in glob.iglob('./data/json/prh_data/**/*.json', recursive=True):
            print('Now processing: {}'.format(file_path))
            write_dict(csv_writer, file_path)


def write_title(csv_writer):

    csv_writer.writerow(['company_name',
                         'business_id',
                         'company_form',
                         'registration_date',
                         'address',
                         'post_code',
                         'city',
                         'liquidation'
                         ])


def write_dict(csv_writer, path):
    prh_dict = open_json(path)
    for key, value in prh_dict.items():
        name = value['name']
        business_id = value['businessId']
        company_form = value['companyForm']
        registration_date = value['registrationDate']

        address = post_code = city = ''
        try:
            address_data = value['addresses'][0]
            address = address_data['street']
            post_code = address_data['postCode']
            city = address_data['city']

        except:
            pass

        liquidation = ''
        try:
            liquidation = value['liquidations'][0]['description']
        except:
            pass
        csv_writer.writerow([
            name,
            business_id,
            company_form,
            registration_date,
            address,
            post_code,
            city,
            liquidation
        ])


def open_json(file_path):
    with open(file_path) as data_file:
        return json.load(data_file)
