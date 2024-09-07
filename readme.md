# CKTyper: Croudsourcing Knowledge Enhanced Type Inference
## Overview
The source code of CKTyper is in `~/code`.

The experimental data of CKTyper is in `~/Data`

```
CKTyper
|—— Code
|    |—— config
|    |—— LuceneIndexr
|    |—— Offline_Processing
|    |—— Online_Processing
|    └—— Evaluation_Result
|—— Data
|    |—— Dataset: StatType-SO & Short-SO
|    |—— Evaluation: RQ1 ~ RQ4
|    └—— note.md
|—— readme.md
└—— requrements.txt
```

## Setting up CKTyper
1. Enviroment for running expriment:
   - Java：openjdk 11.0.19
   - Python: Python 3.11
   - Cuda 12.1
   - PyTorch 2.2.1+cu121
2. Run `pip install -r requirements.txt`.
3. Get your API keys from [openai](https://platform.openai.com/api-keys) to access ChatGPT.
4. Complete the settings for all files in the `config` folder, specific instructions can be found in [`~/code/config/note.md`](./code/config/note.md)

## Running CKTyper
1. cd into `~/code`
2. Run offline operation: `python main.py --mode offline`
3. Run online operation: `python main.py --mode online --pattern pipeline`
4. Evaluate experimental results: `python main.py --mode evaluation --operation precision`

Other available arguments:
```
--log_file: save the log into a file
--log_level [LEVEL]: adjust the log level to [LEVEL] (info, debug, warning, error or critical)
```

## BaseLines
### MLMTyper
This method was proposed in [`Prompt-tuned Code Language Model as a Neural Knowledge Base for Type Inference in Statically-Typed Partial Code(ASE22)`](https://dl.acm.org/doi/abs/10.1145/3551349.3556912).

The source code is from [https://github.com/SE-qinghuang/ASE-22-TypeInference](https://github.com/SE-qinghuang/ASE-22-TypeInference).

#### Modification
In order to **enable the source code to run on GPU in a Linux environment**, we have made minimal modifications(in` ~/Prompt-tune/ASE_prompt_tuning/PromptInference/Practicality/predDictData_line.py`), mainly correcting some errors and transferring the model and data to GPU.  Modifications are done as follows:  
- Change the jar file name from 'Spoon_FQN_3.jar' to 'Spoon_FQN.jar' (in *ground_truth* function)
- Change the *cmd* variable from '"java -jar "+jar_package+" "+lib_path' to '['java','-jar',jar_package,lib_path]' (in *ground_truth* function)
- Change the *cmd* variable from ' 'javac ' + file_path' ' to '['javac',file_path]' (in *ground_truth* function)
- Change the file splitter of json_fileName from '\\\\' to '/' (in *file_read* function )
- Change the file splitter of Spoon_FQN.jar from '\\\\' to '/'
- Change all Chinese characters in the code to English(in *predictData_Gen*,*file_writer*,*Itera_Pred()init* function)
- Move model and token tensors to GPU in (in *Itera_Pred()init*, *model_Pred*function)
- Change the *FQN_Truth_path* variable from 'FQN_truth' to 'FQN'(in *file_read* function)
- Change the *prompt_infer_path* and *prompt_tuning_path*(global variable)

### SnR
This method was proposed in [`SnR: Constraint-Based Type Inference for Incomplete Java Code Snippets(ICSE22)`](https://dl.acm.org/doi/abs/10.1145/3510003.3510061).

The source code is from [https://zenodo.org/record/5843327](https://zenodo.org/record/5843327).

### iJTyper
This method was proposed in [iJTyper: An Iterative Type Inference Framework for Java by Integrating Constraint- and Statistically-based Methods](https://arxiv.org/abs/2402.09995)

The source code is from [https://anonymous.4open.science/r/iJTyper-0A4D/README.md](https://anonymous.4open.science/r/iJTyper-0A4D/README.md)


# CKTyper: 众包知识增强的代码片段类型推断
## 文件结构

本项目的文件结构如下：
- code: 程序运行的目录
  - `main.py`：项目主程序
  - config：存储项目运行的各种设置文件
    - `file_structure.ini`: 配置数据集、中间结果和最终结果的存储位置
    - `chatgpt_conf.py`：配置 ChatGPT API 的 key、选择的模型和代理地址
    - `task_setting.py`：配置程序运行参数，包括数据集、API库、k 值、句子的筛选策略等
    - `text_summarizer_env`：文本摘要模型的参数设置
  - （其他源代码）
- data：实验过程中使用的数据，具体内容见数据备份（）。主要包括以下文件：
  - Dataset
  - API_elements
- Evaluation：存储实验结果的文件夹，论文中展示的实验结果参考数据备份（）。主要包括：
  - results:
  - Lucene_top_k
  - Searched_Post_Folder
  - Generated_Questions
  - Sim_Post_result
  - Intermediate
- `requirements.txt`: 项目依赖的 python 包清单

## 实验环境：
硬件配置：
- 显卡： NVIDIA GeForce RTX 3090
- 处理器: Intel(R) Xeon(R) Silver 4210R CPU@2.40GHz

软件环境：
- Java：openjdk 11.0.19
- Python: Python 3.11
- Cuda 12.1
- PyTorch 2.2.1+cu121

其他依赖：

1. python 依赖包：运行以下命令安装
```bash
pip install -r requirements.txt 
```

2. OpenAI key:
3. nltk: 在终端运行以下命令：
```bash
python
import nltk
nltk.download('punkt')
```

## 运行项目
完成实验环境配置，并将数据放在 `file_structure.ini` 对应的目录下，可根据以下步骤完成实验。

以下所有指令在 `.\code` 目录下执行。

### 数据预处理
即 `CKTyper` 的离线处理部分，运行指令为：
```bash
python main.py --mode offline
```

### 在基准数据集上进行类型推断：

```bash
python main.py --mode online --pattern pipeline
```

### 评估实验结果：

```bash
python main.py --mode evaluation
```

**附：主程序的运行参数说明**
- `--mode`: 程序运行的模式，包括 `offline`、`online` 和 `evaluation`