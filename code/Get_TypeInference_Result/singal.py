def combine_res_data(api_dict, json_res, prev_data):
    remain_api = []
    for dic in api_dict:
        node = dic["Node"]
        truth = dic["Truth"]
        if node in json_res.keys():
            ans = json_res[node]
            prev_data.append([node,ans,truth])
        else:
            remain_api.append(dic)
    return remain_api,prev_data


def handle_remain_api(remain_dic, prev_data):
    ans = "<FQN not provided, as it seems to be a custom interface or not present in the code snippet>"
    for dic in remain_dic:
        node = dic["Node"]
        truth = dic["Truth"]
        prev_data.append([node,ans,truth])
    return prev_data


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
    remain_api = combine_res_data(api_dict,json_res,prev_data)
    handle_remain_api(remain_api,prev_data)
    print(prev_data)
    pass