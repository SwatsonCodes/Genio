import requests
import aiohttp
import time

class RdioArtistVerifier:

    def __init__(self):
        self.access_token = self.__get_access_token()
        self.radio_keys = {}
        self.artist_images = {}

    def __get_access_token(self):
        client_credentials = 'd2Fnd3JvZmlrZmRiNWpveTYzYjQ1NjZvY2k6QTV6UEJva0ZXSGhzQ3lkRGs5VHhKQQ=='

        r = requests.post(url='https://services.rdio.com/oauth2/token',
                          data={'grant_type': 'client_credentials'},
                          headers={'Content-Type': 'application/x-www-form-urlencoded',
                                   'Authorization': 'Basic ' + client_credentials})
        if r.status_code != 200:
            raise Exception("Failed to get Rdio access token with error code %i" % r.status_code)
        return r.json()['access_token']

    def exists(self, artist):
        print('checking for existence')
        r = requests.post(url='https://services.rdio.com/api/1/',
                          data={'method': 'search',
                                'query': artist,
                                'types': 'artist'},
                          headers={'Content-Type': 'application/x-www-form-urlencoded',
                                   'Authorization': 'Bearer ' + self.access_token})
        if r.status_code != 200:
            raise Exception("Search for artist failed with error code %i" % r.status_code)
        result = r.json()['result']
        for i in range(min(5, result['number_results'])):
            if result['results'][i]['name'].lower() == artist.lower():
                return True
        print(artist +' does not exist')
        return False

    async def exists_async(self, artist, gather_radio_keys=True, gather_images=True):
        print('checking for existence')
        r = await aiohttp.post('https://services.rdio.com/api/1/',
                               data={'method': 'search',
                                     'query': artist,
                                     'types': 'artist'},
                               headers={'Content-Type': 'application/x-www-form-urlencoded',
                                        'Authorization': 'Bearer ' + self.access_token})
        if r.status != 200:
            raise Exception("Search for artist failed with error code %i" % r.status)
        result = await r.json()
        result = result['result']
        for i in range(min(5, result['number_results'])):
            cur_result = result['results'][i]
            if cur_result['name'].lower() == artist.lower():
                if gather_radio_keys:
                    self.radio_keys[artist] = cur_result['topSongsKey'] if 'topSongsKey' in cur_result else None
                if gather_images:
                    self.artist_images[artist] = self.__clean_image_url(cur_result['dynamicIcon'])
                return True
        print(artist +' does not exist')
        return False

    def __clean_image_url(self, url):
        url = url[:url.find('boxblur')] + url[url.find('colorize'):]
        url = url[:url.find('pad')] + url[url.find('overlay'):]
        url += '&h=50'
        return url

    def get_radio_keys(self):
        return self.radio_keys

    def clear_radio_keys(self):
        self.radio_keys = {}

    def get_artist_images(self):
        return self.artist_images

    def clear_artist_images(self):
        self.artist_images = {}



