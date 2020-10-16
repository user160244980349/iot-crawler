import re

import nltk


def convert_grammar(grammar: dict):
    return "\n".join([f"{r} -> {' | '.join([' '.join(grammar[r][i]) for i in range(len(grammar[r]))])}" for r in grammar])


def combine_grammars(grammars: tuple):
    return "\n".join(grammars)


def sentence_to_dictionary(sentence: str, exclude=None):
    text = nltk.word_tokenize(sentence)
    tags = nltk.pos_tag(text)
    dictionary = {}

    excluding_words = []
    if exclude is not None:
        excluding_words.extend(exclude)

    for tag in tags:
        if tag[0] not in excluding_words:
            dictionary[re.sub(r"\$", r"S", tag[1])] = []

    for tag in tags:
        if tag[0] not in excluding_words:
            dictionary[re.sub(r"\$", r"S", tag[1])].append(f"{tag[0]}")

    return dictionary
