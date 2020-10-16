import re

import nltk

from preprocessing.preprocessing import preprocess_sentence


def do_labeling(text: str, dictionary: dict):
    processed_text = preprocess_sentence(text)
    for i in range(len(processed_text)):
        for label in dictionary:
            if processed_text[i] in dictionary[label]:
                processed_text[i] = label
    return " ".join(processed_text)


def dictionary_to_bag(dictionary: dict):
    bag = []
    bag.extend(dictionary)
    for label in dictionary:
        bag.extend([token for token in dictionary[label]])
    return set(bag)


def convert_dictionary(dictionary: dict):
    rules = []
    for label in dictionary:
        new_labels = [f"'{token}'" for token in dictionary[label]]
        rules.append(f"{label} -> {' | '.join(new_labels)}")
    return "\n".join(rules)


def extend_dictionary(dictionary: dict):
    for label in dictionary:
        synonyms = []
        for word in dictionary[label]:
            for syn_set in nltk.corpus.wordnet.synsets(word):
                for lem in syn_set.lemmas():
                    synonyms.append(re.sub(r"_", r" ", lem.name().lower()))
        dictionary[label].update(synonyms)
    return dictionary
