from io import BytesIO
import requests
from PIL import Image
import sys
from functions import *

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
address = get_coords(' '.join(sys.argv[1:]))
address_ll = ','.join(map(str, address))
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}
response = requests.get(search_api_server, params=search_params)
if not response:
    exit(0)
json_response = response.json()
pharmacies = []
for org in json_response["features"]:
    dop = org["geometry"]["coordinates"]
    dis = (address[0] - dop[0]) ** 2 + (address[1] - dop[1]) ** 2
    org_name = org["properties"]["CompanyMetaData"]["name"]
    org_address = org["properties"]["CompanyMetaData"]["address"]
    try:
        org_time = org["properties"]["CompanyMetaData"]["Hours"]['text']
    except KeyError:
        org_time = False
    pharmacies.append({'name': org_name,
                       'address': org_name,
                       'time': org_time,
                       'dis': dis,
                       'org': org,
                       'coords': dop})
pharmacies.sort(key=lambda x: x['dis'])
pt = []
for v, i in enumerate(pharmacies[:10]):
    if not i['time']:
        pt.append('{coords0},{coords1},pm2grm{i}'.format(coords0=i['coords'][0],
                                                         coords1=i['coords'][1],
                                                         i=v + 1))
        continue
    try:
        org = i['org']
        TwentyFourHours = org["properties"]["CompanyMetaData"]["Hours"]["Availabilities"][0]["TwentyFourHours"]
        if TwentyFourHours:
            pt.append('{coords0},{coords1},pm2gnm{i}'.format(coords0=i['coords'][0],
                                                             coords1=i['coords'][1],
                                                             i=v + 1))
    except KeyError:
        pt.append('{coords0},{coords1},pm2blm{i}'.format(coords0=i['coords'][0],
                                                         coords1=i['coords'][1],
                                                         i=v + 1))
map_params = {
    "ll": address_ll,
    "l": "map",
    "pt": '~'.join(pt)
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(response.content)).show()
