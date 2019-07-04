import wikipedia

class WikipediaApi:
    def __init__(self):
        wikipedia.set_lang('fr')

    def get_data(self, title):
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