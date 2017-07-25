from util.prh_util import consts
from urllib.request import urlopen
import json


industries = consts.ALL_INDUSTRIES

# industries = [1]
selected_years = [2004]


def get_prh_data():
    processed = 0
    for year in selected_years:
        print('Now processing year: {}'.format(year))
        processed += write_company_data(year)
    print('Handled {} companies'.format(processed))


def write_company_data(year):
    total_company_amount = 0
    for businessline_id in industries:

        if businessline_id < 56:
            continue

        print("Business line id: {}".format(businessline_id))


        company_dict = {}
        file_name = 'year_{}_industry _{}.json'.format(year, businessline_id)

        periods = [
            ("{}-01-01".format(year), "{}-03-31".format(year)),
            ("{}-04-01".format(year), "{}-06-30".format(year)),
            ("{}-07-01".format(year), "{}-09-30".format(year)),
            ("{}-10-01".format(year), "{}-12-31".format(year))
        ]

        for period in periods:
            date_start = period[0]
            date_end = period[1]

            response_data = get_business_line_data(
                businessline_id, date_start, date_end)

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

        with open('data/json/prh_data/{}'.format(file_name),
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
        print("Halting!!! This business line has over 1000 companies founded this year")
        print(id)
        return response_data

    return response_data
