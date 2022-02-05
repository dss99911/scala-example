import pandas as pd
from collections import Counter
from collections import defaultdict

df1 = pd.read_csv("program/data/indonesian_dict/dict1.txt")
df2 = pd.read_csv("program/data/indonesian_dict/dict2.txt")
word_list = pd.concat([df1, df2])
word_list['word'] = word_list['word'].str.lower()
word_list = word_list['word'].str.extract(r'(^[a-z]*)').iloc[:, 0].tolist()


def make_character_count_dict(w):
    try:
        return frozenset(dict(Counter(w).items()).items())
    except:
        return None


def make_count_word_dict():
    dict_count_word = defaultdict(list)
    for w in word_list:
        c = make_character_count_dict(w)
        if c is None:
            continue

        dict_count_word[c].append(w)
    return dict_count_word

def find_word(chars: str, length, dict_count_word):
    if len(chars) - length == 0:
        counter = make_character_count_dict(chars)
        return set(dict_count_word[counter])

    result = set()
    for i in range(len(chars)):
        result.update(find_word(chars[:i] + chars[i + 1:], length, dict_count_word))
    return result

def find_word_list(chars: str, length, dict_count_word):
    result = list(find_word(chars, length, dict_count_word))
    result.sort()
    return result

dict_count_word = make_count_word_dict()

#%%

result = find_word_list("miakna", 6, dict_count_word)
