from flask_restx import abort

from ...core.tagsuggestion_business import TagSuggestion


class tagsuggestionServices:

    def question_tags(self, data):
        try:
            # init models
            suggestor = TagSuggestion()
            suggestor.suggest_tags(data['title'], data['body'])
            return {'tags': []}
        except FileNotFoundError:
            abort(404, 'The model (or his vectorizer) was not found.')


# singleton object to use in the controllers
_tagsuggestion_services = tagsuggestionServices()
