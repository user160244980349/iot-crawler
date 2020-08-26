from pprint import pprint

from initialization import initialization
from lsa.lsa import create_gensim_lsa_model
from preprocessing.preprocessing import preprocess_documents
from tools.read.html import read_segments_in_html
# from tools.read.yml import read_segments_in_yaml


def main():
    # Initializing nltk
    initialization.initialize()

    topics_count = 10
    topics_length = 4

    docs_list = read_segments_in_html("datasets/OPP-115/sanitized_policies")
    # docs_list = read_segments_in_yaml("datasets/APP-350_v1.1/annotations")

    clean_docs = preprocess_documents(docs_list)
    model = create_gensim_lsa_model(clean_docs, topics_count)
    pprint(model.print_topics(num_topics=topics_count, num_words=topics_length))


if __name__ == "__main__":
    main()
