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

def regular_verb_stemmer(word):
    # Define the suffixes you want to remove
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
    
    # Create a pattern that matches any of the suffixes
    pattern = r'(' + '|'.join(suffixes) + r')$'
    
    # Use re.sub() to replace the suffix with =
    return re.sub(pattern, '=', word)

def noun_stemmer(word):
    # Define the suffixes you want to remove
    suffixes = ['be','de', 'ci','i',
                'ngga','ngge','nggo',
                'sa','se','so']
    
    # Create a pattern that matches any of the suffixes
    pattern = r'(' + '|'.join(suffixes) + r')$'
    
    # Use re.sub() to replace the suffix with =
    return re.sub(pattern, '~', word)

def split_verb_in_text(text):
    tokens = text.split()
    new_list = []
    for token in tokens:
        #from_imperative = token + 'mbi'
        token = token.strip()
        from_conjugated_regular = regular_verb_stemmer(token).replace('=','mbi')
        if token in pos_default_dict.keys(): # if the token is in 新满汉dict
            if token in verblist_all: # if the token is -mbi verb
                new_list.append(token.replace('mbi','=mbi'))
            else:
                new_list.append(token)
        elif token in irregular_wordlist.keys(): # if the token is a irregular form
            if '=' in irregular_wordlist[token]: # if it is a irregular verb
                new_list.append(irregular_wordlist[token])
            else:
                new_list.append(token)
        elif from_conjugated_regular in verblist_all: # when the token is not in 新满汉dict, and is a (regular) verb  
            stem = regular_verb_stemmer(token).replace('=','')
            new_list.append(token.replace(stem,f'{stem}='))
        else:
            new_list.append(token)
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
                from_inflected = noun_stemmer(token).replace('~','')
                # the the reconstructed dict form is in dict
                if from_inflected in pos_default_dict.keys():
                    if '方' in pos_default_dict[from_inflected] or '名' in pos_default_dict[from_inflected]: # if it is a noun or 方位词, then split
                        stem = noun_stemmer(token).replace('~','')
                        new_list.append(token.replace(stem,f'{stem}~'))
                    else:
                        new_list.append(token)
                # if the root is not in dict, but root+n is in dict. limited to a few suffices
                elif from_inflected + 'n' in pos_default_dict.keys() and token.endswith(('ci','ngga','ngge','nggo','sa','se','so')): 
                    if '方' in pos_default_dict[from_inflected +'n'] or '名' in pos_default_dict[from_inflected +'n'] or '数' in pos_default_dict[from_inflected]:
                        stem = noun_stemmer(token).replace('~','')
                        new_list.append(token.replace(stem,f'{stem}n~'))# nikasa -> nikan~sa, fujurungga -> fujurun~ngga
                    else:
                        new_list.append(token)
                else:
                    new_list.append(token)
        else:
            new_list.append(token)
    return ' '.join(new_list)

def noun_verb_splitter(text):
    return split_noun_in_text(split_verb_in_text(text))
