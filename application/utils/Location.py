import requests

def getLocation(ip_address):
    url = 'https://get.geojs.io/v1/ip/geo/'+ip_address+'.json'

    geo_request = requests.get(url)
    geo_data = geo_request.json()

    return geo_data