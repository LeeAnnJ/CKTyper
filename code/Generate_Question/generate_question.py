import json

class QuestionGenerator:
    frame_file = "./Generate_Question/question_for_ChatGPT.json"

    def __init__(self) -> None:
        with open(self.frame_file, 'r') as qf:
            question_frame = json.load(qf)
        self.head = question_frame["head"]
        self.api_text = question_frame["api_text"]
        self.prompt_text = question_frame["prompt_text"]
        pass

    def generate_question(self, code, apis:list, prompt:list|None,original:bool=False):
        question = self.head+code+self.api_text+str(apis)
        if not original:
            question += self.prompt_text+str(prompt)
        return question


if __name__ == '__main__':
    # code = "here's code"
    # apis = ['api1', 'api', 'api']
    # prompt = ['xx', "xx", 'xx']
    # qg = QuestionGenerator()
    # question = qg.generate_question(code,apis,prompt)
    # print(question)
    pass