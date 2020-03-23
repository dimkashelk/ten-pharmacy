import requests
import math


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b
    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)
    return distance


def get_coords(place):
    apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
    map_request = f"https://geocode-maps.yandex.ru/1.x/?geocode={place}&apikey={apikey}&format=json"
    response = requests.get(map_request)
    if not response:
        print('Try again...')
        exit(0)
    json_response = response.json()
    try:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    except IndexError:
        print('Try again...')
        exit(0)
    x, y = map(float, toponym["Point"]["pos"].split())
    return x, y


def get_size(place):
    y, x = get_coords(place)
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    address_ll = f"{x},{y}"
    search_params = {
        "apikey": api_key,
        "text": place,
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }

    res = requests.get(search_api_server, params=search_params)
    if not res:
        print('Not correct answer')
        print(res)
        exit(0)
    json_res = res.json()
    dop = json_res['properties']['ResponseMetaData']['SearchRequest']['boundedBy']
    y_size, x_size = abs(dop[0][0] - dop[1][0]), abs(dop[0][1] - dop[1][1])
    return y, x, [y_size, x_size]
