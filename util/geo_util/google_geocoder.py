from urllib.request import urlopen
import json
import pprint

# https://andrewpwheeler.wordpress.com/2016/04/05/using-the-google-geocoding-api-with-python/
# 2500 ilmaista hakua paivassa


def main():
    with open('./util/google_api_key.txt', 'r') as file:
        api_key = file.read()
    cli(api_key)


def cli(api_key):

    prompt = '---> '

    print('\nTervetuloa osoite, postinumero ja koordinaattihakuun')

    while True:
        print('\nMinka perusteella haluat tehda haun?')
        print('[1] Osoite')
        print('[2] Postinumero')
        print('[3] Koordinaatit')
        print('[x] Lopeta\n')

        choice = input(prompt)
        print('')

        if choice == '1':
            print('Syota osoite (Esim: Lintulahdenkuja 4 Helsinki)')
            address = input(prompt)
            query_address_data(address, api_key)

        elif choice == '2':
            print('Syota postinumero (Esim: 00101)')
            address = input(prompt)
            query_address_data(address, api_key)

        elif choice == '3':
            print('Syota leveysaste')
            lat = input(prompt)
            print('Syota pituussaste')
            lng = input(prompt)
            latlng = str(lat) + "," + str(lng)
            query_coordinate_data(latlng, api_key)

        elif choice == 'x':
            break

        else:
            print('\nVirheellinen valinta')


def query_address_data(address):
    with open('./util/google_api_key.txt', 'r') as file:
        api_key = file.read()
    base = 'https://maps.googleapis.com/maps/api/geocode/json?'
    q_address = "address=" + address.replace(" ", "+") + "+Finland"
    geo_url = base + q_address + "&key=" + '&region=.fi' + api_key
    return get_and_print_result(geo_url)


def query_coordinate_data(latlng, api_key=""):
    base = 'https://maps.googleapis.com/maps/api/geocode/json?'
    q_latlng = "latlng=" + latlng
    geo_url = base + q_latlng + "&key=" + '&region=.fi' + api_key
    return get_and_print_result(geo_url)


def get_and_print_result(geo_url):
    json_raw = urlopen(geo_url).read()
    geo_dict = json.loads(json_raw)

    try:
        result = geo_dict['results'][0]
        formatted_address = result['formatted_address']
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']

        # print('\nKohde: {}\nLeveysaste: {}\nPituusaste: {}'.format(
        #     formatted_address, lat, lng))

        return [lat, lng]

    except IndexError:
        print('\nEi hakutuloksia')


if __name__ == '__main__':
    main()
