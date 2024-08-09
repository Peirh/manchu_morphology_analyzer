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

def verb_stemmer(word):
    # Define the suffixes you want to remove
    suffixes = ['mbi','me', 'ci','ki','kini','mbihe','mbime','mbifi','cibe','cina',
                'fi', 'pi','mpi',
                'nggala','nggele','nggolo',
                'tai','tei','toi',
                'tala','tele','tolo',
                'ra','re','ro','ndara','ndere',
                'rakv','rekv',
                'rangge','rengge','rongge','ndarangge','nderengge',
                'ha','he','ho','ka','ke','ko','ngka','ngke','ngko',
                'hai','hei','hoi',
                'hakv','hekv',
                'hangge','hengge','hongge','kangge','kengge','kongge','ngkangge','ngkengge','ngkongge',
                'habi','hebi','hobi','kabi','kebi','kobi',
                'habihe','hebihe','hobihe','kabihe','kebihe','kobihe',
                'habici','hebici','hobici','kabici','kebici','kobici']
    
    # Create a pattern that matches any of the suffixes
    pattern = r'(' + '|'.join(suffixes) + r')$'
    
    # Use re.sub() to replace the suffix with =
    return re.sub(pattern, '=', word)

def noun_stemmer(word):
    # Define the suffixes you want to remove
    suffixes = ['be','de', 'ci','i',
                'ngga','ngge','nggo']
    
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
        from_conjugated = verb_stemmer(token).replace('=','mbi')
        if token in verblist_all:
            new_list.append(token.replace('mbi','=mbi'))
        elif token in pos_default_dict.keys():
        #if token in pos_dict.keys() and '及' not in ' '.join(pos_default_dict[token]): # if the token is in the dictionary, and is not a verb, dont split
            new_list.append(token)
        elif from_conjugated in verblist_all:
        #elif '及' in ' '.join(pos_default_dict[from_conjugated]): # if the reconstructed dictionary form is in the dictionary and is a verb, split the verb
            # or '及' in ' '.join(pos_default_dict[from_imperative])
            stem = verb_stemmer(token).replace('=','')
            new_list.append(token.replace(stem,f'{stem}='))
        else:
            new_list.append(token)
    return ' '.join(new_list)

def split_noun_in_text(text):
    tokens = text.split()
    new_list = []
    for token in tokens:
        token = token.strip()
        from_inflected = noun_stemmer(token).replace('~','')
        if from_inflected in pos_default_dict.keys() and token not in pos_default_dict.keys():
            if '方' in pos_default_dict[from_inflected] or '名' in pos_default_dict[from_inflected]: # if the token is in the dictionary, and is a noun or 方位词, then split
                stem = noun_stemmer(token).replace('~','')
                new_list.append(token.replace(stem,f'{stem}~'))
            else:
                new_list.append(token)
        else:
            new_list.append(token)
    return ' '.join(new_list)

def noun_verb_splitter(text):
    return split_noun_in_text(split_verb_in_text(text))
