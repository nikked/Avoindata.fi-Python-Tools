from util.prh_util import consts
from urllib.request import urlopen
import json

import os.path
import os

industries = consts.ALL_INDUSTRIES

selected_years = [yr for yr in range(2017, 2018)]


def get_prh_data():
    os.makedirs(
        os.path.join(
            'data',
            'json',
            'prh_data',
            '2017')
    )

    processed = 0
    for year in selected_years:
        print('Now processing year: {}'.format(year))
        processed += write_company_data(year)
    print('Handled {} companies'.format(processed))


def write_company_data(year):
    total_company_amount = 0
    for businessline_id in industries:

        dir_path = 'data/json/prh_data/{}/'.format(year)

        print("Business line id: {}".format(businessline_id))

        company_dict = {}
        file_name = 'year_{}_industry _{}.json'.format(year, businessline_id)

        full_path = dir_path + file_name

        #  Check if the businessline for the year has already been processed
        if os.path.isfile(full_path):
            print('Businessline already processed')
            continue

        periods = [
            ("{}-01-01".format(year), "{}-01-31".format(year)),
            ("{}-02-01".format(year), "{}-02-29".format(year)),
            ("{}-03-01".format(year), "{}-03-31".format(year)),

            ("{}-04-01".format(year), "{}-04-30".format(year)),
            ("{}-05-01".format(year), "{}-05-31".format(year)),
            ("{}-06-01".format(year), "{}-06-30".format(year)),

            ("{}-07-01".format(year), "{}-07-31".format(year)),
            ("{}-08-01".format(year), "{}-08-31".format(year)),
            ("{}-07-01".format(year), "{}-09-30".format(year)),

            ("{}-10-01".format(year), "{}-10-31".format(year)),
            ("{}-11-01".format(year), "{}-11-30".format(year)),
            ("{}-12-01".format(year), "{}-12-31".format(year))
        ]

        for period in periods:
            date_start = period[0]
            date_end = period[1]

            response_data = get_business_line_data(
                businessline_id, date_start, date_end)

            if response_data == 'over 1000 results':
                break

            if not response_data:
                continue

            total_company_amount += len(response_data)

            for row in response_data:
                try:
                    details_response = urlopen(row["detailsUri"]).read()
                    details = json.loads(details_response)["results"][0]
                    company_dict[row['name']] = details
                except AttributeError:
                    company_dict[row['name']] = row

        if company_dict:
            with open('data/json/prh_data/{}/{}'.format(year, file_name),
                      'w') as outfile:
                json.dump(company_dict, outfile)

    return total_company_amount


def get_business_line_data(id, date_start, date_end):

    if id < 10:
        id = '0{}'.format(id)

    url = "http://avoindata.prh.fi:80/bis/v1?totalResults=false&maxResults=1000&resultsFrom=0&businessLineCode={}&companyRegistrationFrom={}&companyRegistrationTo={}".format(
        id, date_start, date_end)

    try:
        json_response = urlopen(url).read()
    except:
        return None

    response_data = json.loads(json_response)["results"]
    print('Period {}/{}'.format(date_start, date_end))
    print("Amount of results: " + str(len(response_data)))
    print()

    if len(response_data) > 999:
        print("This business line has over 1000 companies in this timeperiod")
        print(id)
        return response_data

    return response_data
