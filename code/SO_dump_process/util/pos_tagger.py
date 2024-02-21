import os
import re

# NOTE: for python 2.7, the nltk should be 3.4.0
from nltk import StanfordPOSTagger, word_tokenize

from nltk.stem import WordNetLemmatizer

nltk_stanford_path = r'D:\Installed\NLTK\stanford'
postagger_path = os.path.join(nltk_stanford_path, 'stanford-postagger-full-2018-10-16')

POS_tagger = StanfordPOSTagger(
    os.path.join(postagger_path, 'models/english-bidirectional-distsim.tagger'),
    path_to_jar=os.path.join(postagger_path, 'stanford-postagger-3.9.2.jar')
)

wordnet_lemmatizer = WordNetLemmatizer()
parenthesis_pattern = re.compile(r'\(.*?\)')
squarebucket_pattern = re.compile(r'\[.*?\]')


def generatePOS4Str(sen):
    """
    Generate the POS tagging information for a sentence.
    """
    if sen is None and sen != '':
        return

    tokens, poss = [], []
    pos_list = POS_tagger.tag(word_tokenize(sen))
    for item in pos_list:
        tokens.append(item[0])
        poss.append(item[1])
    return tokens, poss


def get1stNP(sen, flag):
    """
    Get the first NP behind 'a'/'an' in a string.
    """
    if flag:  # remove '(...)' and '[...]'
        items = re.finditer(parenthesis_pattern, sen)
        for item in items:
            s = item.group()
            sen = sen.replace(s, '')
        items = re.finditer(squarebucket_pattern, sen)
        for item in items:
            s = item.group()
            sen = sen.replace(s, '')
    if sen == '':
        return ''

    _1st_np, b = '', False
    tokens, poss = generatePOS4Str(sen.lower())

    for i in range(len(tokens)):
        token = tokens[i]
        if token == 'a' or token == 'an':
            b = True
        if b:
            pos = poss[i]
            if pos.startswith('NN'):
                _1st_np += token + ' '
            elif _1st_np != '':
                break

    return _1st_np.strip()


if __name__ == '__main__':

    _s = 'Java (not to be confused with JavaScript, JScript or JS) is a general-purpose, ' \
         'platform-independent, statically typed, object-oriented programming language designed ' \
         'to be used in conjunction with the Java Virtual Machine (JVM).'
    ts, ps = generatePOS4Str(_s)
    s = ''
    for i in range(len(ts)):
        s += ts[i] + '/' + ps[i] + ' '

    print s
    print ts
    print ps
    print get1stNP(_s, True)

    print wordnet_lemmatizer.lemmatize('axes')
