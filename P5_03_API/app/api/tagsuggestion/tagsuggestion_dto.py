from flask_restx import Namespace, fields, reqparse, inputs


class TagSuggestionDTO:
    # Tags Suggestion namespace declaration
    ns = Namespace('Tags Suggestion', description="Tag Suggestion system for StackOverflow's new posts.")

    # Input question model
    post_in = ns.model('input_post', {
        'title': fields.String(description='Post title', required=True),
        'body': fields.String(description='Post body', required=True),
    })
    # output tags model
    tags_out = ns.model('output_tags', {
        'post': fields.String(description='Input post'),
        'tags': fields.List(fields.String(), description='Predicted tags', required=True)
    })

    # Tags Suggestion request params
    post_args = reqparse.RequestParser()
    post_args.add_argument('return-post', type=inputs.boolean, default=True, required=False, help='If False it returns only the tags list.')
