# CKTyper: Croudsourcing Knowledge Enhanced Type Inference
## Overview
The source code of CKTyper is in `~/code`.

The experimental data of CKTyper is in `~/Data`

```
CKTyper
|—— Code
|    |—— config
|    |—— Java
|    |    |—— LuceneIndexer
|    |    └—— Snr-LibraryParser
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
3. Download `punkt_tab` from NLTK downloader:
```python
import nltk
nltk.download('punkt_tab')
```
4. Get your API keys from [openai](https://platform.openai.com/api-keys) to access ChatGPT.
5. Complete the settings for all files in the `config` folder, specific instructions can be found in [`~/code/config/note.md`](./code/config/note.md)

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
