from flask import current_app
from flask_restx import abort
from werkzeug.exceptions import HTTPException

from ...core.tagsuggestion_business import TagSuggestion
from ..utils import file_upload


class tagsuggestionServices:

    def question_tags(self, data):
        try:
            # init models
            suggestor = TagSuggestion()
            suggestor.suggest_tags(data['title'], data['body'])
            return {'tags': []}
        except FileNotFoundError:
            abort(404, 'The model (or his vectorizer) was not found.')

    def upload_model(self, vect_file, model_file):
        try:
            # uploads files on the server and changes used path
            current_app.config['VECT_PATH'] = file_upload(vect_file)
            current_app.config['MODEL_PATH'] = file_upload(model_file)
            return {'message': 'Model successfully changed.'}
        except HTTPException as e:
            abort(400, e)
        except Exception as e:
            abort(500, e)


# singleton object to use in the controllers
_tagsuggestion_services = tagsuggestionServices()
