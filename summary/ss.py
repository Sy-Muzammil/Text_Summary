from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from plaintext import PlaintextParser
from tokenizers import Tokenizer
from Text_Summary import LsaSummarizer as Summarizer
from utils import get_stop_words
import nltk.stem.snowball as nltk_stemmers_module
LANGUAGE = "english"
SENTENCES_COUNT = 10
count = 0
class Stemmer(object):
    
    def __init__(self, language):
    	print("\n\n\t\t*************************************** Text Sumarization Using LSA ***************************************\n\n")
        stemmer_classname = language.capitalize() + 'Stemmer'
        #print(".........stemmer_class......: ",stemmer_classname)
        stemmer_class = getattr(nltk_stemmers_module, stemmer_classname)
        #print("...............calling stemmer __init________\n",stemmer_class)
        self._stemmer = stemmer_class().stem
        #print("sttttt========================================: \n",self._stemmer)

    def __call__(self, word):
        #print("words:======================================================\n\n",word)
        return self._stemmer(word)




if __name__ == "__main__":
    parser = PlaintextParser.from_file("air.txt", Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    # print("======================================================================================")
    # print("called sumy.nlp.stemmers")

    summarizer = Summarizer(stemmer)
    # print("======================================================================================")
    # print("called from sumy.summarizers.lsa import LsaSummarizer as Summarizer")
    summarizer.stop_words = get_stop_words(LANGUAGE)
    # print("======================================================================================")
    # print("called from sumy.utils import get_stop_words")

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(count,": ",sentence)
        count+=1
