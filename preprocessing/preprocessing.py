import nltk

from tools.text import remove_spec_chars, remove_spaces, remove_newlines


def preprocess_documents(documents):
    # Create English stop words list
    stop_words = set(nltk.corpus.stopwords.words("english"))
    # Create p_stemmer of class PorterStemmer
    stemmer = nltk.PorterStemmer()

    preprocess = [
        remove_spec_chars,
        remove_spaces,
        remove_newlines,
    ]

    # Loop through document list
    segments = []
    for d in documents:
        doc_text = d.lower()
        for p in preprocess:
            doc_text = p(doc_text)
        segments.extend(doc_text.split("\n"))

    # List for tokenized documents in loop
    clean_docs = []
    for segment in segments:
        # Clean and tokenize document string
        tokens = nltk.word_tokenize(segment)
        # Remove stop words from tokens
        stopped_tokens = [i for i in tokens if i not in stop_words]
        # Stem tokens
        stemmed_tokens = [stemmer.stem(i) for i in stopped_tokens]
        # Add tokens to list
        clean_docs.append(stemmed_tokens)

    print(f"Total amount of docs is {len(clean_docs)}")
    return clean_docs