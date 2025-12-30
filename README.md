# French AMR to UMR
This repository showcases my contribution to the DinG project retrieving semantic data from spontaneous French dialouge. Here, I define a workflow for converting
our AMRs of French speech transcriptions to automatically-produced semi-completed UMRs.
We specifically developed a pipeline which converts our transcriptions into Universal Dependency
trees, then into Uniform Meaning Representations, or UMRs.

## Set up Enviornment
This pipeline for converting French AMR to UMR requires the Python packages `penman`, `udapi` `word2number`, `googletrans==4.0.0-rc1`, `scikit-learn`, and `stanza`
all listed in the `requirements.txt` file. We outline the steps for creating a proper python enviornment below:

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
The code creates a direct pipeline from French AMR to UMR ouput. Thus, only the following
argument is required
* `--amr`: The path to the amr file. Anticipate .amr or .txt file in format seen in Ding amr files.

We provide an example command with an **input file**. The following input file is provided directly from the DinG corpus in the data directory, as seen below:

```commandline
 python3 amr_to_umr.py --amr data/ding1/ding1-1.coref_ellipsis.only.amr
```
The final **output file** can be found in `ud_umr/output/`. Any other intermediary outputs, such as
preprocessed data or universal dependencies, can be found in their respective directories.

## Files
As mentionned prior, outputs for any step of the process can be found in their respective
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
## Cited Works

> Gamba, F., Palmer, A., and Zeman, D. (forth.). Bootstrapping UMRs from Universal Dependencies for Scalable Multilingual Annotation.
>
> Peng Qi, Yuhao Zhang, Yuhui Zhang, Jason Bolton and Christopher D. Manning. 2020. Stanza: A Python Natural Language Processing Toolkit for Many Human Languages. In Association for Computational Linguistics (ACL) System Demonstrations. 2020.
>
>Kang, Jeongwoo & Boritchev, Maria & Coavoux, Maximin. (2025). ding-01 :ARG0: An AMR Corpus for Spontaneous French Dialogue. 10.48550/arXiv.2508.12819. 
