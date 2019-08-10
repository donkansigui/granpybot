"""This Api will be used with the Wikipedia Module"""
import wikipedia

class WikipediaApi:
    """Class for the Wiki Media Api"""
    def __init__(self):
        """setting the language"""
        wikipedia.set_lang('fr')

    def get_data(self, title):
        """Searching for a page untitled as the title param
        and returning the first 3 sentences of the content and
        the URL
        NOTE : To avoid DisambiguationError we search for the list of matching titles
        and only go for the page of the first element
        """

        try:
            titles = wikipedia.search(title)
            page = wikipedia.page(titles[0])
            url = page.url
            wiki = wikipedia.summary(titles[0], sentences=3)
            result = {"text": wiki, "url": url}
            return result
        except wikipedia.exceptions.DisambiguationError:
            result = {"text": '', "url": False}
            return result