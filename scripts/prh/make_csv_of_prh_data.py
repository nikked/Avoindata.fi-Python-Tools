import json
import csv
import glob
import os.path

# contact details
# only existing companies (exclude lakannut kaupparekister merkinta)


def make_csv_of_prh_data():

    with open('./data/csv/prh/full_prh_data.csv', 'w', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')

        write_title(csv_writer)

        # write content
        # https://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
        for file_path in glob.iglob(
                './data/json/prh_data/**/*.json', recursive=True):
            print('Now processing: {}'.format(file_path))
            write_dict(csv_writer, file_path)


def write_title(csv_writer):

    csv_writer.writerow(['company_name',
                         'business_id',
                         'company_form',
                         'business_line_code',
                         'business_line_name',
                         'registration_date',
                         'postal_address',
                         'postal_post_code',
                         'postal_city',
                         'street_address',
                         'street_post_code',
                         'street_city',
                         'liquidation',
                         # 'phone number',
                         'registered office'
                         ])


def write_dict(csv_writer, path):
    prh_json = open_json(path)
    for key, value in prh_json.items():

        # If company does not exist anymore in traderegister, skip it
        company_exists = True
        for entry in value['registeredEntries']:
            if entry['register'] == 1:
                if entry['description'] in ['Lakannut', 'Ceased']:
                    company_exists = False

        if not company_exists:
            continue

        # Otherwise, proceed writing the company to csv

        # BASIC DATA
        name = value['name']
        business_id = value['businessId']
        company_form = value['companyForm']
        registration_date = value['registrationDate']

        # ADDRESSES
        # Fetch street address and postal address separately.
        # For both, fetch the most recent version

        # Version 1: most recent address
        # Type 1: street address
        # Type 2: postal address

        # Street address
        street_address = street_post_code = street_city = ''
        try:
            writeable_street_address = ''
            for address in value['addresses']:
                if address['version'] == 1 and address['type'] == 1:
                    writeable_street_address = address

            street_address = writeable_street_address['street']
            street_post_code = str(writeable_street_address['postCode'])
            street_city = writeable_street_address['city']

        # Raises when no addresses are defined
        except TypeError:
            pass

        # Postal address
        postal_address = postal_post_code = postal_city = ''
        try:
            writeable_postal_address = ''
            for address in value['addresses']:

                if address['version'] == 1 and address['type'] == 2:
                    writeable_postal_address = address

            postal_address = writeable_postal_address['street']
            postal_post_code = str(writeable_postal_address['postCode'])
            postal_city = writeable_postal_address['city']

        except TypeError:
            pass

        #  INDUSTRY
        industry = ''

        try:
            industry = value['businessLines'][2]['name']

        except IndexError:
            pass

        try:
            industry_code = value['businessLines'][0]['code']

        except IndexError:
            pass

        # LIQUIDATIONS
        liquidation = ''
        if value['liquidations']:
            for lq in value['liquidations']:
                if lq['version'] == 1:
                    liquidation = lq['description']

                if not liquidation:
                    liquidation = lq['description']

        # CONTACT DETAILS
        phone = ''
        if value['contactDetails']:
            for dt in value['contactDetails']:
                if 'puhelin' in dt['type'].lower():
                    phone = dt['value']

        # REGISTERED OFFICE
        # Note there is a typo in PRH's api:
        # registeredOffice vs registedOffice
        registered_office = ''
        if 'registedOffices' in value:
            for reg in value['registedOffices']:
                if reg['version'] == 1:

                    registered_office = reg['name']

        # WRITE TO CSV
        csv_writer.writerow([
            name,
            business_id,
            company_form,
            industry_code,
            industry,
            registration_date,
            postal_address,
            postal_post_code,
            postal_city,
            street_address,
            street_post_code,
            street_city,
            liquidation,
            # phone,
            registered_office
        ])


def open_json(file_path):
    with open(file_path) as data_file:
        return json.load(data_file)
