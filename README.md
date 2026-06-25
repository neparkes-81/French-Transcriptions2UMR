# French AMR to UMR
This repository showcases my contribution to the DinG project, retrieving semantic data (the core, unambiguous meaning) from utterances of spontaneous French dialogue. This project has collected ample human annotations in Abstract Meaning Representation (AMR) format. Although, as AMR was built for English, we seek to convert these annotations to Uniform Meaning Representations (UMRs), a language-agnostic notation which can better reflect the nuances of French speech and thus, lend a more accurate hand to downstream NLP tasks (text summarization, machine translation edge cases, etc.). 

Here, I define a workflow for automatically converting
our AMRs of French speech transcriptions to semi-completed UMRs. We specifically developed a pipeline which converts our transcriptions into Universal Dependency (UD)
trees, then into UMRs. This automation will reduce annotation labor for future linguistic researchers on this project.

## Table of Contents
- [My Contribution](#my-contribution)
- [Architecture](#architecture)
- [Set up Environment](#set-up-environment)
  - [1 ) Create conda environment](#1--create-conda-environment)
  - [2 ) Install packages](#2--install-packages)
  - [3 ) Set Up Directories](#3--set-up-directories)
- [Run the Code](#run-the-code)
- [Files](#files)
- [Limitations](#limitations)
- [Cited Works](#cited-works)

## My Contribution
I built the preprocessing pipeline to convert speech transcriptions into UD trees utilizing heuristic data cleaning/ parsing and Stanza integration for UD conversion. I wrote formatting script to prepare this output for UD-to-UMR conversion. Finally, I completed the pipeline by augmenting pre-built UD-to-UMR conversion scripts to work with our data and annotation rules.

## Architecture
![Architecture Diagram](./assets/French%20AMR%20Conversion-2026-06-25-155631.png)

## Set up Environment
This pipeline for converting French AMR to UMR requires the Python packages `penman`, `udapi` `word2number`, `googletrans==4.0.0-rc1`, `scikit-learn`, and `stanza`
all listed in the `requirements.txt` file. We outline the steps for creating a proper python environment below:

### 1 ) Create conda environment 
```
conda create -n amr_to_umr python=3.11
conda activate amr_to_umr
```
### 2 ) Install packages 
```
pip install -r requirements.txt
```
### 3 ) Set Up Directories
```
mkdir -p amr_ud/output
mkdir -p preprocessing/output
```

## Run the Code
The code creates a direct pipeline from French AMR to UMR output. Thus, only the following
argument is required
* `--amr`: The path to the amr file. Anticipate .amr or .txt file in format seen in Ding amr files.

We provide an example command with an **input file**. The following input file is provided directly from the DinG corpus in the data directory, as seen below:

```commandline
 python3 amr_to_umr.py --amr data/ding1/ding1-1.coref_ellipsis.only.amr
```
The final **output file** can be found in `ud_umr/output/`. Any other intermediary outputs, such as
preprocessed data or universal dependencies, can be found in their respective directories.

## Files
As mentioned prior, outputs for any step of the process can be found in their respective
`output/` directories. The contents of `ud_umr/` is forked from the UD2UMR project. The organization of such folders and project scripts can
be found below:

```
amr_to_umr.py
preprocessing/
├── output/                    
└── tokenize_amr_sents.py    
amr_ud/                                     
├── output/                    
└── amr_ud_via_Stanza.py                     
ud_umr/                                    
├── output/                    
├── external_resources/ 
│ ├── fr/
│ │ ├── advcl.csv
│ │ ├── conj.json
│ │ ├── have-rel-role.txt
│ │ └── modality.json
│ └── en/
│   ├── advcl.csv
│   ├── conj.json
│   ├── have-rel-role.txt
│   └── modality.json
└── scripts/                                    
  ├── prepare_eval (...)                               
  ├── main.py                              
  ├── umr_graphs.py
  ├── umr_node.py
  ├── preprocess.py    
  ├── print_structure.py    
  ├── evaluate_ancast.py                   
  └── tests_ancast.py
requirements.txt                              
README.md         
```

## Limitations
Due to the usage of Stanza's neural pipeline for UD conversion, I note some variable noise in its output where productions unique to spoken language in our collected transcriptions diverted from, or showed limited occurrence in the model's training data. While certain issues were systematically fixed in the augmented UD-to-UMR script, I still heavily advise human review to ensure accuracy of all outputs.

## Cited Works

> Gamba, F., Palmer, A., and Zeman, D. (forth.). Bootstrapping UMRs from Universal Dependencies for Scalable Multilingual Annotation.
>
> Peng Qi, Yuhao Zhang, Yuhui Zhang, Jason Bolton and Christopher D. Manning. 2020. Stanza: A Python Natural Language Processing Toolkit for Many Human Languages. In Association for Computational Linguistics (ACL) System Demonstrations. 2020.
>
>Kang, Jeongwoo & Boritchev, Maria & Coavoux, Maximin. (2025). ding-01 :ARG0: An AMR Corpus for Spontaneous French Dialogue. 10.48550/arXiv.2508.12819. 
