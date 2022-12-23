import string

import nltk

nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

spell = SpellChecker()
ss = SnowballStemmer(language='english')
lemmatizer = WordNetLemmatizer()


def lemmatize(data):
    return [lemmatizer.lemmatize(word) for word in data]


def remove_stopwords(data):
    stop_words = set(stopwords.words('english'))
    return [word for word in data if not word.lower() in stop_words]


def spell_checking(data):
    misspelled = spell.unknown(data)
    result = map(lambda word: spell.correction(word) if word in misspelled else word, data)
    return  [word for word in result]


def remove_punctuation(data):
    return [word.translate(str.maketrans('', '', string.punctuation)) for word in data]


def preprocess(x, lemmatization=True, removeStopwords=True, spellChecking=True, removePunctuation=True):
    data = word_tokenize(x)
    if spellChecking:
        data = spell_checking(data)
    if removeStopwords:
        data = remove_stopwords(data)
    if removePunctuation:
        data = remove_punctuation(data)
    if lemmatization:
        data = lemmatize(data)

    return [word for word in data if len(word) > 0]

def stringify(x):
    ' '.join(x)
