import json
from flask_ngrok import run_with_ngrok
from flask import Flask, request, redirect, g, render_template, session
import requests
from urllib.parse import quote
from index import *

app = Flask(__name__)
run_with_ngrok(app)

#  Client Keys
CLIENT_ID = "2cfcc859fc414051a5a08c69f6825674"
CLIENT_SECRET = "07b6e8799395496b992634075a639874"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "user-top-read"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}


@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback/q")
def callback():
    # efresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    # using the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    # profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    print(profile_response)
    profile_data = json.loads(profile_response.text)
    user = profile_data['display_name']

    # user top tracks data
    playlist_api_endpoint = "{}/me/top/tracks".format(SPOTIFY_API_URL)
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)
    
    dataset = retrieve_spotify_data(playlist_data)
    words = get_processed_dataset(dataset, False)
    words_sentiment = get_processed_dataset(dataset, True)
    
    emotions = get_emotion(" ".join(words_sentiment))

    array = {'words': {}}
    lyrics = {}
    for name in words:
        name.strip()
        if name in lyrics:
            lyrics[name]["freq"] = lyrics[name]["freq"] + 1
        else:
            lyrics[name] = {"freq": 1.0}
    array['words'] = lyrics

    # most common words and word cloud
    df_freq = pd.DataFrame(data=array['words'])
    df_freq = df_freq.T
    df_freq = df_freq.sort_values(by='freq', ascending=False)
    df_freq_plot = df_freq.head(35)
    df_freq_plot.plot.barh(title="Most frequent words in your top tracks")
    plot.savefig('C:/Users/lilac/PycharmProjects/spotify-sentiment-analysis/app/static/images/words.png')
    create_word_cloud(" ".join(words), "C:/Users/lilac/PycharmProjects/spotify-sentiment-analysis/recordPlayer.jpg")

    # pie chart of sentiments
    colors = ['#eae892', '#4d52dd', '#3f705c', '#a5aac2', '#96c78a', '#1775cb']
    new_dataframe = {'emotions': [], 'values': []}
    for i in emotions:
        new_dataframe['emotions'].append(i)
        new_dataframe['values'].append(emotions[i])
    df_emotions = pd.DataFrame(data=new_dataframe, index=new_dataframe['emotions'])
    explode = (0, 0, 0, 0.3, 0, 0)
    df_emotions.plot.pie(y='values', colors=colors, figsize=(5, 5), labels=new_dataframe['values'], explode=explode,
                         shadow=True)
    plot.title("Sentiment analysis of your top tracks")
    plot.legend(new_dataframe['emotions'], loc=10)
    plot.savefig('C:/Users/lilac/PycharmProjects/spotify-sentiment-analysis/app/static/images/plot.png')

    return render_template("index.html", user=user, name1='Most Frequent Words', url1='/static/images/words.png',
                           name2='Your Word Cloud', url2='/static/images/wordCloud.png',
                           name3='Sentiment Analysis of Top Tracks', url3='/static/images/plot.png')


if __name__ == "__main__":
    app.run()
