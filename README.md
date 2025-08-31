# DPLP-German RST Parser & EDU Segmenter

- [DPLP-German RST Parser \& EDU Segmenter](#dplp-german-rst-parser--edu-segmenter)
  - [Setup](#setup)
  - [EDU Segmenter for German](#edu-segmenter-for-german)
    - [Segmenter: run segmentation pipeline](#segmenter-run-segmentation-pipeline)
      - [Parser: run DPLP-German](#parser-run-dplp-german)
  - [Retrain DPLP-German with a Custom Corpus](#retrain-dplp-german-with-a-custom-corpus)
    - [Step 1: Prepare and Split Your Corpus](#step-1-prepare-and-split-your-corpus)
    - [Step 2: Train the Model](#step-2-train-the-model)
    - [Step 3: Predict with Your New Model](#step-3-predict-with-your-new-model)
  - [DPLP-German (original README.md)](#dplp-german-original-readmemd)
    - [1. Introduction](#1-introduction)
    - [2. Runtime Docker Image](#2-runtime-docker-image)
    - [3. RST Parsing from text files](#3-rst-parsing-from-text-files)
    - [4. RST Parsing with the Restful API](#4-rst-parsing-with-the-restful-api)
    - [5. Training Your Own RST Parser](#5-training-your-own-rst-parser)
    - [Reference](#reference)

## Setup

<details>
  <summary>Click to expand</summary>

- clone repository

  ```bash
  git clone git@github.com:MaximilianKr/DPLP-German.git
  ```

  ```bash
  cd DPLP-German
  ```

- create virtual environment (using [uv](https://github.com/astral-sh/uv))

  ```bash
  uv venv --python 3.10
  ```

  ```bash
  source .venv/bin/activate
  ```

  ```bash
  uv pip install -r requirements.txt
  ```

- pull docker image

  ```bash
  docker pull mohamadisara20/dplp-env:ger
  ```

</details>

## EDU Segmenter for German

<details>
  <summary>Click to expand</summary>

From `root/DPLP-German`:

- put `.txt` file(s) to parse into `data/{folder}`
  - for example, using `data/test_input` --> adjust `{input_folder}`
- segmenter will output `.txt` with line-separated EDUs
  - adjust `{output_folder}` accordingly

### Segmenter: run segmentation pipeline

- run segmenter
  
  ```bash
  python run_seg_pipeline.py {input_folder} {output_folder}
  ```

  - for example:

    ```bash
    python run_seg_pipeline.py data/test_input data/test_output
    ```

#### Parser: run DPLP-German

- run parser

  ```bash
  docker run -it \
    -v $(pwd):/home/DPLP \
    -w /home/DPLP \
    mohamadisara20/dplp-env:ger \
    python3 ger_predict_dis_from_txt.py {input_folder}
  ```

  - for example:
  
    ```bash
    docker run -it \
      -v $(pwd):/home/DPLP \
      -w /home/DPLP \
      mohamadisara20/dplp-env:ger \
      python3 ger_predict_dis_from_txt.py data/test_input
    ```

</details>

## Retrain DPLP-German with a Custom Corpus

### Step 1: Prepare and Split Your Corpus

<details>
  <summary>Click to expand</summary>

Before training, your corpus of `.rs3` files must be split into `training`, `dev`, and `test` sets.

1. **Ensure your annotated `.rs3` files are in a single source directory**.

2. **Run the splitting script**:

    ```bash
    python3 scripts/split_corpus.py <source_directory> <destination_directory> --split <train_count> <dev_count> <test_count>
    ```

    - `<source_directory>`: The directory containing your full set of `.rs3` files.
    - `<destination_directory>`: The base path where `training/`, `dev/`, and `test/` subdirectories will be created (e.g., `data/my_corpus`).
    - `--split`: The number of files for the training, dev, and test sets.
    - `--seed` (optional): A number to seed the random shuffle for reproducibility (defaults to `42`).

    **Example:**
    To split 176 files from `data/pcc/rs3` into a training set of 141, a dev set of 18, and a test set of 17 inside `data/pcc`, run:

    ```bash
    python3 scripts/split_corpus.py data/pcc/rs3 data/pcc --split 141 18 17
    ```

</details>

### Step 2: Train the Model

<details>
  <summary>Click to expand</summary>

Once your data is split, you can train the model using the `train_custom_model.sh` script. Simply provide the path to your corpus directory as an argument.

- Run the training:

    ```bash
    bash train_custom_model.sh <corpus_base_path>
    ```

  - `<corpus_base_path>`: The destination directory you used in the splitting step (e.g., `data/pcc`).

    Example:

    ```bash
    bash train_custom_model.sh data/pcc
    ```

    The script will automatically generate a custom relation map and run the entire training pipeline. The model files will be saved to `<corpus_base_path>` with evaluation results in `<corpus_base_path>/result.txt`.

</details>

### Step 3: Predict with Your New Model

<details>
  <summary>Click to expand</summary>

After training, you can use your custom model to parse new `.txt` files.

- Run prediction:

    ```bash
    bash predict_with_custom_model.sh <corpus_base_path> <input_directory> <output_directory>
    ```

  - `<corpus_base_path>`: The path to the corpus directory containing your trained model.
  - `<input_directory>`: The directory containing your new `.txt` files.
  - `<output_directory>`: The directory where the output `.dis` and `.rs3` files will be saved.

    Example:

    To parse files from `data/pcc/test_input` using the model in `data/pcc` and save the parsed results to `data/pcc/test_output`, run:

    ```bash
    bash predict_with_custom_model.sh data/pcc data/pcc/test_input data/pcc/test_output
    ```

</details>

## DPLP-German (original README.md)

<details>
  <summary>Click to expand</summary>

### 1. Introduction

This repository is a fork of [DPLP Parser](https://github.com/jiyfeng/DPLP) that customizes the code for German language by adding new pieces of codes and other resources. A ready to use model is trained by the Postdam University RST Corpus. The pretrained model can be found in **./data/de** along with all its belongings. The source code consists of several python scripts in the root directory, prefixed by _ger_.

### 2. Runtime Docker Image

DPLP Parser was written Python 2 that is discontinued, and depends on libraries that can't be installed by the package managers anymore. Therefore a prebuild Docker image (_mohamadisara20/dplp-env_) is created and shared in Docker Hub that contains all of them preinstalled. Both German and the original English DPLP parsers can be executed within this image. The image can be found here:
https://hub.docker.com/repository/docker/mohamadisara20/dplp-env/general
There are two tags created for this docker image:

- **latest**: the default tag suitable for running the English DPLP parser.
- **ger**: the tag created for running German DPLP. It has some language-specific libraries and data files pre-installed.

### 3. RST Parsing from text files

The German RST parser's main script is ger_predict_dis_from_txt.py (it generates RST trees in both .dis and .rs3 formats). All the preprocessings, segmentation and parsing are included; so the script simply takes text files as input and generates the RST trees as its ultimate output. You can follow these steps to parse a batch of text files using this script in a docker container:

1- in terminal, change directory to the repo's root path:

```bash
cd path_to_rst_german
```

2- copy the _.txt_ input files in a single subdirectory in **./data** (let's say: **data/input**). Please don't choose any place ourside the current directory.

3- run the following command:

```bash
docker run -d -v $(pwd):/home/DPLP -w /home/DPLP mohamadisara20/dplp-env:ger python3 ger_predict_dis_from_txt.py data/input
```

- **Important**: replace `data/input` with the _relative_ path to your input text files. You don't need to change anything else for standard parsing. For customization with additional args, refer to the parser script's source code.

4- There are several ways to check the progress or debug errors:

- verify the new files created in the input path
- replace `-d` option with `-it` to get all logs printed throughout the process
- use `docke logs` to see the logs generated by the Docker container

5- you will see new files created throughout the parsing process. When _.rs3_ files are generated, it means that the process is finished.

### 4. RST Parsing with the Restful API

The script **ger_rest_api.py** creates a REST-API server that allows us to perform RST parsing remotely or integrate it into a web application. It can be launched by running:

```bash
docker run -d -p 5000:5000 -v $(pwd):/home/DPLP -w /home/DPLP mohamadisara20/dplp-env python3 ger_rest_api.py
```

Then the REST-API will listen to port 5000 and accept JSON requests from the subpath **dplp** and return the RST tree in two formats _dis_ and _rs3_. You can test it using this command:

```bash
curl -d '{"text":"Ich bin gut."}' -H 'Content-Type: application/json' http://127.0.0.1:5000/dplp
```

You will get a result like this:

```text
{
    "dis": "(Root (leaf 1) (rel2par None) (text _!lorem ipsum_!))\n",
    "rs3":"<rst>\n
        <header>\n <relations>\n      <rel name=\"Antithesis\" type=\"rst\"/>\n      
            <rel         name=\"Background\" type=\"rst\"/>\n      <rel name=\"Cause\" type=\"rst\"/>\n      <rel name=\"Circumstance\" type=\"rst\"/>\n      <rel name=\"Concession\" type=\"rst\"/>\n      <rel name=\"Condition\" type=\"rst\"/>\n      <rel name=\"Conjunction\" type=\"multinuc\"/>\n      <rel name=\"Contrast\" type=\"multinuc\"/>\n      <rel name=\"Disjunction\" type=\"multinuc\"/>\n      <rel name=\"Elaboration\" type=\"rst\"/>\n      <rel name=\"Enablement\" type=\"rst\"/>\n      <rel name=\"Evaluation\" type=\"rst\"/>\n      <rel name=\"Evidence\" type=\"rst\"/>\n      <rel name=\"Interpretation\" type=\"rst\"/>\n      <rel name=\"Joint\" type=\"multinuc\"/>\n      <rel name=\"Justify\" type=\"rst\"/>\n      <rel name=\"Motivation\" type=\"rst\"/>\n      <rel name=\"Otherwise\" type=\"rst\"/>\n      <rel name=\"Preparation\" type=\"rst\"/>\n      <rel name=\"Purpose\" type=\"rst\"/>\n      <rel name=\"Restatement\" type=\"rst\"/>\n      <rel name=\"Result\" type=\"rst\"/>\n      <rel name=\"Sequence\" type=\"multinuc\"/>\n      <rel name=\"Solutionhood\" type=\"rst\"/>\n      <rel name=\"Summary\" type=\"rst\"/>\n
        </relations>\n</header>\n  
        <body>\n
            <segment id=\"2\">Ich bin gut .</segment>\n 
        </body>\n </rst>",
    "dis_url":"rstout/5d74b5b2-18c6-4443-9d5f-b67ebfe947a3/document.dis",
    "rs3_url":"rstout/5d74b5b2-18c6-4443-9d5f-b67ebfe947a3/document.rs3","uid":"5d74b5b2-18c6-4443-9d5f-b67ebfe947a3"}
```

### 5. Training Your Own RST Parser

You can train your own parser using a corpus of RST trees. German parser uses _.rs3_ files for training. Training consists of these steps:

1- Divide the corpus into train, dev and test set and save them in three subdirectores **training/**, **dev/** and **test/** in a _base_ directory ; for instance, if the base directory is _data/base_dir_, we will get these sub directories: **data/base_dir/training**, **data/base_dir/dev** and **data/base_dir/test**.

2- Review the content of the relation mapping file: _parsing\_eval\_metrics/rel\_mapping.json_. It should contain all relations used in the whole corpus (train, dev and test set); otherwise training can fail and show undefind bahaviors.

3- The script _ger\_train\_parser.py_ tringgers the trining process on the base directory. You can use the following command to run the training code in the docker container:

```bash
docker run -d -v $(pwd):/home/DPLP -w /home/DPLP mohamadisara20/dplp-env:ger python3  ger_train.py data/base_dir
```

4- The model will be saved in the file **model/model.pickle.gz** in the base path (e.g. _model/de_)

5- The parser precision scrores will be reported in the file named **results.txt** in the base directory.

### Reference

Please read the following paper for more technical details

- Yangfeng Ji, Jacob Eisenstein. [Representation Learning for Text-level Parsing](http://jiyfeng.github.io/papers/ji-acl-2014.pdf). ACL 2014
- Joty, S., Carenini, G., & Ng, R. T. (n.d.). CODRA: A Novel Discriminative Framework for Rhetorical Analysis.
- Shahmohammadi, S., & Stede, M. (2024). Discourse Parsing for German with new RST Corpora. Workshop Proceedings of the 20th Edition of the KONVENS Conference.

</details>

[Back to Top](#dplp-german-rst-parser--edu-segmenter)
