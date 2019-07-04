import requests

class GoogleMapApi:

    def __init__(self, key):
        self.url_static_map = "https://maps.googleapis.com/maps/api/staticmap"
        self.url_details = "https://maps.googleapis.com/maps/api/place/details/json"
        self.url_search = "https://maps.googleapis.com/maps/api/geocode/json"
        self.key = key

    def request_details(self, place_id):
        parameters = {"key" : self.key, "placeid" : place_id}
        get = requests.get(self.url_details, params = parameters).json()
        try:
            address = get['result']['formatted_address']
            routes = get['result']['address_components']
            route_name = get['result']['name']
            for route in routes:
                if route['types'][0] == 'route':
                    route_name = route['long_name']
                    break
            return {'address': address, 'route': route_name}

        except:
            return False

    def request_map(self, center, zoom, size):
        parameters = {"key": self.key, "center": center, "zoom": zoom, "size": size, "markers": center}
        get = requests.get(self.url_static_map, params=parameters)
        return get

    def request_search(self, place):
        parameters = {"key": self.key, "address": place, "language": 'fr', "region": "fr"}
        get = requests.get(self.url_search, params=parameters)
        if get.json()['status'] == 'OK':
            return {'place_id': get.json()['results'][0]['place_id']}
        return False
