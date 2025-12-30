import stanza
from stanza.utils.conll import CoNLL

"""
This script converts sentences to completely annotated conllu file 
 adds original Ding corpus sentences/ sentence ids to stanza produced UD trees
 - input:
    .txt file
    expected in folder "preprocessing/output"

 - output:
    .conllu file
    outputed in folder labeled "amr_ud/output"
"""

def get_sentences(filename): # anticipate file of only used sentences (complete ud or something specific)
    with open(filename, 'r', encoding='utf-8') as f:
        sentences = f.readlines()
        return sentences

def get_stanza(filename): # anticipate file of only used sentences (complete ud or something specific)
    with open(filename, 'r', encoding='utf-8') as f:
        stanza = f.readlines()
        return stanza

def if_not_in(sentences, stanza):
    for line in stanza:
        if line.startswith('#text = ') and line[len('#text = '):] not in sentences:
            print(line)


def add_comments(sentences, comments, stanza): # anticipate stanza produced file
    corrected_ud = []

    c_i = 0
    st_i = 0

    # iterate through sentences, add comments if text = sent
    for _ in range(len(sentences)):
        while comments[c_i] != "\n":
            if comments[c_i].startswith('#'):
                corrected_ud.append(comments[c_i])
            c_i += 1
        c_i += 1

        while stanza[st_i] != "\n":
            if not stanza[st_i].startswith('#'):
                corrected_ud.append(stanza[st_i])
            st_i += 1
        st_i += 1

        corrected_ud.append("\n")

    return corrected_ud

# columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC
# French/ding specfic fixes - untested

def fix_nes(uds):
    nes = ['JAUNE', 'BLEU', 'ROUGE', 'BLANC', 'Jaune', 'Bleu', 'Rouge', 'Blanc']
    fixed_uds = []
    for line in uds:
        if not line.startswith('#') and line != '\n':  # if not a comment or newline
            # split column with '\t' del and check for FORM including NameEntity (ne)
            cols = line.split('\t')
            if cols[1] in nes:
                cols[3] = "PROPN" # change UPOS to PROPN
                cols[2] = cols[1] # make sure lemma matches form
                line = '\t'.join(cols)
        fixed_uds.append(line)
    return fixed_uds


def fix_negation(uds):
    fixed_uds = []
    for line in uds:
        if not line.startswith('#') and line != '\n': # if not a comment or newline
            # split column with '\t' del and check for FEATS including 'prontype=Neg'
            cols = line.split('\t')
            if "PronType=Neg" in cols[5]:
                if not ("Polarity=Neg" in cols[5]):
                    cols[5] += "|Polarity=Neg" # add Polarity=Neg
                    line = '\t'.join(cols)
        fixed_uds.append(line)
    return fixed_uds


def stanza2ding(stanza_file, comments, sents):
    sentences = get_sentences(sents)
    stanza = get_stanza(stanza_file)
    if_not_in(sentences, stanza)
    corrected_ud = add_comments(sentences, comments, stanza)
    corrected_ud = fix_nes(corrected_ud)
    corrected_ud = fix_negation(corrected_ud)
    with open(stanza_file, 'w', encoding='utf-8') as f:
        for line in corrected_ud:
            f.write(line)



def amr_to_ud(input, comments):
    # Download/ make sure the French model is downloaded
    stanza.download("fr")

    # Load the French pipeline, indicate that sentences are pre-tokenized
    nlp = stanza.Pipeline(lang="fr", tokenize_pretokenized=True)
    f = input
    text = ""
    with open(f, 'r', encoding='utf-8') as f:
        text = f.read()

    doc = nlp(text)  # run annotation over a sentence
    data_name = input.split("/")[-1].split(".")[0]
    output_file = f"amr_ud/output/{data_name}_complete_uds.conllu"
    CoNLL.write_doc2conll(doc, output_file)

    # Convert stanza output to reflect ding ids and original sentences
    stanza2ding(output_file, comments, input)
    return output_file