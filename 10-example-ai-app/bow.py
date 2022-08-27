import nltk
import numpy as np
from HanTa import HanoverTagger as ht

# run only once (to init a new system)
nltk.download('punkt')

tagger = ht.HanoverTagger('morphmodel_ger.pgz')


def token_and_stem(text):
    text = str(text)
    bag_of_words = []
    delimiters = ('.')
    split_char = '+'

    tokenized_sentence = nltk.tokenize.word_tokenize(text, language='german')

    for word in tokenized_sentence:
        stemmed_words = tagger.analyze(word, taglevel=2)
        stemmed_words = stemmed_words[0]

        for char in delimiters:
            stemmed_words = stemmed_words.replace(char, split_char)

        seperated_stemmed_words = stemmed_words.split(split_char)
        for single_stemmed_word in seperated_stemmed_words:
            if len(single_stemmed_word) > 1 and single_stemmed_word not in bag_of_words:
                bag_of_words.append(single_stemmed_word)

    return bag_of_words


def token_and_stem_array(text):
    #text = str(text)
    new_text = ""
    for word in text:
        new_text = new_text + str(word) + " "
    text = new_text
    bag_of_words = []
    delimiters = ('.')
    split_char = '+'

    tokenized_sentence = nltk.tokenize.word_tokenize(text, language='german')

    for word in tokenized_sentence:
        stemmed_words = tagger.analyze(word, taglevel=2)
        stemmed_words = stemmed_words[0]

        for char in delimiters:
            stemmed_words = stemmed_words.replace(char, split_char)

        seperated_stemmed_words = stemmed_words.split(split_char)

        for single_stemmed_word in seperated_stemmed_words:
            if len(single_stemmed_word) > 1 and single_stemmed_word not in bag_of_words:
                bag_of_words.append(single_stemmed_word)
    return bag_of_words


def bag_of_words(tokenized_sentence, all_words):

    tokenized_sentence = token_and_stem(tokenized_sentence)
    bag = np.zeros(len(all_words), dtype=np.float32)

    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1

    return bag


def bag_of_words_array(tokenized_sentence, all_words):
    tokenized_sentence = token_and_stem_array(tokenized_sentence)
    bag = np.zeros(len(all_words), dtype=np.float32)

    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1

    return bag
