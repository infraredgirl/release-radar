import datetime

import spotipy

from releaseradar import models


def find_artist(name):
    client = spotipy.Spotify(
        client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())
    results = client.search(q='artist:' + name, type='artist')
    for artist in results['artists']['items']:
        if artist['name'].lower() == name.lower():
            return models.Artist(
                name=artist['name'],
                spotify_uri=artist['uri'],
                spotify_url=artist['external_urls']['spotify']
            )


def get_artist_albums_released_after_date(artist_uri, comparison_date):
    client = spotipy.Spotify(
        client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())
    results = client.artist_albums(artist_uri)
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
    uri = 'spotify:artist:762310PdDnwsDxAQxzQkfX'
    comparison_date = datetime.date(2016, 7, 1)
    albums = get_artist_albums_released_after_date(uri, comparison_date)

    for album in albums:
        print(album['release_date'], album['name'], album['type'])
