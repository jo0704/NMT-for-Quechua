#processing xfst output
#outputs morphological segmented Quechua words with tags for suffixes, one sentence per line

import re
import json
import sentencepiece as spm

infile = open ('', 'r', encoding = 'utf8') # path to original file to be changed
outfile = open('', 'w', encoding = 'utf8') # path to new file
vocab_json = open('') # path to json vocab file with tags
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
        # outfile.write(f'{" ".join(map(str,sentence))}\n')
        outfile.write(f'{" ".join(sentence)}\n')
        sentence = []

    elif len(cols) == 2: # process words with morphological analysis available
        morphs = re.sub(r'(?!\]\[)\](.)',r'\] \1',cols[1]).split()
        only_roots = []
        #add '▁' before every token for sentencepiece model > decode
        morphs[0] = '▁' + morphs[0]
        k=0
        for morph in morphs:
            k=k+1
            roots = []
            root = re.sub(r'\[(.{0,2})?([\w.\+[,]+)?\]', '', morphs[0])
            root = re.sub(r'\\', '', root) 
            root = re.sub(r'\[\-\-]', '', root)
            #remove @mMi if it occurs in one of the subwords
            root = re.sub(r'\@(.*)', '', root)
            morph = re.sub(r'\[', r' \[', morph)
            morph = re.sub(r'\\', '', morph)
            token, *analysis = morph.split()
            analysed = ' '.join(analysis)
            tags = re.sub(r'\[[^\[\+]+\]', '', analysed)
            tags = re.sub(r'\[', '', tags)
            tags = re.sub(r'\]', '', tags)
            tags = re.sub(r' ', '', tags)
            tags_list = []
            if tags != '':
                tags_list.append(tags)
            tags_list = ['▁' + x for x in tags_list]
            only_roots.extend(tags_list)

            if (k==1): #remove duplicates
                roots.append(root)
            else:
                continue
            roots = ' '.join(roots)
            roots = re.sub(r'\[=(\w+(,)?)*\]', '', roots)
    
            #if the root is spanish, split additionally with spanish sentencepiece model
            # if '[NRootES]' in analysis:
            if '[NRootES]' or '[NRootG]' or '[VRootG]' or '[NP]' or '[VRootES]' or '[CARD]' in analysis:
                roots = sp.encode(roots, out_type=str)
                for i in roots:
                    only_roots.append(i)

        
            # # for dev and test files additionally 
            # # check if every morpheme is in the quechua vocab.json, if not split with sentencepiece
            elif roots not in vocab.keys():
                roots = sp.encode(roots, out_type=str)
                # print(roots)
                for i in roots:
                    only_roots.append(i)
            else:
                only_roots.append(roots)

        # print(only_roots)
        if '▁PrnPers+3.Sg' in only_roots:
            only_roots[0:2]= only_roots[0:2][::-1]
            # print(only_roots)
        elif '▁PrnPers+2.Sg' in only_roots:
            only_roots[0:2]= only_roots[0:2][::-1]
        elif '▁PrnPers+1.Sg' in only_roots:
            only_roots[0:2]= only_roots[0:2][::-1]
        sentence.extend(only_roots)


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