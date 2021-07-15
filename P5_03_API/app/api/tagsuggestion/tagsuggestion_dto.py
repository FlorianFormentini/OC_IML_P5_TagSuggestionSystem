from flask_restx import Namespace, fields, reqparse, inputs


class TagSuggestionDTO:
    # Tags Suggestion namespace declaration
    ns = Namespace('Tags Suggestion', description='Suggests tags for a given message.')

    # Input question model
    post_in = ns.model('message', {
        'title': fields.String(description='Post title', required=True),
        'body': fields.List(fields.String(), description='Post body', required=True),
    })
    # output tags model
    tags_out = ns.model('message', {
        'tags': fields.List(fields.String(), description='Predicted tags', required=True),
        'post': fields.List(fields.String(), description='Intents responses')
    })

    # Tags Suggestion request params
    post_args = reqparse.RequestParser()
    post_args.add_argument('return-post', type=inputs.boolean, default=False, required=False)
