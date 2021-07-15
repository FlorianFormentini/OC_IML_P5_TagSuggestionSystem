import joblib
from flask import current_app


class TagSuggestion:

    def __init__(self):
        self.load_model()

    def load_model(self, vect_path=current_app.config['VECT_PATH'], model_path=current_app.config['MODEL_PATH']):
        """Loads the model (and his vectorizer) from the given paths
        args:
            vect_path: str, default=current_app.config['VECT_PATH'] - Vectorizer path, from the config file by default
            model_path: str, default=current_app.config['MODEL_PATH'] - Model path, from the config file by default
        Raise:
            FileNotFoundError - If a file is not found
        """
        self.vectorizer = joblib.load(open(vect_path, 'rb'))
        self.model = joblib.load(open(model_path, 'rb'))
        print('> Model loaded')

    def __prepare_post(self, title, body):
        """Post text preparation
        args:
            title: str - Post title
            body: str - Post body
        Raise:
            post: str - Prepared post
        """
        pass

    def suggest_tags(self, title, body):
        """Predict tags for a given StackOverflow Post (title + body)
        args:
            title: str - Post title
            body: str - Post body
        Raise:
            tags: list(str) - Tags distribution (sorted by probability)
        """
        post_txt = self.__prepare_post(title, body)
        tags = self.model.predict(self.vectorizer(post_txt))
        return tags
