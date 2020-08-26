"""
This is not my personal implementation of lsa, I picked it from site:
https://www.datacamp.com/community/tutorials/discovering-hidden-topics-python
"""
import gensim


def prepare_corpus_tfidf(documents):
    dictionary = gensim.corpora.Dictionary(documents)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in documents]
    tfidf = gensim.models.TfidfModel(doc_term_matrix, normalize=True)
    doc_term_matrix = tfidf[doc_term_matrix]
    return dictionary, doc_term_matrix


def prepare_corpus_bow(doc_clean):
    dictionary = gensim.corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    return dictionary, doc_term_matrix


def create_gensim_lsa_model(doc_clean, number_of_topics):
    dictionary, doc_term_matrix = prepare_corpus_tfidf(doc_clean)
    lsa_model = gensim.models.LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word=dictionary)
    return lsa_model
