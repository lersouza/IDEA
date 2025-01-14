# -*- coding=GBK -*-
"""
extractSentenceWords

"""
import unicodedata
import sys
import re
import itertools
import logging

from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models.phrases import Phrases


logging.basicConfig(
    format="%(asctime)s: %(levelname)s: %(message)s", level=logging.INFO
)


unicode_punc_tbl = dict.fromkeys(
    i
    for i in range(128, sys.maxunicode)
    if unicodedata.category(chr(i)).startswith("P")
)


wnl = WordNetLemmatizer()


def lemmatize(word, language):
    if language == "en":
        return wnl.lemmatize(word, "v")

    return word


def extractSentenceWords(
    doc,
    remove_url=True,
    remove_punc="utf-8",
    min_length=1,
    lemma=False,
    sent=True,
    replace_digit=False,
    language="en",
):
    if remove_punc:
        # remove unicode punctuation marks, keep ascii punctuation marks
        doc = doc.translate(unicode_punc_tbl)

    if remove_url:
        re_url = r"(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
        doc = re.sub(re_url, "", doc)

    sentences = re.split(
        r"\s*[;:`\"()?!{}]\s*|--+|\s*-\s+|''|\.\s|\.$|\.\.+|��|��", doc
    )  # comment comma
    wc = 0
    wordsInSentences = []
    for sentence in sentences:
        if sentence == "":
            continue

        if not re.search("[A-Za-z0-9]", sentence):
            continue

        # words = re.split( r"\s+\+|^\+|\+?[\-*\/&%=_<>\[\]~\|\@\$]+\+?|\'\s+|\'s\s+|\'s$|\s+\'|^\'|\'$|\$|\\|\s+", sentence )
        words = re.split(r"[\s+,\-*\/&%=_<>\[\]~\|\@\$\\]", sentence)
        words = filter(lambda w: w, words)
        words = map(lambda w: w.lower(), words)

        if replace_digit:
            map(lambda w: re.sub(r"\d+", "<digit>", w), words)

        if lemma:
            words = map(lambda w: lemmatize(w, language), words)

        words = list(words)

        if len(words) >= min_length:
            wordsInSentences.append(words)
            wc += len(words)
    if not sent:
        return list(itertools.chain.from_iterable(wordsInSentences)), wc

    return wordsInSentences, wc
