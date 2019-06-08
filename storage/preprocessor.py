import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer


class Preprocessor:
    def __init__(self):
        self.stop_words = frozenset(nltk.corpus.stopwords.words('english'))

    # extract tokenized values from text
    def get_tokens(self, text):
        # get lower case, simple word tokens
        simple_tokenized = self.get_simple_tokenized(text)

        # get stop filtered word list
        stop_filtered = self.get_stop_filtered(simple_tokenized)

        # run lemmatization filter across tokens
        lemmad = []
        for word in stop_filtered:
            lemmad.append(self.get_lemma2(self.get_lemma(word)))
        return lemmad

    # lemmatization 1 - extracting plurality reduction
    @staticmethod
    def get_lemma(word):
        lemma = wn.morphy(word)
        if lemma is None:
            return word
        else:
            return lemma

    # lemmatization 2 - extracting root word
    @staticmethod
    def get_lemma2(word):
        return WordNetLemmatizer().lemmatize(word)

    # function to get lower case, word tokenized tokens
    @staticmethod
    def get_simple_tokenized(text):
        lowered = text.lower()
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(lowered)

    # function to filter out stop words
    def get_stop_filtered(self, simple_tokenized):
        stop_filtered = []
        for word in simple_tokenized:
            if word not in self.stop_words:
                stop_filtered.append(word)
        return stop_filtered
