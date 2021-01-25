import nltk


def initialize():
    nltk_setup()


def nltk_setup():
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')
