import codecs
import os
import time

from lxml import etree

from util import serializer
from conf import conf
from obj.comment import Comment
from obj.post import Post
from util.reader import readIds
from util.writer import writeObjs2xml

patch_size = 50000

so_tags_dir = os.path.join(conf.so_dir, 'tags')

if not os.path.exists(so_tags_dir):
    os.makedirs(so_tags_dir)


def getQuestions(tags):
    """
    Get SO Questions (and their ids) that are tagged with a set of tags.
    """
    tag_qc_dict = {}
    tag_qids_dict = {}
    tag_qiddir_dict = {}
    tag_qs_dict = {}
    tag_qdir_dict = {}
    tag_tagstr_dict = {}

    for tag in tags:

        tag_qc_dict[tag] = 0
        tag_qids_dict[tag] = []
        tag_qs_dict[tag] = []
        tag_tagstr_dict[tag] = '<' + tag + '>'
        tag_dir = os.path.join(so_tags_dir, tag)

        tag_qiddir = os.path.join(tag_dir, 'question_ids')
        if not os.path.exists(tag_qiddir):
            os.makedirs(tag_qiddir)
        tag_qiddir_dict[tag] = tag_qiddir

        tag_qdir = os.path.join(tag_dir, 'questions')
        if not os.path.exists(tag_qdir):
            os.makedirs(tag_qdir)
        tag_qdir_dict[tag] = tag_qdir

    context = etree.iterparse(conf.posts_xml, events=('end',), tag='row')

    for event, row in context:
        if event == 'end' and row.tag == 'row':
            if row.get('PostTypeId') == '1':
                for tag, tag_str in tag_tagstr_dict.items():
                    if tag_str in row.get('Tags'):
                        tag_qc_dict[tag] += 1
                        tag_qids_dict[tag].append(row.get('Id'))
                        tag_qs_dict[tag].append(Post(row))
                        c = tag_qc_dict[tag]

                        if c % patch_size == 0:
                            s = str(c / patch_size)
                            id_dump = os.path.join(tag_qiddir_dict[tag], 'dump_' + s)
                            serializer.dumpObj(id_dump, tag_qids_dict[tag])
                            q_xml = os.path.join(tag_qdir_dict[tag], 'dump_' + s + '.xml')
                            writeObjs2xml(q_xml, tag_qs_dict[tag], 'Questions')
                            tag_qids_dict[tag] = []
                            tag_qs_dict[tag] = []
                            print (tag, ':', c)

        row.clear()
        while row.getprevious() is not None:
            del row.getparent()[0]
    del context

    for tag in tags:
        if len(tag_qids_dict[tag]) > 0:
            s = str(tag_qc_dict[tag] / patch_size + 1)
            id_dump = os.path.join(tag_qiddir_dict[tag], 'dump_' + s)
            serializer.dumpObj(id_dump, tag_qids_dict[tag])
            q_xml = os.path.join(tag_qdir_dict[tag], 'dump_' + s + '.xml')
            writeObjs2xml(q_xml, tag_qs_dict[tag], 'Questions')
        print (tag, ':', tag_qc_dict[tag])


def getAnswers(tags):
    """
    Get SO Answers associated with the Questions that are
    tagged with a set of tags based on their ids.
    """
    tag_qids_dict = {}
    tag_ac_dict = {}
    tag_aids_dict = {}
    tag_aiddir_dict = {}
    tag_as_dict = {}
    tag_adir_dict = {}

    for tag in tags:

        tag_ac_dict[tag] = 0
        tag_aids_dict[tag] = []
        tag_as_dict[tag] = []
        tag_dir = os.path.join(so_tags_dir, tag)
        tag_qids_dict[tag] = readIds(os.path.join(tag_dir, 'question_ids'))

        tag_aiddir = os.path.join(tag_dir, 'answer_ids')
        if not os.path.exists(tag_aiddir):
            os.makedirs(tag_aiddir)
        tag_aiddir_dict[tag] = tag_aiddir

        tag_adir = os.path.join(tag_dir, 'answers')
        if not os.path.exists(tag_adir):
            os.makedirs(tag_adir)
        tag_adir_dict[tag] = tag_adir

    context = etree.iterparse(conf.posts_xml, events=('end',), tag='row')

    for event, row in context:
        if event == 'end' and row.tag == 'row':
            if row.get('PostTypeId') == '2':
                for tag, qids in tag_qids_dict.items():
                    if row.get('ParentId') in qids:
                        tag_ac_dict[tag] += 1
                        tag_aids_dict[tag].append(row.get('Id'))
                        tag_as_dict[tag].append(Post(row))
                        c = tag_ac_dict[tag]

                        if c % patch_size == 0:
                            s = str(c / patch_size)
                            id_dump = os.path.join(tag_aiddir_dict[tag], 'dump_' + s)
                            serializer.dumpObj(id_dump, tag_aids_dict[tag])
                            a_xml = os.path.join(tag_adir_dict[tag], 'dump_' + s + '.xml')
                            writeObjs2xml(a_xml, tag_as_dict[tag], 'Answers')
                            tag_aids_dict[tag] = []
                            tag_as_dict[tag] = []
                            print (tag, ':', c)

        row.clear()
        while row.getprevious() is not None:
            del row.getparent()[0]
    del context

    for tag in tags:
        if len(tag_aids_dict[tag]) > 0:
            s = str(tag_ac_dict[tag] / patch_size + 1)
            id_dump = os.path.join(tag_aiddir_dict[tag], 'dump_' + s)
            serializer.dumpObj(id_dump, tag_aids_dict[tag])
            a_xml = os.path.join(tag_adir_dict[tag], 'dump_' + s + '.xml')
            writeObjs2xml(a_xml, tag_as_dict[tag], 'Answers')
        print (tag, ':', tag_ac_dict[tag])


def getComments(tags):
    """
    Get SO Comments associated with the Questions & Answers that
    are tagged with a set of tags based on their ids.
    """
    tag_qaids_dict = {}
    tag_commc_dict = {}
    tag_comms_dict = {}
    tag_commdir_dict = {}

    for tag in tags:

        tag_commc_dict[tag] = 0
        tag_comms_dict[tag] = []
        tag_dir = os.path.join(so_tags_dir, tag)
        tag_qaids_dict[tag] = readIds(os.path.join(tag_dir, 'question_ids'))
        tag_qaids_dict[tag] |= readIds(os.path.join(tag_dir, 'answer_ids'))

        tag_commdir = os.path.join(tag_dir, 'comments')
        if not os.path.exists(tag_commdir):
            os.makedirs(tag_commdir)
        tag_commdir_dict[tag] = tag_commdir

    context = etree.iterparse(conf.comments_xml, events=('end',), tag='row')

    for event, row in context:
        if event == 'end' and row.tag == 'row':
            post_id = row.get('PostId')
            for tag, qaids in tag_qaids_dict.items():
                if post_id in qaids:
                    tag_commc_dict[tag] += 1
                    tag_comms_dict[tag].append(Comment(row))
                    c = tag_commc_dict[tag]

                    if c % patch_size == 0:
                        s = str(c / patch_size)
                        comm_xml = os.path.join(tag_commdir_dict[tag], 'dump_' + s + '.xml')
                        writeObjs2xml(comm_xml, tag_comms_dict[tag], 'Comments')
                        tag_comms_dict[tag] = []
                        print (tag, ':', c)

        row.clear()
        while row.getprevious() is not None:
            del row.getparent()[0]
    del context

    for tag in tags:
        if len(tag_comms_dict[tag]) > 0:
            s = str(tag_commc_dict[tag] / patch_size + 1)
            comm_xml = os.path.join(tag_commdir_dict[tag], 'dump_' + s + '.xml')
            writeObjs2xml(comm_xml, tag_comms_dict[tag], 'Comments')
        print (tag, ':', tag_commc_dict[tag])


def getTagC(tag_c_dump, tag_c_txt):
    """
    Get & dump the SO tags' frequencies.
    """
    tag_c_dict = {}
    content = etree.iterparse(conf.tags_xml, events=('end',), tag='row')
    for event, row in content:
        if event == 'end' and row.tag == 'row':
            tag_c_dict[row.get('TagName')] = int(row.get('Count'))
        row.clear()
    del content

    serializer.dumpObj(tag_c_dump, tag_c_dict)
    sorted_list = sorted(tag_c_dict.items(), key=lambda x:x[1], reverse=True)

    f = codecs.open(tag_c_txt, 'w', encoding='utf-8')
    for item in sorted_list:
        f.write(item[0] + '\t' + str(item[1]) + '\n')
    f.close()


if __name__ == '__main__':

    # print ('get questions and their ids ======')
    # start_time = time.perf_counter()
    # getQuestions(conf.interested_tags)
    # end_time = time.perf_counter()
    # print ('Running time:', end_time - start_time)

    # print ('\n\nget answers and their ids ======')
    # start_time = time.perf_counter()
    # getAnswers(conf.interested_tags)
    # end_time = time.perf_counter()
    # print ('Running time:', end_time - start_time)

    # print ('\n\nget comments ======')
    # start_time = time.perf_counter()
    # getComments(conf.interested_tags)
    # end_time = time.perf_counter()
    # print ('Running time:', end_time - start_time)

    # print ("\n\nget tags' count ======")
    # getTagC(os.path.join(so_tags_dir, 'tag_c.dump'), os.path.join(so_tags_dir, 'tag_c.txt'))
    pass