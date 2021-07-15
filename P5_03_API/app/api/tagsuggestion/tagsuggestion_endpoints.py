# from flask import request
from flask_restx import Resource

from ..utils import apikey_required
from .tagsuggestion_dto import TagSuggestionDTO
from .tagsuggestion_services import _tagsuggestion_services

# ns declaration is in DTO to avoid circular imports and because it have to be loaded before the routes
ns = TagSuggestionDTO.ns


@ns.route('/suggest')
class TagSuggestion(Resource):

    @apikey_required
    @ns.doc(security='apikey')
    @ns.expect([TagSuggestionDTO.post_in, TagSuggestionDTO.post_args])
    @ns.marshal_with(TagSuggestionDTO.tags_out)
    @ns.response(404, "Model or its vectorizer not found.")
    @ns.response(200, "Success.")
    def post(self):
        """Return the tags distribution for a given post (title + body)"""
        return _tagsuggestion_services.question_tags('')
