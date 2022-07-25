#processing xfst output
#outputs morphological segmented Quechua words, one sentence per line

import re
import json
import sentencepiece as spm

infile = open ('', 'r', encoding = 'utf8') # path to original file to be changed
outfile = open('', 'w', encoding = 'utf8') # path to new file
# uncomment for dev and test
vocab_json = open('train.trg.json') # path to json vocab file from target side
vocab = json.load(vocab_json)

sentence = []
prev_line_empty = True
line = infile.readline()
prev_token = ''

sp = spm.SentencePieceProcessor(model_file='spm_normalized.joint.model') # from Nematus model file

while line != '':
    cols = line.strip().split('\t') 
    # skip if multiple possible morphological analyses available, 
    # we only consider the first
    j=-1
    for w in cols[0].split():
        j=j+1
        if prev_token!= w:
            prev_token = w
        else:
            cols.pop(j)

    if line == '': # skip empty lines
        prev_line_empty == True
        continue
    
    if cols[0] == 'EOS': 
        # at EOS symbol we can write previous subwords to the output file as a sentence
        outfile.write(f'{" ".join(sentence)}\n')
        sentence = []

    elif len(cols) == 2: # process words with morphological analysis available
        morphs = re.sub(r'(?!\]\[)\](.)',r'\] \1',cols[1]).split()
        #add '▁' before every token for sentencepiece model > decode
        morphs[0] = '▁' + morphs[0]
        only_tokens = []
        
        for morph in morphs:
            morph = re.sub(r'\[', r' \[', morph)
            morph = re.sub(r'\\', '', morph)
            #remove @mMi if it occurs in one of the subwords
            token, *analysis = morph.split()
            token = re.sub(r'\@(.*)', '', token)

            #if the root is spanish, split additionally with spanish sentencepiece model
            if '[NRootES]' in analysis:
                token = sp.encode(token, out_type=str)
                for i in token:
                    only_tokens.append(i)
            elif '[VRootES]' in analysis:
                token = sp.encode(token, out_type=str)
                for i in token:
                    only_tokens.append(i)
            elif '[NRootG]' in analysis:
                token = sp.encode(token, out_type=str)
                for i in token:
                    only_tokens.append(i)
            elif '[VRootG]' in analysis:
                token = sp.encode(token, out_type=str)
                for i in token:
                    only_tokens.append(i)
            elif '[NP]' in analysis:
                token = sp.encode(token, out_type=str)
                for i in token:
                    only_tokens.append(i)
            elif '[CARD]' in analysis:
                token = sp.encode(token, out_type=str)
                for i in token:
                    only_tokens.append(i)


            # uncomment for dev and test
            # for dev and test files additionally 
            # check if every morpheme is in the quechua vocab.json, if not split with sentencepiece
            elif token not in vocab.keys():
                token = sp.encode(token, out_type=str)
                for i in token:
                    only_tokens.append(i)
            else:
                only_tokens.append(token)
               
        sentence.extend(only_tokens)

    elif len(cols) == 3: # process words with no morphological analysis
        # split word in subwords using spanish sentencepiece model
        word = cols[0]
        words = sp.encode(word, out_type=str)
        for word in words:
            sentence.append(word)

    prev_line_empty == False
    line = infile.readline()

infile.close()
outfile.close()