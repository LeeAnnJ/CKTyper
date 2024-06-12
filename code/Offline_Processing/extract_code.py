import os
import shutil

from Offline_Processing.sort_answers import divide_and_merge
from Offline_Processing.obj import CodeExtracter

# if __name__ == '__main__':
def extract_code_from_post(fs_config):
    post_path = fs_config['POST_DUMP_DIC']
    code_path = fs_config['SO_CODE_FOLDER']
    # sort answers
    ans_folder = f"{post_path}/answers"
    ans_files = os.listdir(ans_folder)
    tmp_folder = f"{post_path}/tmp"
    if not (os.path.exists(tmp_folder)): os.makedirs(tmp_folder)
    res, tmp = divide_and_merge(ans_files, ans_folder, tmp_folder)
    if not res==ans_folder:
        shutil.rmtree(ans_folder)
        for file in os.listdir(res):
            shutil.copyfile(f"{res}/{file}", f"{ans_folder}/{file}")
    shutil.rmtree(tmp_folder)

    # extract codes
    extracter = CodeExtracter(post_path,code_path)
    extracter.get_filtered_code_from_xml()
    pass