import requests
import aiohttp

class RdioArtistVerifier:

    def __init__(self):
        self.access_token = self.__get_access_token()

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

    async def exists_async(self, artist):
        print('checking for existence')
        r = await aiohttp.post('https://services.rdio.com/api/1/',
                               data={'method': 'search',
                                     'query': artist,
                                     'types': 'artist'},
                               headers={'Content-Type': 'application/x-www-form-urlencoded',
                                        'Authorization': 'Bearer ' + self.access_token})
        if r.status != 200:
            raise Exception("Search for artist failed with error code %i" % r.status_code)
        result = await r.json()
        result = result['result']
        for i in range(min(5, result['number_results'])):
            if result['results'][i]['name'].lower() == artist.lower():
                return True
        print(artist +' does not exist')
        return False


