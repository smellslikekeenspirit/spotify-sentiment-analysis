import lyricsgenius

GENIUS_CLIENT_ACCESS_TOKEN = "wO6Ki6gZ57NAd0cTs5lwIJO_IwFeb4V1eOp8OziSWAfrdCr_x9DoEInS_NpHnyEo"

genius = lyricsgenius.Genius(GENIUS_CLIENT_ACCESS_TOKEN)


# returns lyrics from specified song and artist
def get_song_lyrics(song_name, artist):
    song = genius.search_song(song_name, artist)
    if song is not None:
        return song.lyrics
    return ""
