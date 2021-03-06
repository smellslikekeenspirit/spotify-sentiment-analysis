from wordcloud import WordCloud, STOPWORDS
import numpy
from PIL import Image
import random


# returns a random color variation of green
def green_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    colors = ['#228B22', '#008000', '#006400', '#32CD32', '#3CB371', '#2E8B57', '#6B8E23', '#556B2F']
    return colors[random.randint(0, 7)]


# returns a random color variation of green
def blue_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    colors = ['#F0F8FF', '#E6E6FA', '#B0E0E6', '#ADD8E6', '#87CEFA', '#87CEEB', '#00BFFF', '#B0C4DE', '#1E90FF',
              '#6495ED', '#4682B4', '#5F9EA0', '#7B68EE', '#6A5ACD', '#483D8B', '#4169E1', '#0000FF', '#0000CD',
              '#00008B', '#000080', '#191970', '#8A2BE2', '#4B0082']
    return colors[random.randint(0, len(colors) - 1)]


# creates a word cloud in the given shape from a string of words
def create_word_cloud(string, shape_url):
    mask_array = numpy.array(Image.open(shape_url))

    wc = WordCloud(background_color="black", max_words=1000, mask=mask_array, stopwords=set(STOPWORDS), margin=12,
                   random_state=1).generate(string)

    wc.recolor(color_func=blue_color_func, random_state=3)
    wc.to_file("C:/Users/lilac/PycharmProjects/spotify-sentiment-analysis/app/static/images/wordCloud.png")
