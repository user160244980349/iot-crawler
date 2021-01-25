import re

from nltk import pos_tag, WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def wordnet_tag(tag: str):
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag[0], wordnet.NOUN)


def preprocess_sentence(sentence):
    lemmatizer = WordNetLemmatizer()
    sentence = sentence.lower()
    tokens = word_tokenize(sentence)
    tags = pos_tag(tokens)
    stop_words = stopwords.words('english')
    stop_words.extend(["us"])
    lemmas = []
    for tag in tags:
        if tag[0] not in stop_words:
            lemmas.append(lemmatizer.lemmatize(tag[0], pos=wordnet_tag(tag[1])))
        else:
            lemmas.append(tag[0])
    return lemmas


def preprocess_document(document: str, preprocess: tuple):
    # Loop through document list and apply preprocess functions
    sentences = re.split(r"\.\s+|\.\n+|!|\?", document)
    # List for tokenized documents in loop
    clean_sentences = []
    for sentence in sentences:
        for p in preprocess:
            sentence = p(sentences)
        clean_sentences.append(preprocess_sentence(sentence))
    return clean_sentences
