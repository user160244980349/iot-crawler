
import nltk

from initialization.initialization import initialize
from synonymuos_search import grammar, labels
from synonymuos_search.grammatics import combine_grammars, sentence_to_dictionary, convert_grammar
from synonymuos_search.wordpools import convert_dictionary, dictionary_to_bag, do_labeling


def main():

    initialize()

    # sentence = "you give us information about your location"
    # sentence = "you give information honestly and immediately"
    # sentence = "we collecting and storing information permanently"
    # sentence = "you thinking and we are collecting information honestly"
    sentence = "All work and no play makes jack dull boy"
    # sentence = "we may also collect technical information to help us identify your device for fraud prevention and diagnostic purposes"

    labeled_sentence = do_labeling(sentence, labels.dictionary)
    sentence_dictionary = sentence_to_dictionary(labeled_sentence, dictionary_to_bag(labels.dictionary))
    nltk_grammar = combine_grammars((
        convert_grammar(grammar.glob),
        convert_dictionary(sentence_dictionary),
    ))

    print(f"\n # ==================== #\n"
          f" # NLTK GRAMMAR IS      #\n"
          f" # ==================== #\n\n"
          f"{nltk_grammar}")

    binary_grammar = nltk.CFG.fromstring(nltk_grammar)
    rd_parser = nltk.RecursiveDescentParser(binary_grammar)

    print("\n # ===================== #\n"
          " # SENTENCES TREES ARE   #\n"
          " # ===================== #\n")

    labeled_tokens = labeled_sentence.split()
    for tree in rd_parser.parse(labeled_tokens):
        print(tree)
