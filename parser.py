import re
from files import STOPWORDS


class Parser():

    def __init__(self):
        pass

    @staticmethod
    def parse_sentence(string):

        result = ''
        if len(string) > 99:
            return result
        words = string.split()
        for word in words:
            try:
                if int(word):
                    if not result:
                        result += word
                    else:
                        result += ' ' + word
            except ValueError:
                if len(word) > 2 and word not in STOPWORDS:
                    # This part is to get ride of apostrophe
                    word = word.split("'")
                    if not result:
                        result += word[-1]
                    else:
                        result += ' ' + word[-1]
        return result

    @staticmethod
    def remove_number(string):

        result = ''
        words = string.split()
        for word in words:
            try:
                int(word)
            except ValueError:
                if not result:
                    result += word
                else:
                    result += ' ' + word
        return result

    @staticmethod
    def remove_titles(string):

        sentence = re.sub("={2}\s.*\s={2}\s", "", string)
        return sentence