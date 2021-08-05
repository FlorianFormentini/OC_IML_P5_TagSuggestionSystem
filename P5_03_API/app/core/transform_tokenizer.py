"""
This file contains the custom class used to tokenize text documents from the research notebooks.
It's necessary to load the vectorizer coming from the same notebook.
It also has to be outside the app.
"""

import nltk
from nltk.stem import lancaster, WordNetLemmatizer


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
