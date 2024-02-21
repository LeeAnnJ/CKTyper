def combine_res_data(api_dict,json_res):
    data = []
    for dic in api_dict:
        node = dic["Node"]
        truth = dic["Truth"]
        ans = "\"<FQN not provided, as it seems to be a custom interface or not present in the code snippet>\""
        if node in json_res.keys():
            ans = json_res[node]
        data.append([node,ans,truth])
    return data

if __name__ == '__main__':
    # api_dict = [
    #     {
    #         "Node": "Activity",
    #         "Truth": "android.app.Activity"
    #     },
    #     {
    #         "Node": "Bundle",
    #         "Truth": "android.os.Bundle"
    #     },
    #     {
    #         "Node": "TextView",
    #         "Truth": "android.widget.TextView"
    #     }
    # ]
    # json_res = {
    #     "Activity": "123",
    #     "Bundle": "223",
    # }
    # data = combine_res_data(api_dict,json_res)
    # print(data)
    pass