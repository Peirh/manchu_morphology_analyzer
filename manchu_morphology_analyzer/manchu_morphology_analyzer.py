import re
import os
from collections import defaultdict

# read in the mbi_list
# Determine the path relative to this script's directory
# relative to the script’s directory, not the current working directory.
script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, 'data', 'mbi_list.txt'),'r',encoding='utf8') as file:
    verblist_all = [v.strip() for v in file]

# read in the 新满汉_POStag
pos_default_dict = defaultdict(str)
with open(os.path.join(script_dir,'data', '新满汉_POStag.txt'),'r',encoding='utf8') as file:
    for line in file:
        w,pos = line.strip().split('\t')
        pos_default_dict[w] = pos

## irregular nouns and verbs
irregular_wordlist = dict()
with open(os.path.join(script_dir,'data', '新满汉_irregular_verbs_and_nouns.txt'),'r',encoding='utf8') as file:
    for line in file:
        form, split = line.strip().split('\t')
        irregular_wordlist[form] = split

## get a manchu to mongol dict from 五体清文鉴
mnc2mgl_all_dict = defaultdict(set)
with open(r'C:\Users\haral\Desktop\my_own_projects\my_ipynb\scraping\dynamic\栗林均\dict五体清文鉴\五体清文鉴(满汉蒙).txt','r',encoding='utf8') as file:
    lines = file.readlines()
# generated from all entries of 五体清文鉴
for line in lines:
    id, mnc, nikan, mgl= line.split('\t')
    mgl = mgl.replace('\n','')
    mnc = re.sub('\[.*\]', '', mnc)
    mnc = re.sub('mbi$', '=', mnc)
    mnc = mnc.replace('š','x').replace('ū','v')
    mgl = re.sub('\[.*\]', '', mgl)
    mgl = mgl.replace('=mui','=').replace('=müi','=').replace('=ü','').replace('=u','').replace('_','').replace('D','d')
    mgl = mgl.replace('\'','').replace('?','')
    if ',' in mgl:
        mgl_splits = mgl.split(',')
        for mgl_split in mgl_splits:
            mnc2mgl_all_dict[mnc].add(mgl_split.strip())
    else:
        mnc2mgl_all_dict[mnc].add(mgl)

def regular_verb_split_inflection(word):
    # suffixes for regular verbs that we want to remove
    suffixes = ['mbi','me', 'ci','ki','kini','mbihe','mbime','mbifi','cibe','cina',
                'fi', 
                'nggala','nggele','nggolo',
                'tai','tei','toi',
                'tala','tele','tolo',
                'ra','re','ro',
                'rakv','rekv',
                'rangge','rengge','rongge',
                'ha','he','ho',
                'hai','hei','hoi',
                'hakv','hekv',
                'hangge','hengge','hongge',
                'habi','hebi','hobi',
                'habihe','hebihe','hobihe',
                'habici','hebici','hobici']
    
    pattern = r'(' + '|'.join(suffixes) + r')$'# Create a pattern that matches any of the suffixes
    new_word = re.sub(pattern, r'=\1', word) # \1 refers to the matched suffix

    return new_word

def noun_split(word):
    # Define the suffixes you want to remove
    suffixes = ['be','de', 'ci','i',
                'ngga','ngge','nggo',
                'sa','se','so']
    
    # Create a pattern that matches any of the suffixes
    pattern = r'(' + '|'.join(suffixes) + r')$'
    
    new_word = re.sub(pattern, r'~\1', word) # \1 refers to the matched suffix
    return new_word

# a function for splitting derivational suffixes
def split_derivation_in_verbal_stem(word):
    derivational_stem = re.sub('=.*$','',word)
    #print(derivational_stem)
    new_word = word
    # causative/passive
    if derivational_stem.endswith(('mbu', 'bu')):
        for mgl in mnc2mgl_all_dict[derivational_stem+'=']:
            if mgl.endswith(('ge=','γa=','ke=','qa=','γul=','gül=','γda=','gde=')):
                new_word = re.sub('(bu=|mbu=|bu$|mbu$)', r'+\1', word) # \1 refers to the matched suffix
    # cooperative, reciprocal
    elif derivational_stem.endswith(('nu', 'ndu')):
        for mgl in mnc2mgl_all_dict[derivational_stem+'=']:
            if mgl.endswith(('ldü=','ldu=','lca=','lce=')):
                new_word = re.sub('(nu=|ndu=|nu$|ndu$)', r'+\1', word) # \1 refers to the matched suffix
    # to come to..
    elif derivational_stem.endswith('nji'):
        for mgl in mnc2mgl_all_dict[derivational_stem+'=']:
            if mgl.endswith('ire='):
                new_word = re.sub('(nji=|nji$)', r'+\1', word) # \1 refers to the matched suffix
    # to go to..
    elif derivational_stem.endswith(('na','ne','no')):
        for mgl in mnc2mgl_all_dict[derivational_stem+'=']:
            if mgl.endswith('od='):
                new_word = re.sub('(na=|ne=|no=|na$|ne$|no$)', r'+\1', word) # \1 refers to the matched suffix
    return new_word

def split_verb_in_text(text, split_derivational=False):
    tokens = text.split()
    new_list = []
    for token in tokens:
        #from_imperative = token + 'mbi'
        token = token.strip()
        from_conjugated_regular = re.sub('=.+$','mbi',regular_verb_split_inflection(token))
        # if the token is already in 新满汉dict, keep the token
        if token in pos_default_dict.keys(): 
            if token in verblist_all: # if the token is -mbi verb
                new_list.append(re.sub('mbi$','=mbi',token))
            else:
                new_list.append(token)
        # if the token is a irregular form, split the token according to irregular verb list
        elif token in irregular_wordlist.keys(): 
            if '=' in irregular_wordlist[token]: # if it is a irregular verb
                new_list.append(irregular_wordlist[token])
            else:
                new_list.append(token)
        # when the token is not in 新满汉dict, and is a (regular) verb, replace the stem with 'stem='
        elif from_conjugated_regular in verblist_all:
            splitted = regular_verb_split_inflection(token)
            new_list.append(splitted)
        else:
            new_list.append(token)
    
    # optional: can also split the derivational suffixes
    if split_derivational == True:
        new_list_derivaition = [split_derivation_in_verbal_stem(token) for token in new_list]
        return ' '.join(new_list_derivaition)
    else:
        return ' '.join(new_list)

def split_noun_in_text(text):
    tokens = text.split()
    new_list = []
    for token in tokens:
        token = token.strip()
        # if the token is not directly in dict
        if token not in pos_default_dict.keys():
            # if the token is irregular, then just split according to irregular list
            if token in irregular_wordlist.keys() and '~' in irregular_wordlist[token]:# if it is a irregular noun (with ~)
                new_list.append(irregular_wordlist[token])
            else:
                # get the dict form
                from_inflected = re.sub('~.+$','',noun_split(token))
                # the the reconstructed dict form is in dict
                if from_inflected in pos_default_dict.keys():
                    if '方' in pos_default_dict[from_inflected] or '名' in pos_default_dict[from_inflected]: # if it is a noun or 方位词, then split
                        new_list.append(noun_split(token))
                    else:
                        new_list.append(token)
                # if the root is not in dict, but root+n is in dict. limited to a few suffices
                elif from_inflected + 'n' in pos_default_dict.keys() and token.endswith(('ci','ngga','ngge','nggo','sa','se','so')): 
                    if '方' in pos_default_dict[from_inflected +'n'] or '名' in pos_default_dict[from_inflected +'n'] or '数' in pos_default_dict[from_inflected]:
                        new_list.append(noun_split(token).replace('~','n~'))# nika~sa -> nikan~sa, fujuru~ngga -> fujurun~ngga
                    else:
                        new_list.append(token)
                else:
                    new_list.append(token)
        else:
            new_list.append(token)
    return ' '.join(new_list)

def noun_verb_splitter(text,split_derivational):
    return split_noun_in_text(split_verb_in_text(text,split_derivational))
