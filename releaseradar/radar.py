import datetime

import spotipy


def find_artist(name):
    results = client.search(q='artist:' + name, type='artist')
    return results['artists']['items']


def get_artist_albums_released_after_date(client, artist, comparison_date):
    results = client.artist_albums(artist)
    all_albums = results['items']
    relevant_albums = []

    while results['next']:
        results = client.next(results)
        all_albums.extend(results['items'])

    for album in all_albums:
        if album['release_date_precision'] != 'day':
            continue

        release_date = datetime.datetime.strptime(
            album['release_date'], '%Y-%m-%d').date()
        if release_date < comparison_date:
            continue

        relevant_albums.append(album)

    return relevant_albums


if __name__ == '__main__':
    client = spotipy.Spotify(
        client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())

    artist = 'spotify:artist:762310PdDnwsDxAQxzQkfX'
    comparison_date = datetime.date(2016, 7, 1)
    albums = get_artist_albums_released_after_date(
        client, artist, comparison_date)

    for album in albums:
        print(album['release_date'], album['name'], album['type'])
