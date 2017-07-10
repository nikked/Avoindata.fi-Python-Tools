from . import etrs_to_wgs84, google_geocoder
from geopy.distance import great_circle


def test(northern, eastern, address):
    from_etrs = etrs_to_wgs84.etrs_to_wgs84(northern, eastern)
    from_google = google_geocoder.query_address_data(address)
    calculate_distance_between_coordinates(from_etrs, from_google)


def calculate_distance_between_coordinates(from_etrs, from_google):
    etrs = (from_etrs[0], from_etrs[1])
    google = (from_google[0], from_google[1])

    print(etrs)
    print(google)
    print(great_circle(etrs, google).meters)
