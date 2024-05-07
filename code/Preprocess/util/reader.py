import codecs
import json
import os

from lxml import etree

from util import serializer
from conf import conf


def readIds(ids_dump_path):
    """
    Read ids from a dumped path.
    """
    ids = set()
    for name in os.listdir(ids_dump_path):
        id_dump_file = os.path.join(ids_dump_path, name)
        for _id in serializer.load(id_dump_file):
            ids.add(_id)
    return ids


def readPreprocessedQuestions(questions_dir):
    """
    Read all preprocessed questions.
    """
    qid_question_dict = {}
    for tag in os.listdir(questions_dir):
        tag_dir = os.path.join(questions_dir, tag)
        _dict = readPreprocessedQuestionsOfTag(os.path.join(tag_dir, 'questions.xml'))
        for qid in _dict:
            qid_question_dict[qid] = _dict[qid]
    return qid_question_dict


def readPreprocessedQuestionsOfTag(tag_questions_xml):
    """
    Read preprocessed questions of a tag from a xml file.
    """
    qid_question_dict = {}
    content = etree.iterparse(tag_questions_xml, events=('end',), tag='row')

    for event, row in content:
        if event == 'end' and row.tag == 'row':
            qid_question_dict[row.get('Id')] = {
                'P-Title': row.get('P-Title'),
                'P-Body': row.get('P-Body'),
                'P-Tags': row.get('P-Tags'),
                'Title': row.get('Title'),
                'Tags': row.get('Tags'),
                'CreationDate': row.get('CreationDate'),
                'OwnerUserId': row.get('OwnerUserId'),
                'Score': row.get('Score'),
                'ViewCount': row.get('ViewCount'),
                'AcceptedAnswerId': row.get('AcceptedAnswerId')
            }
        row.clear()
        while row.getprevious() is not None:
            del row.getparent()[0]
    del content
    return qid_question_dict


def readPreprocessedComments(questions_dir):
    """
    Read all preprocessed comments.
    """
    qid_comments_dict = {}

    for tag in os.listdir(questions_dir):
        tag_commdir = os.path.join(questions_dir, tag + '/comments')
        for name in os.listdir(tag_commdir):
            content = etree.iterparse(os.path.join(
                tag_commdir, name), events=('end',), tag='row')
            for event, row in content:
                if event == 'end' and row.tag == 'row':
                    qid = row.get('PostId')
                    if qid not in qid_comments_dict:
                        qid_comments_dict[qid] = []
                    qid_comments_dict[qid].append({
                        'P-Text': row.get('P-Text'),
                        'P-CQ': row.get('P-CQ'),
                        'CQ': row.get('CQ'),
                        'CreationDate': row.get('CreationDate'),
                        'UserId': row.get('UserId')
                    })
                row.clear()
                while row.getprevious() is not None:
                    del row.getparent()[0]
            del content

    return qid_comments_dict


def readTagSynsDescription():
    """
    Read SO tags' synonyms and descriptions.
    """
    tag_syndesc_dict = {}
    content = etree.iterparse(os.path.join(
        conf.tagcate_dir, 'tag_synonyms_description.xml'), events=('end',), tag='row')

    for event, row in content:
        if event == 'end' and row.tag == 'row':
            tag = row.get('Tag')
            syns = row.get('Synonyms')
            tag_syndesc_dict[tag] = {'Synonyms': set(), 'Description': row.get('Description')}
            if syns != '':
                for syn in syns.split(', '):
                    tag_syndesc_dict[tag]['Synonyms'].add(syn)
        row.clear()
        while row.getprevious() is not None:
            del row.getparent()[0]
    del content
    return tag_syndesc_dict


def readLuceneSimQ(lucene_SimQ_path):
    """
    Get the reduced set of possible similar questions of queries retrieved by lucene,
    which will used for retrieving top k semtically similar questions.
    """
    query_simqids_dict = {}
    for name in os.listdir(lucene_SimQ_path):
        query_id = name.replace('.txt', '')
        query_simqids_dict[query_id] = set()
        for line in codecs.open(os.path.join(lucene_SimQ_path, name), 'r', encoding='utf-8'):
            qid = line.split('\t')[0].strip()
            if qid != '':
                query_simqids_dict[query_id].add(qid)
    return query_simqids_dict


def readJson(json_file):
    """
    Read a dict from a json file.
    """
    with open(json_file, 'r') as f:
        _dict = json.load(f, encoding='utf-8')
    return _dict
