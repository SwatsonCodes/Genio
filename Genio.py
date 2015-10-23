import requests
from RdioArtistVerifier import RdioArtistVerifier


class Genio:

    def __init__(self):
        self.genius_base_url = "http://api.genius.com/"
        self.auth_header = {"Authorization": "Bearer heOS7t124GoomESzHUywrt7YhAaYYhI7eVygSoULIOhA0QXzc98jIU5hSascfFvm"}
        self.artist_verifier = RdioArtistVerifier()

    # Returns the id associated with the given artist, if it can be found.
    # Unfortunately the Genius API only supports searching for songs, so
    # the best workaround I can figure is to get the artist ID associated
    # with the top song result
    def get_artist_id(self, artist_name):
        print('getting artist id')
        r = requests.get(url=self.genius_base_url + "search",
                         params={"q": artist_name},
                         headers=self.auth_header)
        result = r.json()
        if result['meta']['status'] != 200:
            raise Exception("Artist ID lookup failed with code " + str(result['meta']['status']))
        if result['response']['hits']:
            top_hit = result['response']['hits'][0]['result']['primary_artist']
        else:
            raise Exception("No results found for artist " + artist_name)
        if top_hit['name'].lower() != artist_name.lower():
            raise Exception("Could not associate \'%s\' with an artist ID" % artist_name)
        return top_hit['id']


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

    def extract_artists_from_song(self, song_id, num_referents=200, artists_counts={}):
        print('extracting from song')
        r = requests.get(url=self.genius_base_url + "referents",
                         params={'song_id': song_id,
                                 'per_page': num_referents},
                         headers=self.auth_header)
        result = r.json()
        if result['meta']['status'] != 200:
            raise Exception("Failed to fetch song %s with error code %s" % (str(song_id), str(result['meta']['status'])))
        if result['response']['referents'] is []:
            return artists_counts

        for referent in result['response']['referents']:
            for annotation in referent['annotations']:
                self.extract_artists_from_annotation(annotation['body']['dom'], artists_counts)
        return artists_counts # XXX remove this?


    def extract_artists_from_annotation(self, annotation, artist_counts={}):
        if type(annotation) is not dict or 'tag' not in annotation:
            return
        if annotation['tag'] == 'a':
            self.__extract_all_children(annotation['children'], artist_counts)
        elif 'children' in annotation:
            for child in annotation['children']:
                self.extract_artists_from_annotation(child, artist_counts)


    def __extract_all_children(self, link_dom, artist_counts):
        for doc in link_dom:
            if type(doc) is dict and 'children' in doc:
                self.__extract_all_children(doc['children'], artist_counts)
            elif type(doc) is str \
                    and doc.strip() is not '' \
                    and doc[:4] != 'http' \
                    and self.artist_verifier.exists(doc):
                if doc in artist_counts:
                    artist_counts[doc] = artist_counts[doc] + 1
                else:
                    artist_counts[doc] = 1
        return artist_counts


    def find_related_artists(self, artist):
        artist_id = self.get_artist_id(artist)
        songs = self.get_artist_song_ids(artist_id)
        for song in songs:
            related_artist_counts = self.extract_artists_from_song(song)
        print(related_artist_counts)
        return related_artist_counts


test = Genio()
test.find_related_artists('Yung Lean')


