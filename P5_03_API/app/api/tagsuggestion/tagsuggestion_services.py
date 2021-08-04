from flask_restx import abort
from ...core.tagsuggestion_business import TagSuggestion


class tagsuggestionServices:

    def question_tags(self, data, return_post):
        try:
            # init models
            suggestor = TagSuggestion()
            tags, post = suggestor.suggest_tags(data['title'], data['body'])
            if return_post:
                return {'post': post, 'tags': tags}
            else:
                return {'tags': tags}
        except FileNotFoundError:
            abort(404, 'The model or a vectorizer was not found.')

    def model_params(self):
        params = {
            'tokenizer': {
                'type': 'TransformTokenizer (custom)',
                'regex': r"r'(?u)\b\w\w+\b'",
                'stop_words': 'NLTK english list',
                'keeped_POStags': ['NN', 'NNP', 'NNPS', 'NNS']
            },
            'vectorizer': {
                'type': 'TfidfVectorizer',
                'ngram_range': '(1,1) - unigrams',
                'min_df': 5,
                'max_df': 0.80,
            },
            'model': {
                'type': "OneVsRestClassifier(Logisticregression(solver='saga', penalty='l1', C=10))",
                'testset_F1': 0.662
            }
        }
        return params


# singleton object to use in the controllers
_tagsuggestion_services = tagsuggestionServices()
