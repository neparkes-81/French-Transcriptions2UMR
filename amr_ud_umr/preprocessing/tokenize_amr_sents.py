import re

"""
This script converts Ding AMR files into a valid input file for Flaubertagger
 - input:
    .amr or .txt file in amr format

 - output:
    .txt file
    outputed in folder "preprocessing/output"
    example output:
        10 points ?
        si vous voulez
        je
        ...
"""

# Return the sentences only with tokenization with spacing on same line
def read_sents(file):
    print('Tokenizing...')
    with open(file, 'r', encoding='utf-8') as f:
        sentences = []
        for line in f:
            if line.startswith('# ::snt '):
                # format sentence for tokenizing
                line = line[8:]
                line = re.sub('\'', '\' ', line)
                line = re.sub('-', ' -', line)

                # reform tokenized phrases - peut-être
                line = re.sub('peut -être', 'peut-être', line)

                sentences.append(line)

        return sentences

def get_comments(file):
    with open(file, 'r', encoding='utf-8') as f:
        comments = []
        comment = ""
        new_comment = False
        for line in f:
            if line.startswith('# ::id'):
                line = line[7:]
                comment += f"# sent_id = {line}"
                new_comment = True
            elif line.startswith('# ::snt'):
                line = line[8:]
                comment += f"# text = {line}"
            elif new_comment:
                comments.append(comment)
                comment = ""
                new_comment = False
    return comments

# Return sentences with non-verbal and unintelligible sound transcriptions removed
def clean_sentences(sentences, comments):
    print('Cleaning...')
    cleaned_sentences = []
    cleaned_comments = []
    c_i = 0
    for sentence in sentences:
        # remove non-verbal and unintelligible sound transcriptions
        sentence = re.sub('\((.*?)\)|\[(.*?)]|<(.*?)>', '', sentence)
        # fix spacing
        sentence = ' '.join(sentence.split())
        sentence = sentence.strip()
        if sentence:
            # append sentences with "\n" so each on new line
            cleaned_sentences.append(sentence + "\n")
            if c_i == 0:
                cleaned_comments.append("# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC\n" + comments[c_i])
            else:
                cleaned_comments.append(comments[c_i])
            cleaned_comments.append("\n") #new line between each comment section
        c_i += 1

    return cleaned_sentences, cleaned_comments

# Write formatted data to a file
def write_sentences(sentences, filename):
    print('Writing sentences...')
    file = f"preprocessing/output/{filename.split('/')[-1]}_input.txt"

    with open(file, 'w', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(sentence)

    return file


# Consolidate all helper functions to one function to retrieve input and produce output file
def tokenize(filename):
    print('Converting data...')
    sentences = read_sents(filename)
    comments = get_comments(filename)
    cleaned_sentences, cleaned_comments = clean_sentences(sentences, comments)
    return write_sentences(cleaned_sentences, filename), cleaned_comments

