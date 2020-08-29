import paralleldots

PARALLELDOTS_API_KEY = 'RShBsDAdsdB8r4F7TMsZtTmRCSpjatbu1pxG0IMcjOg'

paralleldots.set_api_key(PARALLELDOTS_API_KEY)


def get_emotion(string):
    value_returned = paralleldots.emotion(string)
    if 'emotion' in value_returned:
        return value_returned['emotion']
    return None
