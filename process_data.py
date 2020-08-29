import os


# removes stop-words and extra characters from string and formats the string into corpus
def strip_data(string):
    string = string.lower().replace(r"(http|@)\S+", "").replace(r"’", "'").replace(r"[^a-z\':_]", "") \
        .replace("\n", ' ').replace('\u2005', ' ').replace('•', ' ')
    stop_chars = ['(', ')', '&', '\'', '\"', ',', '[', ']', ':', '—', '-', '1', '2', '3', '4', '5',
                  '6', '7', '8', '9', '0', '.', '/', '?']
    for char in stop_chars:
        string = string.replace(char, "")
    file = open("C:/Users/lilac/PycharmProjects/spotify-sentiment-analysis/stop-words.txt", 'r', encoding='cp850')

    stop_words = []
    for line in file.readlines():
        stop_words.append(line.strip())
    words = []
    for word in string.split():
        if word not in stop_words:
            words.append(word)
    return words


# removes stop-words and extra characters and formats the string into corpus for sentiment analysis
def clean_data(string):
    string = string.lower()

    stop_chars = ['(', ')', '&', '\'', '\"', ',', '[', ']', ':', '—', '-', '1', '2', '3', '4', '5',
                  '6', '7', '8', '9', '0', '.', '/', 'na']
    for char in stop_chars:
        string = string.replace(char, "")

    file = open('C:/Users/lilac/PycharmProjects/spotify-sentiment-analysis/stop-words.txt', 'r', encoding='cp850')
    stop_words = []
    for line in file.readlines():
        stop_words.append(line.strip())

    sentences = []
    for sentence in string.split("\n"):
        words = sentence.split()
        final_string = ''
        for word in words:
            if word not in stop_words:
                final_string = final_string + " " + word
        if final_string != '':
            sentences.append(final_string.strip())
    return sentences


# reads data from a text file and returns array
def read_data(url):
    file = open(url, 'r')
    words = []
    for line in file.readlines():
        words.append(line.strip())
    return words


# removes cached spotify access keys
def clear_cache():
    os.remove(".spotipyauthcache")
