import os
import re
import time
import shutil
import datetime
import logging
import xml.etree.ElementTree as ET
from util import serializer
from lxml import etree
from pathlib import Path
from sort_answers import divide_and_merge

class XmlTraverser:
    current = None
    root = None

    def __init__(self,target_tag) -> None:
        self.target_tag = target_tag
        pass
    
    def read_file(self, xml_file):
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        self.iter = (elem for elem in self.root.iter() if elem.tag == self.target_tag)
        self.current = next(self.iter)
        return self.current
    
    def get_next_element(self):
        try:
            self.current = next(self.iter)
            return self.current
        except StopIteration:
            self.current = None
            return None


class CodeExtracter(object):
    logger = logging.getLogger(__name__)
    codes_batch = []
    answer_file_list = []
    cur_ans_file = 0
    cur_ans_elment = None
    code_id = 1
    ans_traverser = XmlTraverser('row')

    def __init__(self, post_path, output_dir):
        self.question_dir = Path(f'{post_path}/questions/')
        self.answer_dir = Path(f'{post_path}/answers/')
        self.output_path = output_dir
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)
        pass

    def extract_code_from_body(self,body):
        return re.findall(r'<code>(.*?)</code>', body, re.DOTALL)
    
    def write_objs_to_xml(self,xml_file, objs, objs_name):
        root = etree.Element(objs_name)
        for obj in objs:
            code_elem = etree.SubElement(root, 'code', attrib=obj)
        tree = etree.ElementTree(root)
        tree.write(xml_file, pretty_print=True, xml_declaration=True, encoding='utf-8')

    def sort_key(self,file_path):
        return float(file_path.stem.split('_')[1])
    
    def parse_ans_file(self):
        ans_file = self.answer_file_list[self.cur_ans_file]
        self.logger.info(f"Processing question file: {ans_file}")
        self.cur_ans_elment = self.ans_traverser.read_file(ans_file)
        self.cur_ans_file += 1
    
    def get_next_answer(self):
        elment = self.ans_traverser.get_next_element()
        if elment is None:
            self.parse_ans_file()
        elif self.cur_ans_file<len(self.answer_file_list):
            self.cur_ans_elment = elment
        else: 
            self.cur_ans_elment = None
        
    def add_code_to_batch(self,code_obj):
        self.codes_batch.append(code_obj)
        if self.code_id % 50000 == 0:
            si = self.code_id / 50000
            s = str(si) if si>10 else '0'+str(si)
            output_file = os.path.join(self.output_path, f'dump_{s}.xml')
            self.write_objs_to_xml(output_file, self.codes_batch, 'codes')
            self.codes_batch = []
            self.logger.info(f'{self.code_id} codes dumped')
        self.code_id += 1

    def append_anwer_code_after_question(self, ques_id):
        parent_id = int(self.cur_ans_elment.get('ParentId'))
        while parent_id<ques_id:
            self.logger.debug(f"parent_id: {parent_id} ques_id: {ques_id}")
            post_type_id = self.cur_ans_elment.get('PostTypeId')
            body = self.cur_ans_elment.get('Body')
            row_id = self.cur_ans_elment.get('Id')
            codes = self.extract_code_from_body(body)
            for code in codes:
                if '\n' not in code[0:-1]: continue # filtered out single row code
                code_obj = {
                    'CodeId': str(self.code_id),
                    'RowId': row_id,
                    'ParentId': str(parent_id),
                    'PostTypeId': post_type_id,
                    'Code': code
                }
                self.add_code_to_batch(code_obj)
            self.get_next_answer()
            if self.cur_ans_elment is None: break
            parent_id = int(self.cur_ans_elment.get('ParentId'))
        pass

    def get_filtered_code_from_xml(self):
        '''
        Filter code from question and answer bodies in xml files.
        Only keep the code that contains '\n'.
        '''
        # get xml files
        question_file_list = list(self.question_dir.glob('*.xml'))
        ans_file_list = list(self.answer_dir.glob('*.xml'))
        question_file_list = sorted(question_file_list, key=self.sort_key)
        self.answer_file_list = sorted(ans_file_list, key=self.sort_key)
        self.parse_ans_file()
        # file_list = question_file_list + answer_file_list
        # code_id = 1

        # process question files
        for ques_file in question_file_list:
            self.logger.info(f"Processing question file: {ques_file}")
            context = etree.iterparse(ques_file, events=('end',), tag='row')
            for _, elem in context:
                post_type_id = elem.get('PostTypeId')
                body = elem.get('Body')
                row_id = elem.get('Id')
                parent_id = row_id
                codes = self.extract_code_from_body(body)
                for code in codes:
                    if '\n' not in code[0:-1]: continue # filtered out single row code
                    code_obj = {
                        'CodeId': str(self.code_id),
                        'RowId': row_id,
                        'ParentId': parent_id,
                        'PostTypeId': post_type_id,
                        'Code': code
                    }
                    self.add_code_to_batch(code_obj)
                if self.cur_ans_elment is not None:
                    self.append_anwer_code_after_question(int(parent_id))
                elem.clear()

        if self.codes_batch: # left codes
            s = str(self.code_id / 50000 + 1)
            output_file = os.path.join(self.output_path, f'dump_{s}.xml')
            self.write_objs_to_xml(output_file, self.codes_batch, 'codes') 


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


if __name__ == '__main__':
    now = datetime.datetime.now().strftime('%y%m%d%H%M')
    log_path = f"../logs/{now}.log"
    logging.basicConfig(filename=log_path, level=logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    post_path = "D:/ZhangNeng/codesearch4typeinference/SOdata/tags/java/"
    code_path = "D:/ZhangNeng/codesearch4typeinference/SOdata/SO_multi_row_code_snippets/"

    # sort answers
    ans_folder = f"{post_path}/answers"
    ans_files = os.listdir(ans_folder)
    tmp_folder = f"{post_path}/tmp"
    if not (os.path.exists(tmp_folder)): os.makedirs(tmp_folder)
    start_time = time.process_time()
    res,tmp = divide_and_merge(ans_files, ans_folder, tmp_folder)
    if not res==ans_folder:
        shutil.rmtree(ans_folder)
        for file in os.listdir(res):
            shutil.copyfile(f"{res}/{file}", f"{ans_folder}/{file}")
    shutil.rmtree(tmp_folder)
    end_time = time.process_time()
    logger.info(f'Running time for sort answers: {end_time-start_time}')

    # extract codes
    extracter = CodeExtracter(post_path,code_path)
    start_time = time.process_time()
    extracter.get_filtered_code_from_xml()
    end_time = time.process_time()
    logger.info(f'Running time for extract codes: {end_time-start_time}') # 300.170200691 seconds
    pass