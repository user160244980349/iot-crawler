
glob = {

    # ========================================
    # CORE GRAMMAR FOR DOCUMENT
    # ========================================

    # document
    "DOCUMENT":
        # recursion
        [["SENTENCE", "DOCUMENT"], ["SENTENCE"]],

    # sentence
    "SENTENCE":
        # sentence base
        [["NOUN_PHRASE_GROUP", "VERB_PHRASE_GROUP"]],

    # group of verb phrases
    "VERB_PHRASE_GROUP":
        # recursion
        [["VERB_PHRASE"],
         ["VERB_PHRASE", "VERB_PHRASE_GROUP"],
         ["VERB_PHRASE", "CC", "VERB_PHRASE_GROUP"],
         # group attributes
         ["VERB_PHRASE", "ADVERB_PHRASE_GROUP"],
         ["VERB_PHRASE", "PREPOSITION_PHRASE_GROUP"],
         ["VERB_PHRASE", "PREPOSITION_PHRASE_GROUP", "ADVERB_PHRASE_GROUP"]],

    # group of noun phrases
    "NOUN_PHRASE_GROUP":
        # recursion
        [["NOUN_PHRASE"],
         ["NOUN_PHRASE", "NOUN_PHRASE_GROUP"],
         ["NOUN_PHRASE", "CC", "NOUN_PHRASE_GROUP"],
         # group attributes
         ["ADJECTIVE_PHRASE_GROUP", "NOUN_PHRASE"]],

    # group of adjective phrases
    "ADJECTIVE_PHRASE_GROUP":
        # recursion
        [["ADJECTIVE"],
         ["ADJECTIVE", "ADJECTIVE_PHRASE_GROUP"],
         ["ADJECTIVE", "CC", "ADJECTIVE_PHRASE_GROUP"]],

    # group of adverb phrases
    "ADVERB_PHRASE_GROUP":
        # recursion
        [["ADVERB"],
         ["ADVERB", "ADVERB_PHRASE_GROUP"],
         ["ADVERB", "CC", "ADVERB_PHRASE_GROUP"]],

    # group of prepositional phrases
    "PREPOSITION_PHRASE_GROUP":
        # recursion
        [["PREPOSITION_PHRASE"],
         ["PREPOSITION_PHRASE", "PREPOSITION_PHRASE_GROUP"],
         ["PREPOSITION_PHRASE", "CC", "PREPOSITION_PHRASE_GROUP"]],

    # verb phrase
    "VERB_PHRASE":
        [["VERB"],
         ["VERB", "ADVERB_PHRASE_GROUP"],
         ["VERB", "PREPOSITION_PHRASE_GROUP"],
         ["VERB", "PREPOSITION_PHRASE_GROUP", "ADVERB_PHRASE_GROUP"]],

    # noun phrase
    "NOUN_PHRASE":
        [["NOMINAL_PHRASE"],
         ["DETERMINER_PHRASE", "NOMINAL_PHRASE"]],

    # nominal phrase
    "NOMINAL_PHRASE":
        [["NOUN"],
         ["ADJECTIVE_PHRASE_GROUP", "NOUN"]],

    # prepositional phrase
    "PREPOSITION_PHRASE":
        [["NOUN_PHRASE_GROUP"],
         ["PREPOSITION", "NOUN_PHRASE_GROUP"]],

    # determiner phrase
    "DETERMINER_PHRASE":
        [["DETERMINER"],
         ["PREDETERMINER", "DETERMINER"]],

    # ========================================
    # BINDINGS TO NLTK PARTS OF SPEECH TAGS
    # ========================================

    # nltk determiners
    "DETERMINER":
        [["DT"]],

    # nltk predeterminers
    "PREDETERMINER":
        [["PDT"]],

    # preposition
    "PREPOSITION":
        [["P"], ["TO"], ["IN"]],

    # nltk adverbs
    "ADVERB":
        [["RB"], ["RBR"], ["RBS"]],

    # nltk adjectives
    "ADJECTIVE":
        [["JJ"], ["JJR"], ["JJS"], ["POS"], ["PRPS"], ["WPS"]],

    # nltk nouns
    "NOUN":
        [["'__COLLECTION_NOUN__'"], ["'__ACTOR_FP__'"], ["'__ACTOR_TP__'"],
         ["FW"], ["WDT"], ["WP"], ["NN"], ["PRP"], ["NNS"], ["NNP"], ["NN"], ["NNS"], ["NNP"], ["NNPS"]],

    # nltk verbs
    "VERB":
        [["'__COLLECTION_VERB__'"],
         ["VB", "RP"], ["VB"], ["VBD"], ["VBG"], ["VBN"], ["VBP"], ["VBZ"], ["MD"]]

}

# NLTK part of speech tags
# (to use) CC coordinating conjunction
# (to use) CD cardinal digit
# DT determiner
# (to use) EX existential there (like: “there is” … think of it like “there exists”)
# FW foreign word
# IN preposition/subordinating conjunction
# JJ adjective ‘big’
# JJR adjective, comparative ‘bigger’
# JJS adjective, superlative ‘biggest’
# (to use) LS list marker 1)
# MD modal could, will
# NN noun, singular ‘desk’
# NNS noun plural ‘desks’
# NNP proper noun, singular ‘Harrison’
# NNP$ proper noun, plural ‘Americans’
# PDT predeterminer ‘all the kids’
# POS possessive ending parent’s
# PRP personal pronoun I, he, she
# PRP$ possessive pronoun my, his, hers
# RB adverb very, silently,
# RBR adverb, comparative better
# RBS adverb, superlative best
# RP particle give up
# TO, to go ‘to’ the store.
# (unused) UH interjection, errrrrrrrm
# VB verb, base form take
# VBD verb, past tense took
# VBG verb, gerund/present participle taking
# VBN verb, past participle taken
# VBP verb, sing. present, non-3d take
# VBZ verb, 3rd person sing. present takes
# WDT wh-determiner which
# WP wh-pronoun who, what
# WP$ possessive wh-pronoun whose
# WRB wh-adverb where, when
