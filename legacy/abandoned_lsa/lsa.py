"""
This is not my personal implementation of lsa, I picked it from site:
https://www.datacamp.com/community/tutorials/discovering-hidden-topics-python
"""

from pprint import pprint

from gensim import corpora
from gensim.models import LsiModel
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from os.path import join

from config import resources
from tools.read.yml import read_segments_texts


def preprocess_data(doc_set):
    """
    Input  : document list
    Purpose: preprocess text (tokenize, removing stopwords, and stemming)
    Output : preprocessed text
    """
    # Initialize regex tokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    # Create English stop words list
    en_stop = set(stopwords.words('english'))
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    # List for tokenized documents in loop
    texts = []
    # Loop through document list
    for i in doc_set:
        # Clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)
        # Remove stop words from tokens
        stopped_tokens = [i for i in tokens if i not in en_stop]
        # Stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        # Add tokens to list
        texts.append(stemmed_tokens)
    return texts


def prepare_corpus(doc_clean):
    """
    Input  : clean document
    Purpose: create term dictionary of our corpus and Converting list of documents (corpus) into Document Term Matrix
    Output : term dictionary and Document Term Matrix
    """
    # Creating the term dictionary of our corpus, where every unique term is
    # Assigned an index. dictionary = corpora.Dictionary(doc_clean)
    dictionary = corpora.Dictionary(doc_clean)
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    # Generate LDA model
    return dictionary, doc_term_matrix


def create_gensim_lsa_model(doc_clean, number_of_topics, words):
    """
    Input  : clean document, number of topics and number of words associated with each topic
    Purpose: create LSA model using gensim
    Output : return LSA model
    """
    dictionary, doc_term_matrix = prepare_corpus(doc_clean)
    # Generate LSA model
    lsa_model = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word=dictionary)  # train model
    pprint(lsa_model.print_topics(num_topics=number_of_topics, num_words=words))
    return lsa_model


def main():

    topics_count = 8
    topics_length = 4

    docs_list = read_segments_texts(join(resources, 'annotations'))
    clean_text = preprocess_data(docs_list)
    model = create_gensim_lsa_model(clean_text, topics_count, topics_length)
    
    X_topics = model.get_topics()
    model.get_topics()
    pprint(X_topics)
