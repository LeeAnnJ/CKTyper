import os
import re

from nltk import sent_tokenize, word_tokenize, PorterStemmer

from so_parser import so_tags_dir
from util import serializer
from tfidf_trainer import eng_stopwords
from cleaner import cleanText, cleanHtmlTags

porter_stemmer = PorterStemmer()
# p = re.compile(r'([a-z+#]|\d)/([a-z+#]|\d)')
punc_pattern = re.compile(r'[()/:\\\'\",?`\[\]{}!=;|@_]')

# two global dicts for preprocessing
token_stem_dict, token_rstr_dict = {}, {}
tag_c_dict = serializer.load(os.path.join(so_tags_dir, 'tag_c.dump'))

for tag in tag_c_dict:
    for _token in tag.split('-'):
        if ('#' in _token or '+' in _token) and _token not in token_rstr_dict:
            # replace special tokens, e.g., 'c#' and 'c++', before word_tokenize()
            i = len(token_rstr_dict)
            token_rstr_dict[_token] = 'specialtoken' + str(i)


def preprocessStr(s, s_type):
    """
    Preprocess a string (a body or a title or a query).
    1) s_type == '1': 's' is a question's body or a comment's text;
    2) s_type == '2': 's' is a question's title or tags, or a query.
    """
    if s is None:
        return ''

    if s_type != '':
        if s_type == '1':
            s = cleanText(s)
        if s_type == '2':
            s = cleanHtmlTags(s)
        if s is None or s == '':
            return ''

    pstr = ''

    for sen in sent_tokenize(s.lower()):

        words, st2token_dict = [], {}
        for token in token_rstr_dict:
            rstr = token_rstr_dict[token]
            sen = sen.replace(token, rstr)
            st2token_dict[rstr] = token

        s = s.replace('+', ' + ').replace('=', ' = ').replace("'s", '')
        sen = re.sub(punc_pattern, ' ', sen)
        # sen = re.sub(p, r'\1 \2', sen)

        for token in word_tokenize(sen):
            if '..' in token or len(token) > 100 or \
                    (len(token) == 1 and not 'a' <= token <= 'z'):
                continue
            if token in st2token_dict:
                words.append(st2token_dict[token])
            elif token in token_stem_dict:
                words.append(token_stem_dict[token])
            else:
                try:
                    stem = porter_stemmer.stem(token)
                    if stem is not None and stem != '':
                        token_stem_dict[token] = stem
                        words.append(stem)
                except Exception as e:
                    print ('***** Error in StemToken *****', e, ':', token)

        sen = ' '.join(words)
        if s_type == '1':
            # discard short sentences with < 3 words
            if len(words) > 3:
                pstr += sen + '\n'
        else: pstr += sen + '\n'

    return pstr.strip()


# def preprocessStr(s, s_type):
#     """
#     Preprocess a string (a body or a title or a query).
#     1) s_type == '1': 's' is a question's body or a comment's text;
#     2) s_type == '2': 's' is a question's title or tags, or a query.
#     """
#     if s is None or s.strip() == '':
#         return ''
#
#     if s_type != '':
#         if s_type == '1':
#             s = cleanText(s)
#         if s_type == '2':
#             s = cleanHtmlTags(s)
#         if s is None or s == '':
#             return ''
#
#     pstr = ''
#
#     for sen in sent_tokenize(s.lower()):
#
#         words, st2token_dict = [], {}
#         for token in token_rstr_dict:
#             rstr = token_rstr_dict[token]
#             sen = sen.replace(token, rstr)
#             st2token_dict[rstr] = token
#
#         sen = sen.replace('+', ' + ').replace('=', ' = ')
#         sen = separateTwoConjTokensInStr(sen)
#
#         for token in word_tokenize(sen):
#             if token in st2token_dict:
#                 words.append(st2token_dict[token])
#                 continue
#             if token == 'r' or token == 'c':  # two important programming languages
#                 words.append(token)
#                 continue
#             if token.startswith("\'") or token.startswith("\""):
#                 token = token[1:]
#             if token.endswith("\'") or token.endswith("\""):
#                 token = token[:-1]
#
#             if '..' not in token and len(token) < 100 and \
#                     re.match(r'[a-zA-Z0-9.][a-zA-Z0-9.\-/_]*[a-zA-Z0-9]$', token) and \
#                     not re.match(r'[0-9]+(\.[0-9]+)*(\.x|x)?$', token):
#
#                 if token in token_stem_dict:
#                     words.append(token_stem_dict[token])
#                 else:
#                     try:
#                         stem = porter_stemmer.stem(token)
#                         if stem is not None and stem != '':
#                             words.append(stem)
#                             token_stem_dict[token] = stem
#                     except Exception as e:
#                         print '***** Error in StemToken *****', e, ':', token, ' ===== '
#
#         sen = ' '.join(words)
#         if s_type == '1':
#             if len(words) > 3:  # discard short sentences with no more than 3 words
#                 pstr += sen + '\n'
#         else: pstr += sen + '\n'
#
#     return pstr.strip()


# def separateTwoConjTokensInStr(s):
#     """
#     Separate conjective tokens in a string, e.g., 'private/public'.
#     """
#     res = ''
#     for sen in s.split('\n'):
#         for token in sen.split():
#             if len(token.split('/')) == 2 and not re.match(r'[0-9.]+/[0-9.]+$', token):
#                 res += token.replace('/', ' ') + ' '
#             else: res += token + ' '
#         res = res.strip() + '\n'
#     return res.strip()


def removeStopwords(s):
    """
    Remove stopwords in a string.
    """
    if s is None or s == '':
        return ''
    tokens = [token for token in s.split() if token not in eng_stopwords]
    if len(tokens) > 0:
        return ' '.join(tokens)
    return ''


if __name__ == '__main__':

    _s = 'what, which, and xml+convert java between json in a .net .... java_project c++/c# 0-9/2-10'
    print (preprocessStr(_s, '2'))
    print (word_tokenize(_s))
