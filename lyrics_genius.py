import lyricsgenius

GENIUS_CLIENT_ACCESS_TOKEN = ""

genius = lyricsgenius.Genius(GENIUS_CLIENT_ACCESS_TOKEN)


# returns lyrics from specified song and artist
def get_song_lyrics(song_name, artist):
    song = genius.search_song(song_name, artist)
    if song is not None:
        return song.lyrics
    return ""
