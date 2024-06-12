import os
import logging
from lxml import etree

from Offline_Processing.obj import Post
from utils import writeObjs2xml, write_pickle, read_pickle

question_patch_size = 50000
answer_patch_size = 50000


def readIds(ids_dump_path):
    """
    Read ids from a dumped path.
    """
    ids = set()
    for name in os.listdir(ids_dump_path):
        id_dump_file = os.path.join(ids_dump_path, name)
        part_ids = read_pickle(id_dump_file)
        ids.update(part_ids)
        # for _id in serializer.load(id_dump_file):
        #     ids.add(_id)
    return ids


def getQuestions(conf):
    """
    Get SO Questions (and their ids) that are tagged with a set of tags.
    """
    logger = logging.getLogger(__name__)
    so_tags_dir = conf.so_tags_dir
    if not os.path.exists(so_tags_dir): os.makedirs(so_tags_dir)
    tags = conf.interested_tags
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

                        if c % question_patch_size == 0:
                            si = c / question_patch_size
                            s = '0'+str(si) if si<10 else str(si)
                            id_dump = os.path.join(tag_qiddir_dict[tag], 'dump_' + s)
                            write_pickle(id_dump, tag_qids_dict[tag])

                            q_xml = os.path.join(tag_qdir_dict[tag], 'dump_' + s + '.xml')
                            writeObjs2xml(q_xml, tag_qs_dict[tag], 'Questions')
                            tag_qids_dict[tag] = []
                            tag_qs_dict[tag] = []
                            logger.info(f'{tag} : {c}')

        row.clear()
        while row.getprevious() is not None:
            del row.getparent()[0]
    del context

    for tag in tags:
        if len(tag_qids_dict[tag]) > 0:
            s = str(tag_qc_dict[tag] / question_patch_size + 1)
            id_dump = os.path.join(tag_qiddir_dict[tag], 'dump_' + s)
            write_pickle(id_dump, tag_qids_dict[tag])
            q_xml = os.path.join(tag_qdir_dict[tag], 'dump_' + s + '.xml')
            writeObjs2xml(q_xml, tag_qs_dict[tag], 'Questions')
        logger.info(f'{tag} : {tag_qc_dict[tag]}')


def getAnswers(conf):  #tags):
    """
    Get SO Answers associated with the Questions that are
    tagged with a set of tags based on their ids.
    """
    logger = logging.getLogger(__name__)
    so_tags_dir = conf.so_tags_dir
    tags = conf.interested_tags
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

                        if c % answer_patch_size == 0:
                            si = c / answer_patch_size
                            s = '0'+str(si) if si<10 else str(si)
                            id_dump = os.path.join(tag_aiddir_dict[tag], 'dump_' + s)
                            write_pickle(id_dump, tag_aids_dict[tag])
                            a_xml = os.path.join(tag_adir_dict[tag], 'dump_' + s + '.xml')
                            writeObjs2xml(a_xml, tag_as_dict[tag], 'Answers')
                            tag_aids_dict[tag] = []
                            tag_as_dict[tag] = []
                            logger.info(f'{tag} : {c}')

        row.clear()
        while row.getprevious() is not None:
            del row.getparent()[0]
    del context

    for tag in tags:
        if len(tag_aids_dict[tag]) > 0:
            s = str(tag_ac_dict[tag] / answer_patch_size + 1)
            id_dump = os.path.join(tag_aiddir_dict[tag], 'dump_' + s)
            write_pickle(id_dump, tag_aids_dict[tag])
            a_xml = os.path.join(tag_adir_dict[tag], 'dump_' + s + '.xml')
            writeObjs2xml(a_xml, tag_as_dict[tag], 'Answers')
        logger.info(f'{tag} : {tag_ac_dict[tag]}')


# def getComments(tags):
#     """
#     Get SO Comments associated with the Questions & Answers that
#     are tagged with a set of tags based on their ids.
#     """
#     logger = logging.getLogger(__name__)
#     tag_qaids_dict = {}
#     tag_commc_dict = {}
#     tag_comms_dict = {}
#     tag_commdir_dict = {}

#     for tag in tags:

#         tag_commc_dict[tag] = 0
#         tag_comms_dict[tag] = []
#         tag_dir = os.path.join(so_tags_dir, tag)
#         tag_qaids_dict[tag] = readIds(os.path.join(tag_dir, 'question_ids'))
#         tag_qaids_dict[tag] |= readIds(os.path.join(tag_dir, 'answer_ids'))

#         tag_commdir = os.path.join(tag_dir, 'comments')
#         if not os.path.exists(tag_commdir):
#             os.makedirs(tag_commdir)
#         tag_commdir_dict[tag] = tag_commdir

#     context = etree.iterparse(conf.comments_xml, events=('end',), tag='row')

#     for event, row in context:
#         if event == 'end' and row.tag == 'row':
#             post_id = row.get('PostId')
#             for tag, qaids in tag_qaids_dict.items():
#                 if post_id in qaids:
#                     tag_commc_dict[tag] += 1
#                     tag_comms_dict[tag].append(Comment(row))
#                     c = tag_commc_dict[tag]

#                     if c % patch_size == 0:
#                         s = str(c / patch_size)
#                         comm_xml = os.path.join(tag_commdir_dict[tag], 'dump_' + s + '.xml')
#                         writeObjs2xml(comm_xml, tag_comms_dict[tag], 'Comments')
#                         tag_comms_dict[tag] = []
#                         logger.info(f'{tag} : {c}')

#         row.clear()
#         while row.getprevious() is not None:
#             del row.getparent()[0]
#     del context

#     for tag in tags:
#         if len(tag_comms_dict[tag]) > 0:
#             s = str(tag_commc_dict[tag] / patch_size + 1)
#             comm_xml = os.path.join(tag_commdir_dict[tag], 'dump_' + s + '.xml')
#             writeObjs2xml(comm_xml, tag_comms_dict[tag], 'Comments')
#         logger.info(f'{tag} : {tag_commc_dict[tag]}')
