import argparse
import subprocess
from pathlib import Path
import preprocessing.tokenize_amr_sents as preprocess
import amr_ud.amr_ud_via_Stanza as to_ud

parser = argparse.ArgumentParser()
parser.add_argument("--amr", help="Path to the Ding AMR file.", required=True)



if __name__ == "__main__":
    ### STEP 1 - Preprocess AMR file to obtain tokenized sentences and comments from transcriptions
    args = parser.parse_args()

    # returns the path of the output file & returns a list of comments
    tokenized_sentences, comments = preprocess.tokenize(args.amr)


    ### STEP 2 - Create UDs given input data provided above
    data_name = tokenized_sentences.split("/")[-1].split(".")[0]
    uds = f"amr_ud/output/{data_name}_complete_uds.conllu"

    file_path = Path(uds)
    # returns the path of the output file, avoids running stanza if not necessary
    uds = uds if file_path.exists() else to_ud.amr_to_ud(tokenized_sentences, comments)


    ### STEP 3 - Convert UDs to UMR
    lang = "fr"
    project_root = Path(__file__).resolve().parent
    sub_dir = project_root / "ud_umr"

    cmd = [
        "python3",
        "scripts/main.py",
        "--treebank", f"../{uds}",
        "--lang", lang
    ]
    # runs the UD2UMR code using the uds outputted above
    result = subprocess.run(cmd, cwd=sub_dir, check=True)




