import os
import re
import time
import logging
from util import serializer
from lxml import etree
from pathlib import Path


def extract_code_from_body(body):
    return re.findall(r'<code>(.*?)</code>', body, re.DOTALL)

# def process_xml(file_path_list, output_dir):
#     '''
#     Extract code from question and answer bodies in xml files.
#     '''
#     output_dir_path = Path(output_dir)
#     output_dir_path.mkdir(parents=True, exist_ok=True)
    
#     code_id = 1
#     codes_batch = []
#     for input_file in file_path_list:
#         print(f"==>> Processing: {input_file}")
#         context = etree.iterparse(input_file, events=('end',), tag='row')
#         for _, elem in context:
#             post_type_id = elem.get('PostTypeId')
#             body = elem.get('Body')
#             codes = extract_code_from_body(body)
#             for code in codes:
#                 post_id = elem.get('Id') if post_type_id == '1' else elem.get('ParentId')
#                 code_obj = {
#                     'CodeId': str(code_id),
#                     'PostId': post_id,
#                     'PostTypeId': post_type_id,
#                     'Code': code
#                 }
#                 codes_batch.append(code_obj)
#                 if code_id % 50000 == 0:
#                     s = str(code_id / 50000)
#                     output_file = os.path.join(output_dir, f'dump_{s}.xml')
#                     write_objs_to_xml(output_file, codes_batch, 'codes')
#                     codes_batch = []
#                     print(f'==>> {code_id} codes dumped')
#                 code_id += 1
#             elem.clear()

#     if codes_batch: # left codes
#         s = str(code_id / 50000 + 1) 
#         output_file = os.path.join(output_dir, f'dump_{s}.xml')
#         write_objs_to_xml(output_file, codes_batch, 'codes')


def get_filtered_code_from_xml(file_path_list, output_dir):
    '''
    Filter code from question and answer bodies in xml files.
    Only keep the code that contains '\n'.
    '''
    logger = logging.getLogger(__name__)
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)
    
    code_id = 1
    codes_batch = []
    for input_file in file_path_list:
        print(f"==>> Processing: {input_file}")
        context = etree.iterparse(input_file, events=('end',), tag='row')
        for _, elem in context:
            post_type_id = elem.get('PostTypeId')
            body = elem.get('Body')
            post_id = elem.get('Id') if post_type_id == '1' else elem.get('ParentId')
            codes = extract_code_from_body(body)
            jointed_code = ""
            for code in codes:
                if '\n' in code[0:-1]: # filtered out single row code
                    logger.debug(f"code: {code}")
                    jointed_code += code
            if len(jointed_code) > 0:
                if post_type_id == '1': body = elem.get('Title') + '\n' + body
                code_obj = {
                    'CodeId': str(code_id),
                    'PostId': post_id,
                    'PostTypeId': post_type_id,
                    'Code': code,
                    'Body': body
                }
                codes_batch.append(code_obj)
                if code_id % 50000 == 0:
                    si = code_id / 50000
                    s = '0'+str(si) if si<10 else str(si)
                    output_file = os.path.join(output_dir, f'dump_{s}.xml')
                    write_objs_to_xml(output_file, codes_batch, 'codes')
                    codes_batch = []
                    print(f'==>> {code_id} codes dumped')
                code_id += 1
            elem.clear()

    if codes_batch: # left codes
        s = str(code_id / 50000 + 1)
        output_file = os.path.join(output_dir, f'dump_{s}.xml')
        write_objs_to_xml(output_file, codes_batch, 'codes') 


# def get_filtered_code_from_xml(file_path_list, output_dir):
#     '''
#     Filter code from question and answer bodies in xml files.
#     Only keep the code that contains '\n'.
#     '''
#     output_dir_path = Path(output_dir)
#     output_dir_path.mkdir(parents=True, exist_ok=True)
    
#     code_id = 1
#     codes_batch = []
#     for input_file in file_path_list:
#         print(f"==>> Processing: {input_file}")
#         context = etree.iterparse(input_file, events=('end',), tag='row')
        # for _, elem in context:
        #     post_type_id = elem.get('PostTypeId')
        #     body = elem.get('Body')
        #     codes = extract_code_from_body(body)
        #     for code in codes:
        #         if '\n' not in code: # filtered out single row code
        #             continue
        #         post_id = elem.get('Id') if post_type_id == '1' else elem.get('ParentId')
        #         code_obj = {
        #             'CodeId': str(code_id),
        #             'PostId': post_id,
        #             'PostTypeId': post_type_id,
        #             'Code': code
        #         }
        #         codes_batch.append(code_obj)
        #         if code_id % 50000 == 0:
        #             s = str(code_id / 50000)
        #             output_file = os.path.join(output_dir, f'dump_{s}.xml')
        #             write_objs_to_xml(output_file, codes_batch, 'codes')
        #             codes_batch = []
        #             print(f'==>> {code_id} codes dumped')
        #         code_id += 1
        #     elem.clear()

#     if codes_batch: # left codes
#         s = str(code_id / 50000 + 1) 
#         output_file = os.path.join(output_dir, f'dump_{s}.xml')
#         write_objs_to_xml(output_file, codes_batch, 'codes') 
    

def write_objs_to_xml(xml_file, objs, objs_name):
    root = etree.Element(objs_name)
    for obj in objs:
        code_elem = etree.SubElement(root, 'code', attrib=obj)
    tree = etree.ElementTree(root)
    tree.write(xml_file, pretty_print=True, xml_declaration=True, encoding='utf-8')


def sort_key(file_path):
    return float(file_path.stem.split('_')[1])


if __name__ == '__main__':
    # get xml files
    script_path = Path(__file__).parent
    question_dir = script_path / Path(f'../SOData/tags/java/questions/')
    answer_dir = script_path / Path(f'../SOData/tags/java/answers/')
    print(f'question_dir = {question_dir}')
    question_file_list = list(question_dir.glob('*.xml'))
    answer_file_list = list(answer_dir.glob('*.xml'))
    question_file_list = sorted(question_file_list, key=sort_key)
    answer_file_list = sorted(answer_file_list, key=sort_key)
    file_list = question_file_list + answer_file_list

    
    start_time = time.process_time()
    get_filtered_code_from_xml(file_list,'../SOData/SO_multi_row_code_snippets/')
    end_time = time.process_time()
    print ('Running time:', end_time - start_time) # 300.170200691 seconds