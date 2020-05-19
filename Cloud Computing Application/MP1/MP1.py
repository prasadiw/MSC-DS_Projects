import random
import os
import string
import sys
import re

stopWordsList = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
                 "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
                 "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
                 "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having",
                 "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
                 "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
                 "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
                 "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
                 "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
                 "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

delimiters = " \t,;.?!-:@[](){}_*/"
regx = ' |\t|\,|\;|\.|\?|\!|\-|\:|\@|\[|\]|\(|\)|\{|\}|\_|\*|\/|\s|\|'

def getIndexes(seed):
    random.seed(seed)
    n = 10000
    number_of_lines = 50000
    ret = []
    for i in range(0, n):
        ret.append(random.randint(0, 50000-1))
    return ret

def process(userID):
    indexes = getIndexes(userID)
    ret = []

    allLines = sys.stdin.readlines()
    for i in range(len(allLines)):
        allLines[i] = allLines[i].replace('\n','')

    tw = []

    for idx in indexes:
        str = allLines[idx]
        words = re.split(regx, str)
        for word in words:
            word = word.lower().strip()
            if not word in stopWordsList and word != '':
                tw.append(word)

    unique = list(set(tw))
    wordfreq = [tw.count(p) for p in unique]
    pairs = dict(zip(unique, wordfreq))
    aux = sorted(pairs.items(), key=lambda x: (-x[1], x[0]))

    retp = aux[:20]

    for i in range(len(retp)):
            ret.append(retp[i][0])

    for word in ret:
        print word

process(sys.argv[1])

