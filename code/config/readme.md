# Configurations in CKTyper
This folder contains parameter settings for components of CKTyper. This document explains the meaning of fields in each file, where **fields that must be configured after cloning this repository are shown in bold**.

## chatgpt_conf.py
Configs for calling ChatGPT and other LLMs:
- `PROXY_URL`: Set this field if your network environment requires a proxy to call the LLM API
- **`MODEL`: The name of the model to call.**
- **`ACCOUNTS`: Parameters required for calling LLM API using the openai library, including `api-key` and `base_url`, multiple accounts can be configured.**

## CKTyper_setting.py
Parameter configs for CKTyper components and running experiments:
- **`DATASETS`: The dataset to use for running experiments**
- **`LIBS`: Which libraries in the dataset to select for experiments**
- `LANGUAGES`: program language
- `RETRIEVAL_CONF`: Settings for retrieving similar code snippets:
  - `lucene_top_n`: Number of results to retrieve using lucene index
  - `calculate_CrystalBLEU`: Whether to enable two-stage similarity calculation
  - `similarity_top_n`: Number of results to keep using similarity calculation
- `PROMPT_CONF`: Prompt content settings:
  - `data_for_context`: Context type
  - `summarize`: Whether to summarize the context
- `RECOMMEND_TOP_K`: Number of type inference recommendations

## PEGESUS_env.py
Parameters for the text summarizer used by the CKC generator component:
- `SUM_MODEL_NAME`: The name of the selected text summarizer, defaults to [google/pegasus-xsum](https://huggingface.co/google/pegasus-xsum)
- **`CUDADIVECE`: The number of the GPU device used by the summarizer model, which can be viewed through command `nvidia-smi`. If there is no GPU on the machine, CPU will be used instead.**
- `MAX_BATCH_SIZE`: Maximum input token limit, determined by the selected summarizer model.
- `SUMMERIZATION_RATIO`: Compression ratio of input text.

## path_config.ini
Paths for input data, intermediate results, and output data, with `CKTyper/code` as the root directory:

resource part:
- **`SO_DATA_STORAGE`: The extraction directory of the official Stack Overflow archive file (typically named `stackoverflow.com-Posts.7z`), which needs to be downloaded from [https://archive.org/](https://archive.org/search?query=creator%3A%22Stack+Exchange%2C+Inc.%22)**
- `POST_DUMP_DIC`,`SO_CODE_FOLDER`: Filtered posts and code snippets related to the programming language
- `CODE_LUCENE_INDEX`,`POST_LUCENE_INDEX`: Directory where the constructed lucene index is located
- `TOKENIZER`: The name of the tokenizer used when building the lucene index
- `DATASET_CODE_FOLDER`,`API_ELEMENTS_FOLDER`: Directory where the dataset is located

intermediate part:
The actual meaning is basically the same as the field name

results part:
- **`EVAL_PATH`: Directory for storing experimental results**
- **`INFERENCE_RESULT_FOLDER`: Directory for storing inference results**