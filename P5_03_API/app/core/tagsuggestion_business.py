import joblib
import re
from flask import current_app

from transform_tokenizer import TransformTokenizer


class TagSuggestion:

    def __init__(self, vect_path=current_app.config['VECT_PATH'], model_path=current_app.config['MODEL_PATH']):
        # from ipynb.fs.full.P5_02_models import TransformTokenizer

        test = TransformTokenizer()
        print('test ok\n', test)
        self.load_model(vect_path, model_path)

    def load_model(self, vect_path, model_path):
        """Loads the model (and his vectorizer) from the given paths
        args:
            vect_path: str, default=current_app.config['VECT_PATH'] - Vectorizer path, from the config file by default
            model_path: str, default=current_app.config['MODEL_PATH'] - Model path, from the config file by default
        Raise:
            FileNotFoundError - If a file is not found
        """
        self.input_vect, self.output_vect = joblib.load(vect_path)
        self.model = joblib.load(model_path)
        print('> Model loaded')

    def __prepare_post(self, title, body):
        """Post text preparation
        args:
            title: str - Post title
            body: str - Post body
        Raise:
            post: csr_matrix - vectorized post
        """
        doc = title + ' ' + body
        # removes HTML tags
        doc = re.sub(r"<.*?>", ' ', doc)
        # replace HTML symbols (&quot; &lt; &gt; ...) by ' '
        doc = re.sub(r"&(\w+);", ' ', doc)
        return doc

    def suggest_tags(self, title, body):
        """Predict tags for a given StackOverflow Post (title + body)
        args:
            title: str - Post title
            body: str - Post body
            return_post: bool, default=False - Return post with tags if True
        Raise:
            tags: list(str) - Tags distribution (sorted by probability)
            tags: str, optionnal - Prepared post text
        """
        post_txt = self.__prepare_post(title, body)
        post_matrix = self.input_vect.transform([post_txt])
        tags_vect = self.model.predict(post_matrix)
        tags = self.output_vect.inverse_transform(tags_vect)[0]
        return list(tags), post_txt
