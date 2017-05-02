# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from utils import cached_property

def unicode_compatible(cls):
    cls.__str__ = lambda self: self.__unicode__().encode("utf-8")
    return cls

@unicode_compatible
class Sentence(object):
    __slots__ = ("_text", "_cached_property_words", "_tokenizer", "_is_heading",)

    def __init__(self, text, tokenizer, is_heading=False):
        
        self._text = text.strip()
        self._tokenizer = tokenizer
        self._is_heading = bool(is_heading)

    @cached_property
    def words(self):
        return self._tokenizer.to_words(self._text)

    @property
    def is_heading(self):
        return self._is_heading

    def __eq__(self, sentence):
        assert isinstance(sentence, Sentence)
        return self._is_heading is sentence._is_heading and self._text == sentence._text

    def __ne__(self, sentence):
        return not self.__eq__(sentence)

    def __hash__(self):
        return hash((self._is_heading, self._text))

    def __unicode__(self):
        return self._text

    def __repr__(self):
        return ("<%s: %s>").encode("utf-8") % ("Heading" if self._is_heading else "Sentence",self.__str__())
