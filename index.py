from lyrics_genius import get_song_lyrics
from process_data import clean_data, strip_data


def retrieve_spotify_data(playlist):
    songs = ""
    for item in playlist['items']:
        artist = item["artists"][0]["name"]
        song_name = item['name']
        songs += get_song_lyrics(song_name, artist)
    return songs


def get_processed_dataset(dataset, sentiment_analysis):
    processed_dataset = clean_data(dataset) if sentiment_analysis else strip_data(dataset)
    return processed_dataset
