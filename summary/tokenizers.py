# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import re
import nltk

class DefaultWordTokenizer(object):
    def tokenize(self, text):
        #print(".........called DefaultWordTokenizer ")
        return nltk.word_tokenize(text)


class Tokenizer(object):

    _WORD_PATTERN = re.compile(r"^[^\W\d_]+$", re.UNICODE)
    # improve tokenizer by adding specific abbreviations it has issues with
    # note the final point in these items must not be included
    LANGUAGE_EXTRA_ABREVS = {
        "english": ["e.g", "i.e", "wrt", "EFB", "VoIP", "ADS", "IP" , "A.I."],
    }


    def __init__(self, language):
        self._language = language
        #print("............in tokenizers...............")
        tokenizer_language = self.language
        self._sentence_tokenizer = self._get_sentence_tokenizer(tokenizer_language)
        self._word_tokenizer = self._get_word_tokenizer(tokenizer_language)

    @property
    def language(self):
        return self._language

    def _get_sentence_tokenizer(self, language):
        path = ("tokenizers/punkt/%s.pickle").encode("utf-8") % (language).encode("utf-8")
        #print(".........called DefaultWordTokenizer 2 ")
        return nltk.data.load(path)

    def _get_word_tokenizer(self, language):
       return DefaultWordTokenizer()

    def to_sentences(self, paragraph):
        if hasattr(self._sentence_tokenizer, '_params'):
            extra_abbreviations = self.LANGUAGE_EXTRA_ABREVS.get(self._language, [])
            #print("abv================================\n",extra_abbreviations)
            self._sentence_tokenizer._params.abbrev_types.update(extra_abbreviations)
        sentences = self._sentence_tokenizer.tokenize(paragraph)
        return tuple(map(unicode.strip, sentences))

    def to_words(self, sentence):
        words = self._word_tokenizer.tokenize(sentence)
        return tuple(filter(self._is_word, words))

    def _is_word(self, word):
        return bool(Tokenizer._WORD_PATTERN.search(word))
