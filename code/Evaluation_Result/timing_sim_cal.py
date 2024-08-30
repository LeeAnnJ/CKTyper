import time
from lxml import etree
from nltk import word_tokenize
from crystalbleu import corpus_bleu


def timing_crystalbleu_calculation():
    cs_num = 1000
    test_time = 50
    cs_file = f"../data/SOData/SO_multi_row_code_snippets/dump_01.0.xml"
    cs_list = []

    count = 0
    context = etree.iterparse(cs_file, events=('end',), tag='code')
    for event, row in context:
        cs_list.append(row.get('Code'))
        row.clear()
        count += 1
        if count >= cs_num: break
    del context

    start_time = time.time()
    for i in range(0,test_time):
        hyp = word_tokenize(cs_list[i])
        for j in range(0, cs_num):
            ref = word_tokenize(cs_list[j])
            corpus_bleu([hyp], [ref])
    end_time = time.time()
    average = (end_time-start_time)/test_time
    print(f"Average time spent on calculating CrystalBLEU for {cs_num} times: {average}")
    pass

if __name__ == '__main__':
    timing_crystalbleu_calculation()