from util.prh_util import consts
from urllib.request import urlopen
import json


# industries = consts.ALL_INDUSTRIES

industries = [1]
selected_years = [2016]


def get_prh_data():
    company_dict = {}
    processed = 0
    selected_years = [2016]
    for year in selected_years:
        print('Now processing year: {}'.format(year))
        processed += write_company_data(company_dict, year)
    print('Handled {} companies'.format(processed))


def write_company_data(company_dict, year):
    total_company_amount = 0
    for businessline_id in industries:

        date_start_h1 = "{}-01-01".format(year)
        date_end_h1 = "{}-06-30".format(year)
        date_start_h2 = "{}-06-30".format(year)
        date_end_h2 = "{}-12-31".format(year)

        response_data_h1 = get_business_line_data(
            businessline_id, date_start_h1, date_end_h1)

        response_data_h2 = get_business_line_data(
            businessline_id, date_start_h2, date_end_h2)

        if response_data_h1 is None and response_data_h2 is None:
            continue

        total_company_amount += len(response_data_h1)
        total_company_amount += len(response_data_h2)

        for row in response_data_h1:
            details_response = urlopen(row["detailsUri"]).read()
            details = json.loads(details_response)["results"][0]
            company_dict[row['name']] = details

            with open('data/json/prh_data/output.json', 'w') as outfile:
                json.dump(company_dict, outfile)

        for row in response_data_h2:
            details_response = urlopen(row["detailsUri"]).read()
            details = json.loads(details_response)["results"][0]
            company_dict[row['name']] = details

            with open('data/json/prh_data/output.json', 'w') as outfile:
                json.dump(company_dict, outfile)

    return total_company_amount


def get_business_line_data(id, date_start, date_end):
    print("Business line id: " + str(id))

    url = "http://avoindata.prh.fi:80/bis/v1?totalResults=false&maxResults=1000&resultsFrom=0&businessLineCode={}&companyRegistrationFrom={}&companyRegistrationTo={}".format(
        id, date_start, date_end)

    json_response = urlopen(url).read()
    response_data = json.loads(json_response)["results"]

    print("Amount of results: " + str(len(response_data)))

    if len(response_data) > 999:
        print("Halting!!! This business line has over 1000 companies founded this year")
        print(id)
        return response_data

    return response_data
