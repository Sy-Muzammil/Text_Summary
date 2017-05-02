# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import pkgutil
from nltk.corpus import stopwords
from functools import wraps

string_types = (bytes, unicode,)

def cached_property(getter):
    @wraps(getter)
    def decorator(self):
        key = "_cached_property_" + getter.__name__
        if not hasattr(self, key):
            setattr(self, key, getter(self))
        return getattr(self, key)

    return property(decorator)



def get_stop_words(language):
    stopwords_data = stopwords.words('english')
    return stopwords_data


class ItemsCount(object):
    def __init__(self, value):
        self._value = value

    def __call__(self, sequence):
        if isinstance(self._value, string_types):
            if self._value.endswith("%"):
                total_count = len(sequence)
                percentage = int(self._value[:-1])
                # at least one sentence should be chosen
                count = max(1, total_count*percentage // 100)
                return sequence[:count]
            else:
                return sequence[:int(self._value)]
        elif isinstance(self._value, (int, float)):
            return sequence[:int(self._value)]
        else:
            ValueError("Unsuported value of items count '%s'." % self._value)
