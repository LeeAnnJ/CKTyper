import utils

class ResHandler:
    empty_ans = "<FQN not provided, as it seems to be a custom interface or not present in the code snippet>"

    def __init__(self, fqn_file):
        self.fqn_set = utils.read_pickle(fqn_file)['fqn_list']
        pass

    def combine_res_data(self, api_dict, json_res, prev_data):
        remain_api = []
        for dic in api_dict:
            node = dic["Node"]
            truth = dic["Truth"]
            flag = False
            if node in json_res.keys():
                ans_list = json_res[node]
                if len(ans_list) > 1:
                    for ans in ans_list:
                        ans = ans.replace('()', '').replace('$', '.')
                        if ans in self.fqn_set:
                        # if ans.rpartition('.')[0] in self.fqn_set:
                            flag = True
                            prev_data.append([node, ans, truth])
                            break
                elif len(ans_list) > 0:
                    ans = ans_list[0].replace('()', '').replace('$', '.')
                    flag = True
                    prev_data.append([node, ans, truth])
            if not flag: remain_api.append(dic)
        return remain_api, prev_data

    def handle_remain_api(self, remain_dic, prev_data):
        for dic in remain_dic:
            node = dic["Node"]
            truth = dic["Truth"]
            prev_data.append([node, self.empty_ans, truth])
        return prev_data
