# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from warnings import warn
from collections import namedtuple
from operator import attrgetter
from utils import ItemsCount
import inspect
import math
import numpy
from numpy.linalg import svd as singular_value_decomposition

SentenceInfo = namedtuple("SentenceInfo", ("sentence", "order", "rating",))
class AbstractSummarizer(object):
    def __init__(self, stemmer):
		self._stemmer = stemmer

    def stem_word(self, word):
        return self._stemmer(self.normalize_word(word))

    def normalize_word(self, word):
        return word.decode("utf-8").lower()

    def get_best_sentences(self, sentences, count, rating, *args, **kwargs):
        rate = rating
        if isinstance(rating, dict):
            assert not args and not kwargs
            rate = lambda s: rating[s]
        # for o, s in enumerate(sentences):
        # 	print("============================================================================\n",s,rate(o))
       
        infos = (SentenceInfo(s, o, rate(s, *args, **kwargs))for o, s in enumerate(sentences))
        # for o, s in enumerate(sentences):
        #     print("sent:=========================================\n",o)

        infos = sorted(infos, key=attrgetter("rating"), reverse=True)
        if not isinstance(count, ItemsCount):
            count = ItemsCount(count)   #sort by rating
        infos = count(infos)
        infos = sorted(infos, key=attrgetter("order")) #sort by order

        return tuple(i.sentence for i in infos)



class LsaSummarizer(AbstractSummarizer):
    MIN_DIMENSIONS = 10
    REDUCTION_RATIO = 3/1
    _stop_words = frozenset()

    @property
    def stop_words(self):
        return self._stop_words

    @stop_words.setter
    def stop_words(self, words):
        self._stop_words = frozenset(map(self.normalize_word, words))

    def __call__(self, document, sentences_count):
        dictionary = self.create_dictionary(document)
        matrix = self.create_matrix(document, dictionary)
        matrix = self.compute_term_frequency(matrix)
        #print("mat==============================================:\n",matrix)
        u, sigma, v = singular_value_decomposition(matrix, full_matrices=False)
        ranks = iter(self.compute_ranks(sigma, v))
        #print("ranks**************************************\n",next(ranks))
        return self.get_best_sentences(document.sentences, sentences_count,lambda s: next(ranks))
        
    def create_dictionary(self, document):
        """Creates mapping key = word, value = row index"""
        #count = []
        #percentage  = []
        
        words = map(self.normalize_word, document.words)
        unique_words = frozenset(self.stem_word(w) for w in words if w not in self._stop_words)
        # 
        #total_count = len(sequence)
        #percentage = int(self._value[:-1])
        # at least one sentence should be chosen
        # count = max(1, total_count*percentage // 100)
        # 
        return dict((w, i) for i, w in enumerate(unique_words))

    def create_matrix(self, document, dictionary):
        
        sentences = document.sentences
        words_count = len(dictionary)
        sentences_count = len(sentences)
        # if words_count < sentences_count:
        #     if word in dictionary:
        #             row = dictionary[word]
        #             matrix[row, col] += 1

        matrix = numpy.zeros((words_count, sentences_count))
       
        for col, sentence in enumerate(sentences):
            for word in map(self.stem_word, sentence.words):
                if word in dictionary:
                    row = dictionary[word]
                    matrix[row, col] += 1

        return matrix

    def compute_term_frequency(self, matrix, smooth=0.4):
        assert 0.0 <= smooth < 1.0
        count = 0
        param = {}
        tf_idf = []
        max_word_frequencies = numpy.max(matrix, axis=0)
        rows, cols = matrix.shape
        for row in range(rows):
            for col in range(cols):
                max_word_frequency = max_word_frequencies[col]
                if max_word_frequency != 0:
                    frequency = matrix[row, col]/max_word_frequency
                    matrix[row, col] = smooth + (1.0 - smooth)*frequency

        return matrix

    def compute_ranks(self, sigma, v_matrix):
        assert len(sigma) == v_matrix.shape[0], "Matrices should be multiplicable"
        #print("===================\n",int(len(sigma)))
        dimensions = max(LsaSummarizer.MIN_DIMENSIONS,int(len(sigma)*LsaSummarizer.REDUCTION_RATIO))
        powered_sigma = tuple(s**2 if i < dimensions else 0.0 for i, s in enumerate(sigma))
        ranks = []
        # iterate over columns of matrix (rows of transposed matrix)
        for column_vector in v_matrix.T:
        	rank = sum(s*v**2 for s, v in zip(powered_sigma, column_vector))
        	ranks.append(math.sqrt(rank))
        return ranks
