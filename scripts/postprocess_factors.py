#processing xfst output
#outputs morphological segmented Quechua words with tags for suffixes, one sentence per line
#factors

import re
import json
import sentencepiece as spm

infile = open ('', 'r', encoding = 'utf8') # path to original file to be changed
outfile = open('', 'w', encoding = 'utf8') # path to new file
vocab_json = open('train.trg.json') # path to json vocab file from target side
vocab = json.load(vocab_json)

sentence = []
prev_line_empty = True
line = infile.readline()
prev_token = ''

sp = spm.SentencePieceProcessor(model_file='spm.joint.model') # from Nematus model file

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

        k=0
        for morph in morphs:
            morph = re.sub(r'\[', r' \[', morph)
            morph = re.sub(r'\\', '', morph)
            token, *analysis = morph.split()
            token = re.sub(r'\@(.*)', '', token)
            
            analysed = ' '.join(analysis)
            analysed = re.sub(r'\+', '|+', analysed)
            analysed = re.sub(r'\[=(\w+(,)?)*\]', '', analysed)
            analysed = re.sub(r'\[\-\-]', '', analysed)
            analysed = re.sub(r'\[', '', analysed)
            analysed = re.sub(r'\]', '', analysed)
            analysed = re.sub(r'\^\w+', '', analysed)
            analysed = re.sub(r'PrnPers\+\d\.\w+', 'PrnPers', analysed)
            analysed = re.sub(r'NPers\+\d\.\w+', 'NPers', analysed)
            analysed = re.sub(r' ', '', analysed)
            analysed = re.sub(r'CARD', 'Root|Special', analysed)
            analysed = re.sub(r'NP$', 'Root|Special', analysed)
            analysed = re.sub(r'NRoot', 'Root|NRoot', analysed)
            analysed = re.sub(r'VRoot', 'Root|VRoot', analysed)
            analysed = re.sub(r'PrnDem', 'Root|PrnDem', analysed)
            analysed = re.sub(r'Part_Contr', 'Root|Part_Contr', analysed)
            analysed = re.sub(r'PrnInterr', 'Root|PrnInterr', analysed)
            analysed = re.sub(r'Part_Neg', 'Root|Part_Neg', analysed)
            analysed = re.sub(r'Part_Affir', 'Root|Part_Affir', analysed)
            analysed = re.sub(r'Part_Sim', 'Root|Part_Sim', analysed)
            analysed = re.sub(r'Part_Cond', 'Root|Part_Cond', analysed)
            analysed = re.sub(r'ALFS', 'Root|ALFS', analysed)
            analysed = re.sub(r'Part_Disc', 'Root|Part_Disc', analysed)
            analysed = re.sub(r'PrepES', 'Root|PrepES', analysed)
            analysed = re.sub(r'Part_Conec', 'Root|Part_Conec', analysed)
            analysed = re.sub(r'ConjES', 'Root|ConjES', analysed)
            analysed = re.sub(r'AdvES', 'Root|AdvES', analysed)
            analysed = re.sub(r'VRootVPers\|\+2.Sg.Subj.Imp', 'HAKU', analysed) #haku
            analysed = re.sub(r'VRootVPers\|\+2.Pl.Subj.Imp', 'HAKU', analysed) #hakuchik
            analysed = re.sub(r'\$\.', 'Root|Special', analysed)
            analysed = re.sub(r'PrnPers\|\+Lim\|\+3.Sg', 'PrnPers|+Lim+3.Sg', analysed)
            analysed = re.sub(r'NPers\|\+3.Sg.Poss\|\+Lim', 'NPers|+3.Sg.Poss+Lim', analysed)
            analysed = re.sub(r'NPers\|\+1.Sg.Poss\|\+Lim', 'NPers|+1.Sg.Poss+Lim', analysed)
            analysed = re.sub(r'NPers\|\+1.Pl.Excl.Poss\|\+Lim', 'NPers|+1.Pl.Excl.Poss+Lim', analysed)
            analysed = re.sub(r'PrnPers\|\+Lim\|\+1.Pl.Incl', 'PrnPers|+Lim+1.Pl.Incl', analysed)
            analysed = re.sub(r'NPers\|\+3.Pl.Poss\|\+Lim', 'NPers|+3.Pl.Poss+Lim', analysed)
            analysed = re.sub(r'PrnPers\|\+Lim\|\+1.Pl.Excl', 'PrnPers|+Lim+1.Pl.Excl', analysed)
            analysed = re.sub(r'NPers\|\+1.Pl.Incl.Poss\|\+Lim', 'NPers|+1.Pl.Incl.Poss+Lim', analysed)
            analysed = re.sub(r'NPers\|\+2.Sg.Poss\|\+Lim', 'NPers|+2.Sg.Poss+Lim', analysed)

            #if the root is spanish, split additionally with spanish sentencepiece model
            if 'NRootES' in analysed:
                token = sp.encode(token, out_type=str)
                for i in token:
                    i = i+'|' +str(analysed)
                    only_tokens.append(i)
            elif 'VRootES' in analysed:
                token = sp.encode(token, out_type=str)
                for i in token:
                    i = i+'|' +str(analysed)
                    only_tokens.append(i)
            elif 'NRootG' in analysed:
                token = sp.encode(token, out_type=str)
                for i in token:
                    i = i+'|' +str(analysed)
                    only_tokens.append(i)
            elif 'VRootG' in analysed:
                token = sp.encode(token, out_type=str)
                for i in token:
                    i = i+'|' +str(analysed)
                    only_tokens.append(i)
            elif '[NP]' in analysis:
                token = sp.encode(token, out_type=str)
                for i in token:
                    i = i+'|' +str(analysed)
                    only_tokens.append(i)
            elif '[CARD]' in analysis:
                token = sp.encode(token, out_type=str)
                for i in token:
                    i = i+'|' +str(analysed)
                    only_tokens.append(i)

            #dev and test
            # elif token not in vocab.keys():
            #     token = sp.encode(token, out_type=str)
            #     for i in token:
            #         i = i+'|' +str(analysed)
            #         only_tokens.append(i)


            else:
                
                token = token + '|' + str(analysed)
                only_tokens.append(token)

            tags = []
            if analysed != '':
                    tags.append(analysed)
            tags = [s for s in tags if s!='Root|VRootES']
            tags = [s for s in tags if s!='Root|NRootES']
            tags = [s for s in tags if s!='Root|Special']
            tags = [s for s in tags if s!='Root|VRootG']
            tags = [s for s in tags if s!='Root|NRootG']
            tags = [s for s in tags if s!='Root|Part_Neg']
            tags = [s for s in tags if s!='Root|NRoot']
            tags = [s for s in tags if s!='Root|VRoot']
            tags = [s for s in tags if s!='Cas|+Acc']
            tags = [s for s in tags if s!='Cas|+Loc']

            tags= [s for s in tags if re.search(r'Amb.*', s)]
            
            only_tokens.extend(tags)
 
        sentence.extend(only_tokens)

        
        #remove duplicate tags: tag|tag not attached to token
        sentence = [s for s in sentence if not re.search(r'((^\w+[|]\+\w+)|(\|\|Root\|NONE)|(\▁\+\?\|))', s)]

    elif len(cols) == 3: # process words with no morphological analysis
        # split word in subwords using spanish sentencepiece model
        word = cols[0]
        words = sp.encode(word, out_type=str)
        for word in words:
            sentence.append(word + '|Root|NONE')

    prev_line_empty == False
    line = infile.readline()

infile.close()
outfile.close()