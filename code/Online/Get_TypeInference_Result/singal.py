import logging

from Online.obj import ModelAccesser


def combine_res_data(api_elems, json_res, prev_data:dict):
    remain_api = []
    for node in api_elems:
        if node in json_res.keys():
            ans = json_res[node]
            prev_data[node] = ans
        else:
            remain_api.append(node)
    return remain_api,prev_data


def handle_remain_api(remain_node, prev_data):
    ans = "<FQN not provided, as it seems to be a custom interface or not present in the code snippet>"
    for node in remain_node:
        prev_data[node] = ans
    return prev_data


def get_result_singal(question, api_elems):
    logger = logging.getLogger(__name__)
    model_acs = ModelAccesser()
    res_data = []
    remain_len = len(api_elems)+1
    prev_num = remain_len+1
    remain_api = api_elems.copy()
    get_response = True
    while remain_len>0 and remain_len<prev_num:
        try: 
            res_json = model_acs.get_result(question)
        except:
            get_response = False 
            break
        # handle result
        remain_api,res_data = combine_res_data(remain_api,res_json,res_data)
        prev_num = remain_len
        remain_len = len(remain_api)
        # logger.debug("res_data len: ",len(res_data),"remain_api_len: ",remain_len,"prev_num: ",prev_num)

    if len(res_data)==0 or not get_response:
        logger.error("Failed to get response from ChatGPT")
        exit(1)
    else:
        res_data = handle_remain_api(remain_api,res_data)
    return res_data


if __name__ == '__main__':
    api_dict = [
        {
            "Node": "Activity",
            "Truth": "android.app.Activity"
        },
        {
            "Node": "Bundle",
            "Truth": "android.os.Bundle"
        },
        {
            "Node": "TextView",
            "Truth": "android.widget.TextView"
        }
    ]
    json_res = {
        "Activity": "123",
        "Bundle": "223",
    }
    prev_data = []
    remain_api = combine_res_data(api_dict, json_res, prev_data)
    handle_remain_api(remain_api, prev_data)
    print(prev_data)
    pass