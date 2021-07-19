import joblib
import re
import nltk
from nltk.stem import lancaster, WordNetLemmatizer
from flask import current_app


class TransformTokenizer:
    """ 'All in one' tokenizer. Tokenize and normalize (lemmatize or stem) a text corpus, depending on the given mode
    A RegEx can be used for the tokenisation.
    It's possible to use a custom lemmatizer/stemmer, defaults are WordNetLemmatizer or LancasterStemmer
    It's also possible to remove a custom list of stop words, or nltk stopwords for a given langage
    """

    def __init__(self, mode='lemma', normalizer=None, regex_pattern=None,
                 sw='english', used_postags=[]):
        """
        args:
            mode: {'lemma', 'stem'}, default='lemma' - normalization mode
            transformer: obj default=None - optional custom normalizer
            regexp_pattern: str, default=None - optional regxp for tokenization
            sw_lang: str, default='english' - stop words langage
            rmv_postags: list(str) - unused postags, to remove in the corpus
        """
        if mode and mode not in ['lemma', 'stem']:
            raise ValueError(":mode: must be 'lemma', 'stem' or None only.")
        # defines normalizer (custom or default) depending on the given mode
        self.mode = mode
        self.normalizer = normalizer or WordNetLemmatizer(
        ) if self.mode == 'lemma' else lancaster.LancasterStemmer()
        # defines regexptokenizer if pattern
        self.regexptokenizer = nltk.RegexpTokenizer(
            regex_pattern) if regex_pattern else None
        # defines stop words
        if sw and type(sw) == str:
            self.stop_words = nltk.corpus.stopwords.words(sw)
        elif sw and type(sw) == list:
            self.stop_words = sw
        self.used_postags = used_postags

    def __call__(self, doc):
        """
        args:
            doc: str - text document to tokenize
        output:
            list - tokenized document
        """
        # tokenization
        if self.regexptokenizer:
            tokens = self.regexptokenizer.tokenize(doc)
        else:
            tokens = nltk.word_tokenize(doc)
        # unused POStags removal
        if self.used_postags and tokens:
            postags = nltk.pos_tag(tokens)
            tokens = [x[0] for x in postags if (
                x[1] in self.used_postags) and (x[0] not in self.stop_words)]
        # Normalisation + stop words removal
        if self.mode == 'lemma':
            tokens = [self.normalizer.lemmatize(tkn) for tkn in tokens]
        elif self.mode == 'stem':
            tokens = [self.normalizer.stem(tkn) for tkn in tokens]
        return tokens


class TagSuggestion:

    def __init__(self, vect_path=current_app.config['VECT_PATH'], model_path=current_app.config['MODEL_PATH']):
        self.load_model(vect_path, model_path)

    def load_model(self, vect_path, model_path):
        """Loads the model (and his vectorizer) from the given paths
        args:
            vect_path: str, default=current_app.config['VECT_PATH'] - Vectorizer path, from the config file by default
            model_path: str, default=current_app.config['MODEL_PATH'] - Model path, from the config file by default
        Raise:
            FileNotFoundError - If a file is not found
        """
        print(vect_path, "\n", model_path)
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
        print(len(self.input_vect.get_feature_names()), post_matrix.shape)
        tags = self.model.predict(post_matrix)
        print("tags: ", tags)
        return self.output_vect.inverse_transform(tags), post_txt
