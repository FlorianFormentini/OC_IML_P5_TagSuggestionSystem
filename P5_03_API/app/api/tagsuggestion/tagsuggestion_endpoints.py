from flask import request
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
    @ns.expect(TagSuggestionDTO.post_args, TagSuggestionDTO.post_in)
    @ns.marshal_with(TagSuggestionDTO.tags_out)
    @ns.response(404, "Model or a vectorizer not found.")
    @ns.response(200, "Success.")
    def post(self):
        """Return the tags distribution for a given post"""
        args = TagSuggestionDTO.post_args.parse_args()
        data = request.get_json()
        return _tagsuggestion_services.question_tags(data, args['return-post'])


@ns.route('/config')
class ModelParams(Resource):

    @apikey_required
    @ns.doc(security='apikey')
    @ns.response(500, "Wrong API key")
    @ns.response(200, "Success.")
    def get(self):
        """Return the used configuration"""
        return _tagsuggestion_services.model_params()
