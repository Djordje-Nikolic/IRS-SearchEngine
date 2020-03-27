# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 05:41:48 2020

@author: djord

This is only a modified version of the Snowball spanish stemmer, in a way that it works for non accented text. 
"""

# -*- coding: utf-8 -*-
#
# Natural Language Toolkit: Snowball Stemmer
#
# Copyright (C) 2001-2020 NLTK Project
# Author: Peter Michael Stahl <pemistahl@gmail.com>
#         Peter Ljunglof <peter.ljunglof@heatherleaf.se> (revisions)
#         Lakhdar Benzahia <lakhdar.benzahia@gmail.com>  (co-writer)
#         Assem Chelli <assem.ch@gmail.com>  (reviewer arabicstemmer)
#         Abdelkrim Aries <ab_aries@esi.dz> (reviewer arabicstemmer)
# Algorithms: Dr Martin Porter <martin@tartarus.org>
#             Assem Chelli <assem.ch@gmail.com>  arabic stemming algorithm
#             Benzahia Lakhdar <lakhdar.benzahia@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

"""
Snowball stemmers

This module provides a port of the Snowball stemmers
developed by Martin Porter.

There is also a demo function: `snowball.demo()`. REMOVED

"""

from nltk.corpus import stopwords
from nltk.stem.util import suffix_replace, prefix_replace

from nltk.stem.api import StemmerI

class _LanguageSpecificStemmer(StemmerI):

    """
    This helper subclass offers the possibility
    to invoke a specific stemmer directly.
    This is useful if you already know the language to be stemmed at runtime.

    Create an instance of the Snowball stemmer.

    :param ignore_stopwords: If set to True, stopwords are
                             not stemmed and returned unchanged.
                             Set to False by default.
    :type ignore_stopwords: bool
    """

    def __init__(self, ignore_stopwords=False):
        # The language is the name of the class, minus the final "Stemmer".
        language = type(self).__name__.lower()
        if language.endswith("stemmer"):
            language = language[:-7]

        self.stopwords = set()
        if ignore_stopwords:
            try:
                for word in stopwords.words(language):
                    self.stopwords.add(word)
            except IOError:
                raise ValueError(
                    "{!r} has no list of stopwords. Please set"
                    " 'ignore_stopwords' to 'False'.".format(self)
                )

    def __repr__(self):
        """
        Print out the string representation of the respective class.

        """
        return "<{0}>".format(type(self).__name__)

class _StandardStemmer(_LanguageSpecificStemmer):

    """
    This subclass encapsulates two methods for defining the standard versions
    of the string regions R1, R2, and RV.

    """

    def _r1r2_standard(self, word, vowels):
        """
        Return the standard interpretations of the string regions R1 and R2.

        R1 is the region after the first non-vowel following a vowel,
        or is the null region at the end of the word if there is no
        such non-vowel.

        R2 is the region after the first non-vowel following a vowel
        in R1, or is the null region at the end of the word if there
        is no such non-vowel.

        :param word: The word whose regions R1 and R2 are determined.
        :type word: str or unicode
        :param vowels: The vowels of the respective language that are
                       used to determine the regions R1 and R2.
        :type vowels: unicode
        :return: (r1,r2), the regions R1 and R2 for the respective word.
        :rtype: tuple
        :note: This helper method is invoked by the respective stem method of
               the subclasses DutchStemmer, FinnishStemmer,
               FrenchStemmer, GermanStemmer, ItalianStemmer,
               PortugueseStemmer, RomanianStemmer, and SpanishStemmer.
               It is not to be invoked directly!
        :note: A detailed description of how to define R1 and R2
               can be found at http://snowball.tartarus.org/texts/r1r2.html

        """
        r1 = ""
        r2 = ""
        for i in range(1, len(word)):
            if word[i] not in vowels and word[i - 1] in vowels:
                r1 = word[i + 1 :]
                break

        for i in range(1, len(r1)):
            if r1[i] not in vowels and r1[i - 1] in vowels:
                r2 = r1[i + 1 :]
                break

        return (r1, r2)

    def _rv_standard(self, word, vowels):
        """
        Return the standard interpretation of the string region RV.

        If the second letter is a consonant, RV is the region after the
        next following vowel. If the first two letters are vowels, RV is
        the region after the next following consonant. Otherwise, RV is
        the region after the third letter.

        :param word: The word whose region RV is determined.
        :type word: str or unicode
        :param vowels: The vowels of the respective language that are
                       used to determine the region RV.
        :type vowels: unicode
        :return: the region RV for the respective word.
        :rtype: unicode
        :note: This helper method is invoked by the respective stem method of
               the subclasses ItalianStemmer, PortugueseStemmer,
               RomanianStemmer, and SpanishStemmer. It is not to be
               invoked directly!

        """
        rv = ""
        if len(word) >= 2:
            if word[1] not in vowels:
                for i in range(2, len(word)):
                    if word[i] in vowels:
                        rv = word[i + 1 :]
                        break

            elif word[0] in vowels and word[1] in vowels:
                for i in range(2, len(word)):
                    if word[i] not in vowels:
                        rv = word[i + 1 :]
                        break
            else:
                rv = word[3:]

        return rv

class SpanishModStemmer(_StandardStemmer):

    """
    The Spanish Snowball stemmer.

    :cvar __vowels: The Spanish vowels.
    :type __vowels: unicode
    :cvar __step0_suffixes: Suffixes to be deleted in step 0 of the algorithm.
    :type __step0_suffixes: tuple
    :cvar __step1_suffixes: Suffixes to be deleted in step 1 of the algorithm.
    :type __step1_suffixes: tuple
    :cvar __step2a_suffixes: Suffixes to be deleted in step 2a of the algorithm.
    :type __step2a_suffixes: tuple
    :cvar __step2b_suffixes: Suffixes to be deleted in step 2b of the algorithm.
    :type __step2b_suffixes: tuple
    :cvar __step3_suffixes: Suffixes to be deleted in step 3 of the algorithm.
    :type __step3_suffixes: tuple
    :note: A detailed description of the Spanish
           stemming algorithm can be found under
           http://snowball.tartarus.org/algorithms/spanish/stemmer.html

    """

    __vowels = "aeiou\xE1\xE9\xED\xF3\xFA\xFC"
    __step0_suffixes = (
        "selas",
        "selos",
        "sela",
        "selo",
        "las",
        "les",
        "los",
        "nos",
        "me",
        "se",
        "la",
        "le",
        "lo",
    )
    __step1_suffixes = (
        "amientos",
        "imientos",
        "amiento",
        "imiento",
        "aciones",
        "uciones",
        "adoras",
        "adores",
        "ancias",
        "logias",
        "encias",
        "amente",
        "idades",
        "anzas",
        "ismos",
        "ables",
        "ibles",
        "istas",
        "adora",
        "acion",
        "antes",
        "ancia",
        "logia",
        "ucion",
        "encia",
        "mente",
        "anza",
        "icos",
        "icas",
        "ismo",
        "able",
        "ible",
        "ista",
        "osos",
        "osas",
        "ador",
        "ante",
        "idad",
        "ivas",
        "ivos",
        "ico",
        "ica",
        "oso",
        "osa",
        "iva",
        "ivo",
    )
    __step2a_suffixes = (
        "yeron",
        "yendo",
        "yamos",
        "yais",
        "yan",
        "yen",
        "yas",
        "yes",
        "ya",
        "ye",
        "yo",
    )
    __step2b_suffixes = (
        "ariamos",
        "eriamos",
        "iriamos",
        "ieramos",
        "iesemos",
        "ariais",
        "aremos",
        "eriais",
        "eremos",
        "iriais",
        "iremos",
        "ierais",
        "ieseis",
        "asteis",
        "isteis",
        "abamos",
        "aramos",
        "asemos",
        "arian",
        "arias",
        "areis",
        "erian",
        "erias",
        "ereis",
        "irian",
        "irias",
        "ireis",
        "ieran",
        "iesen",
        "ieron",
        "iendo",
        "ieras",
        "ieses",
        "abais",
        "arais",
        "aseis",
        "eamos",
        "aran",
        "aras",
        "aria",
        "eran",
        "eras",
        "eria",
        "iran",
        "iras",
        "iria",
        "iera",
        "iese",
        "aste",
        "iste",
        "aban",
        "aran",
        "asen",
        "aron",
        "ando",
        "abas",
        "adas",
        "idas",
        "aras",
        "ases",
        "iais",
        "ados",
        "idos",
        "amos",
        "imos",
        "emos",
        "ara",
        "are",
        "era",
        "ere",
        "ira",
        "ire",
        "aba",
        "ada",
        "ida",
        "ara",
        "ase",
        "ian",
        "ado",
        "ido",
        "ias",
        "ais",
        "eis",
        "ia",
        "ad",
        "ed",
        "id",
        "an",
        "io",
        "ar",
        "er",
        "ir",
        "as",
        "is",
        "en",
        "es",
    )
    __step3_suffixes = ("os", "a", "e", "o", "a", "e", "i", "o")

    def stem(self, word):
        """
        Stem a Spanish word and return the stemmed form.

        :param word: The word that is stemmed.
        :type word: str or unicode
        :return: The stemmed form.
        :rtype: unicode

        """
        word = word.lower()

        if word in self.stopwords:
            return word

        step1_success = False

        r1, r2 = self._r1r2_standard(word, self.__vowels)
        rv = self._rv_standard(word, self.__vowels)

        # STEP 0: Attached pronoun
        for suffix in self.__step0_suffixes:
            if not (word.endswith(suffix) and rv.endswith(suffix)):
                continue

            if (
                rv[: -len(suffix)].endswith(
                    (
                        "ando",
                        "ar",
                        "er",
                        "iendo",
                        "ir",
                    )
                )
            ) or (
                rv[: -len(suffix)].endswith("yendo")
                and word[: -len(suffix)].endswith("uyendo")
            ):

                word = self.__replace_accented(word[: -len(suffix)])
                r1 = self.__replace_accented(r1[: -len(suffix)])
                r2 = self.__replace_accented(r2[: -len(suffix)])
                rv = self.__replace_accented(rv[: -len(suffix)])
            break

        # STEP 1: Standard suffix removal
        for suffix in self.__step1_suffixes:
            if not word.endswith(suffix):
                continue

            if suffix == "amente" and r1.endswith(suffix):
                step1_success = True
                word = word[:-6]
                r2 = r2[:-6]
                rv = rv[:-6]

                if r2.endswith("iv"):
                    word = word[:-2]
                    r2 = r2[:-2]
                    rv = rv[:-2]

                    if r2.endswith("at"):
                        word = word[:-2]
                        rv = rv[:-2]

                elif r2.endswith(("os", "ic", "ad")):
                    word = word[:-2]
                    rv = rv[:-2]

            elif r2.endswith(suffix):
                step1_success = True
                if suffix in (
                    "adora",
                    "ador",
                    "acion",
                    "adoras",
                    "adores",
                    "aciones",
                    "ante",
                    "antes",
                    "ancia",
                    "ancias",
                ):
                    word = word[: -len(suffix)]
                    r2 = r2[: -len(suffix)]
                    rv = rv[: -len(suffix)]

                    if r2.endswith("ic"):
                        word = word[:-2]
                        rv = rv[:-2]

                elif suffix in ("logia", "logias"):
                    word = suffix_replace(word, suffix, "log")
                    rv = suffix_replace(rv, suffix, "log")

                elif suffix in ("ucion", "uciones"):
                    word = suffix_replace(word, suffix, "u")
                    rv = suffix_replace(rv, suffix, "u")

                elif suffix in ("encia", "encias"):
                    word = suffix_replace(word, suffix, "ente")
                    rv = suffix_replace(rv, suffix, "ente")

                elif suffix == "mente":
                    word = word[: -len(suffix)]
                    r2 = r2[: -len(suffix)]
                    rv = rv[: -len(suffix)]

                    if r2.endswith(("ante", "able", "ible")):
                        word = word[:-4]
                        rv = rv[:-4]

                elif suffix in ("idad", "idades"):
                    word = word[: -len(suffix)]
                    r2 = r2[: -len(suffix)]
                    rv = rv[: -len(suffix)]

                    for pre_suff in ("abil", "ic", "iv"):
                        if r2.endswith(pre_suff):
                            word = word[: -len(pre_suff)]
                            rv = rv[: -len(pre_suff)]

                elif suffix in ("ivo", "iva", "ivos", "ivas"):
                    word = word[: -len(suffix)]
                    r2 = r2[: -len(suffix)]
                    rv = rv[: -len(suffix)]
                    if r2.endswith("at"):
                        word = word[:-2]
                        rv = rv[:-2]
                else:
                    word = word[: -len(suffix)]
                    rv = rv[: -len(suffix)]
            break

        # STEP 2a: Verb suffixes beginning 'y'
        if not step1_success:
            for suffix in self.__step2a_suffixes:
                if rv.endswith(suffix) and word[-len(suffix) - 1 : -len(suffix)] == "u":
                    word = word[: -len(suffix)]
                    rv = rv[: -len(suffix)]
                    break

            # STEP 2b: Other verb suffixes
            for suffix in self.__step2b_suffixes:
                if rv.endswith(suffix):
                    word = word[: -len(suffix)]
                    rv = rv[: -len(suffix)]
                    if suffix in ("en", "es", "eis", "emos"):
                        if word.endswith("gu"):
                            word = word[:-1]

                        if rv.endswith("gu"):
                            rv = rv[:-1]
                    break

        # STEP 3: Residual suffix
        for suffix in self.__step3_suffixes:
            if rv.endswith(suffix):
                word = word[: -len(suffix)]
                if suffix in ("e", "\xE9"):
                    rv = rv[: -len(suffix)]

                    if word[-2:] == "gu" and rv.endswith("u"):
                        word = word[:-1]
                break

        word = self.__replace_accented(word)

        return word


    def __replace_accented(self, word):
        """
        Replaces all accented letters on a word with their non-accented
        counterparts.

        :param word: A spanish word, with or without accents
        :type word: str or unicode
        :return: a word with the accented letters (á, é, í, ó, ú) replaced with
                 their non-accented counterparts (a, e, i, o, u)
        :rtype: str or unicode
        """
        return (
            word.replace("\xE1", "a")
            .replace("\xE9", "e")
            .replace("\xED", "i")
            .replace("\xF3", "o")
            .replace("\xFA", "u")
        )