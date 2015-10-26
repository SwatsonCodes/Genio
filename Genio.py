import requests
import asyncio
import aiohttp
import operator
from RdioArtistVerifier import RdioArtistVerifier


class Genio:

    def __init__(self):
        self.genius_base_url = "http://api.genius.com/"
        self.auth_header = {"Authorization": "Bearer heOS7t124GoomESzHUywrt7YhAaYYhI7eVygSoULIOhA0QXzc98jIU5hSascfFvm"}
        self.artist_verifier = RdioArtistVerifier()
        self.artist_counts ={}

    # Returns the id associated with the given artist, if it can be found.
    # Unfortunately the Genius API only supports searching for songs, so
    # the best workaround I can figure is to try to find the artist id within
    # the top 5 song results
    def get_artist_id(self, artist_name):
        print('getting artist id')
        r = requests.get(url=self.genius_base_url + "search",
                         params={"q": artist_name},
                         headers=self.auth_header)
        result = r.json()
        if result['meta']['status'] != 200:
            raise Exception("Artist ID lookup failed with code " + str(result['meta']['status']))
        if result['response']['hits']:
            artist_result =  None
            for i in range(min(5, len(result['response']['hits']))):
                cur_artist = result['response']['hits'][i]['result']['primary_artist']
                if cur_artist['name'].lower() == artist_name.lower():
                    artist_result = cur_artist
                    break
        else:
            raise Exception("No results found for artist " + artist_name)
        if artist_result is None:
            raise Exception("Could not associate \'%s\' with an artist ID" % artist_name)
        return artist_result['id']

    def get_artist_song_ids(self, artist_id, num_songs=25):
        print('getting song ids')
        r = requests.get(url=self.genius_base_url + 'artists/%s/songs' % artist_id,
                         params={'per_page': num_songs,
                                 'sort': 'popularity'},
                         headers=self.auth_header)
        result = r.json()
        if result['meta']['status'] != 200:
            raise Exception("Failed to fetch songs with error code " + str(result['meta']['status']))
        song_ids = [song['id'] for song in result['response']['songs']]
        return song_ids

    async def extract_artists_from_song(self, song_id, num_referents=200):
        r = await aiohttp.get(self.genius_base_url + 'referents',
                                    params={'song_id': song_id,
                                   'per_page': num_referents},
                                    headers=self.auth_header)

        result = await r.json()
        if result['meta']['status'] != 200:
            raise Exception("Failed to fetch song %s with error code %s" % (str(song_id), str(result['meta']['status'])))
        if result['response']['referents'] is []:
            self.artist_counts = {}
        coros = []
        for referent in result['response']['referents']:
            for annotation in referent['annotations']:
                coros.append(asyncio.Task(self.extract_artists_from_annotation(annotation['body']['dom'])))
        await asyncio.gather(*coros)


    async def extract_artists_from_annotation(self, annotation):
        if type(annotation) is not dict or 'tag' not in annotation:
            return

        if annotation['tag'] == 'a':
            link = annotation['attributes']['href']
            if link[:26] == "http://genius.com/artists/":
                artist_name = link[26:].replace('-', ' ')
                in_rdio = await self.artist_verifier.exists_async(artist_name)
                if in_rdio:
                    if artist_name in self.artist_counts:
                        self.artist_counts[artist_name] += 1
                    else:
                        self.artist_counts[artist_name] = 1

        if 'children' in annotation:
            for child in annotation['children']:
               await self.extract_artists_from_annotation(child)

    def __crawl_songs_async(self, artist):
        artist_id = self.get_artist_id(artist)
        songs = self.get_artist_song_ids(artist_id)
        coros = []
        for song in songs:
            coros.append(asyncio.Task(self.extract_artists_from_song(song)))
        yield from asyncio.gather(*coros)

    def find_related_artists(self, artist):
        self.artist_verifier.clear_radio_keys()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__crawl_songs_async(artist))
        print(self.artist_counts)
        related_artists = list(self.artist_counts.keys())
        related_artists.sort(key=lambda artist_name: self.artist_counts[artist_name], reverse=True)
        radio_keys = self.artist_verifier.get_radio_keys()
        sorted_keys = [radio_keys[r] for r in related_artists]
        return {'related_artists': related_artists, 'radio_keys': radio_keys}


# test = Genio()
# print(test.find_related_artists('yung lean'))