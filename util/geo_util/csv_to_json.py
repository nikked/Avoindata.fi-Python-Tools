from . import file_util


def godi_data(file_name):

    #     Zipcodes
    # Addresses
    # Coordinates (latitude, longitude)
    # Data available for entire country

    data = _open_file_and_skip_header(file_name)

    out = {}

    for r in data:
        province = r[2]
        if province not in out:
            out[province] = {}

        municipality = r[1]
        if municipality not in out[r[2]]:
            out[r[2]][municipality] = {}

        postal_code = r[12]
        if postal_code not in out[r[2]][r[1]]:
            out[r[2]][r[1]][postal_code] = {}

        if r[9]:
            street = r[9]

        elif r[10]:
            street = r[10]

        else:
            continue

        if street not in out[r[2]][r[1]][r[12]]:
            out[r[2]][r[1]][r[12]][street] = {}

        lon = round(float(r[6]), 7)
        lat = round(float(r[7]), 7)

        if r[11]:
            house = r[11]
            out[r[2]][r[1]][r[12]][street][house] = {}

            out[r[2]][r[1]][r[12]][street][house]['lon'] = lon
            out[r[2]][r[1]][r[12]][street][house]['lat'] = lat

        else:
            out[r[2]][r[1]][r[12]][street]['lon'] = lon
            out[r[2]][r[1]][r[12]][street]['lat'] = lat

    file_util.write_dict_as_json(
        './json/godi_data/{}.json'.format(file_name), out)


def full_data(file_name):

    data = _open_file_and_skip_header(file_name)

    out = {}

    for r in data:
        province = r[2]
        if province not in out:
            out[province] = {}

        municipality = r[1]
        if municipality not in out[r[2]]:
            out[r[2]][municipality] = {}

        postal_code = r[12]
        if postal_code not in out[r[2]][r[1]]:
            out[r[2]][r[1]][postal_code] = {}

        building_use = r[3]
        if building_use not in out[r[2]][r[1]][r[12]]:
            out[r[2]][r[1]][r[12]][building_use] = {}

        building_code = r[0]
        if building_code not in out[r[2]][r[1]][r[12]][r[3]]:
            out[r[2]][r[1]][r[12]][r[3]][building_code] = {}

        # building_code,municipality,province,use,longitude_ETRSTM35FIN, 4
        # latitude_ETRSTM35FIN,longitude_wgs84,latitude_wgs84,address_number,street_finnish, 9
        # street_swedish,street_number,postal_code,voting_area,voting_area_name_finnish, 14
        # voting_area_name_swedish 14

        building = out[r[2]][r[1]][r[12]][r[3]][building_code]

        address = {}
        if r[9]:
            address['fin'] = r[9]
        if r[10]:
            address['swe'] = r[10]
        if r[11]:
            address['no'] = r[11]

        if address:
            if 'addresses' not in building:
                building['addresses'] = []
            building['addresses'].append(address)

        building['coord'] = {}
        building['coord']['ETRS'] = {'lon': r[4], 'lat': r[5]}
        building['coord']['WGS84'] = {'lon': r[6], 'lat': r[7]}

        if r[13]:
            building['va_code'] = r[13]

        if r[14]:
            building['va_fin'] = r[14]

        if r[15]:
            building['va_swe'] = r[15]

    file_util.write_dict_as_json(
        './json/full_data/{}.json'.format(file_name), out)


def _open_file_and_skip_header(file_name):
    print('Opening csv file... {}'.format(file_name))
    data = file_util.open_csv('./csv/' + file_name + '.csv')
    print('Csv file opened succesfully')

    # skip header row
    data = iter(data)
    next(data)

    return data
