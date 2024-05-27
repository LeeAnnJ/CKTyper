import heapq
import logging
from lxml import etree
import xml.etree.ElementTree as ET

from obj.post import Post
from util.writer import writeObjs2xml
    

def parse_xml(file):
    return ET.parse(file).getroot().findall('row')


def sort_singal_file(file_name, source_folder, res_folder):
    ans_elems = []
    ans_file = f'{source_folder}/{file_name}'
    context = etree.iterparse(ans_file, events=('end',), tag='row')
    for _, elem in context:
        ans_elems.append(Post(elem))
    ans_elems.sort()
    sorted_file = f'{res_folder}/{file_name}'
    writeObjs2xml(sorted_file, ans_elems, 'Answers')
    return


def merge_files(groups, res_folder, tmp_folder):
    logger = logging.getLogger(__name__)
    logger.info(f"merge files: {groups} from {tmp_folder} to {res_folder}")
    heap = []
    file_iters = [iter(parse_xml(f"{tmp_folder}/{group[0]}")) for group in groups]

    for i, file_iter in enumerate(file_iters):
        try:
            elem = next(file_iter)
            record = Post(elem)
            heapq.heappush(heap, (record, i))
        except StopIteration:
            continue

    merged_records = []
    res_file_list = []
    iter_count = [1,1,1,1]
    file_count = 0
    for group in groups: res_file_list.extend(group)
    
    while heap:
        record, i = heapq.heappop(heap)
        merged_records.append(record)
        if len(merged_records) >= 50000:
            out_file = f"{res_folder}/{res_file_list[file_count]}"
            writeObjs2xml(out_file, merged_records, 'Answers')
            merged_records = []
            file_count += 1
        try:
            next_record = Post(next(file_iters[i]))
            heapq.heappush(heap, (next_record,i))
        except StopIteration:
            if iter_count[i] < len(groups[i]):
                file_iters[i] = iter(parse_xml(f"{tmp_folder}/{groups[i][iter_count[i]]}"))
                iter_count[i] += 1
                try:
                    next_record = Post(next(file_iters[i]))
                    heapq.heappush(heap, (next_record,i))
                except StopIteration:
                    continue
    
    if merged_records:
        out_file = f"{res_folder}/{res_file_list[file_count]}"
        # out_file = os.path.join(res_folder, f"{file_prefix}_{file_count}.xml")
        writeObjs2xml(out_file, merged_records, 'Answers')
    return


def divide_and_merge(file_list, source_folder, res_folder):
    logger = logging.getLogger(__name__)
    file_num = len(file_list)
    res = ""
    tmp = ""
    if file_num == 1: 
        logger.info(f"move file: {file_list} from {source_folder} to {res_folder}")
        sort_singal_file(file_list[0], source_folder, res_folder)
        return (res_folder, source_folder)
    else:
        group_len = (file_num+3) // 4 if file_num > 4 else 1
        grouped_files = [file_list[i:i+group_len] for i in range(0,file_num,group_len)]
        for group in grouped_files:
            if group :
                tmp, res = divide_and_merge(group, source_folder, res_folder)
        merge_files(grouped_files, res, tmp)
    return (res, tmp)


if __name__ == '__main__':
    ans_file = ["dump_59.0.xml","dump_60.0.xml","dump_61.0.xml","dump_62.46856.xml"]
    source_folder="D:/联机的文件/入学文件/毕业设计/code/test/A"
    res_folder="D:/联机的文件/入学文件/毕业设计/code/test/B"
    sort_singal_file(ans_file, source_folder, res_folder)
    res,tmp = divide_and_merge(ans_file, source_folder, res_folder)
    print(res)
    pass
