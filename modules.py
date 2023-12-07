import pandas as pd
import re
import code

alphabet_rus = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'j',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'x',
    'ц': 's',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sh',
    'ъ': "'",
    'ы': 'i',
    'ь': "'",
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
    'ў': "o'",
    'ғ': "g'",
    'қ': 'q',
    'ҳ': 'h',
    'А': 'a',
    'Б': 'b',
    'В': 'v',
    'Г': 'g',
    'Д': 'd',
    'Е': 'e',
    'Ё': 'yo',
    'Ж': 'j',
    'З': 'z',
    'И': 'i',
    'Й': 'y',
    'К': 'k',
    'Л': 'l',
    'М': 'm',
    'Н': 'n',
    'О': 'o',
    'П': 'p',
    'Р': 'r',
    'С': 's',
    'Т': 't',
    'У': 'u',
    'Ф': 'f',
    'Х': 'x',
    'Ц': 's',
    'Ч': 'ch',
    'Ш': 'sh',
    'Щ': 'sh',
    'Ъ': "'",
    'Ы': 'i',
    'Ь': "'",
    'Э': 'e',
    'Ю': 'yu',
    'Я': 'ya',
    'Ў': "o'",
    'Ғ': "g'",
    'Қ': 'q',
    'Ҳ': 'h',
}




pattern_id = r'23\d{6}(?!\d)'
pattern_lastname = r"\b[A-Z][a-zA-Z]\w+(?:ov|yev|va|ev|VA|OV|YEV|EV)\b"


def unidecode(word):
    return (''.join(alphabet_rus[char] if char in alphabet_rus else char for char in word)).upper()


def find_studentid(data):
    talab_raqam = re.search(pattern_id, data)
    if talab_raqam:
        return 'ID' + talab_raqam.group()
    return ''

def fish_setter(data):
    data = unidecode(str(data))
    data = re.sub(r'[^a-zA-Z ]', '', data)
    searched = data.split()[3:]
    counter_lastname = 0
    for item in searched:
        if re.search(pattern_lastname, item):
            break
        counter_lastname += 1
    counter_middlename = 0
    for item in searched:
        item = item.lower()
        try:
            if item.endswith('vich') or item.endswith('vna') or item.endswith('vichning') or item.endswith('vnaning'):
                last_name = searched[counter_lastname]
                first_name = searched[counter_lastname+1]
                middle_name = searched[counter_middlename]
                return f"{last_name} {first_name} {middle_name}"
            elif  item.endswith('ugli') or item.endswith('uglini') or item.endswith('oglini') or item.endswith('ogli') or item.endswith('o\'gli') or item.endswith('qizi') or item.endswith('kizi') or item.endswith('kzi') or item.endswith('uglining') or item.endswith('oglining') or item.endswith('o\'glining') or item.endswith('qizining') or item.endswith('kizining') or item.endswith('kzining') or item.endswith('uglini') or item.endswith('oglu'):
                last_name = searched[counter_middlename - 3]
                first_name = searched[counter_middlename - 2]
                middle_name_1 = searched[counter_middlename - 1]
                middle_name_2 = searched[counter_middlename]
                return f"{last_name} {first_name} {middle_name_1} {middle_name_2}"
        except Exception as err:
            # print(err, searched, counter_lastname, counter_middlename)
            pass
        counter_middlename += 1

def levenshtein_distance_tester(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance_tester(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def find_similar_words_tester(target_word, word_list, threshold):
    similar_words = []
    for word in word_list:
        distance = levenshtein_distance_tester(target_word, word)
        if distance <= threshold:
            similar_words.append(word)
    return similar_words

# def fish_searcher():
#     if row['Student ID'] == '':
#         if row['FISH'] == None:
#             continue
#         similar_words = find_similar_words(row['FISH'], setter['FISH'])
#         if len(similar_words) == 1:
#             setter_row = setter[setter['FISH'].str.contains(similar_words[0])]
#             print(setter_row)
#             setter.loc[setter_row.index, "To'langan summa"] = setter_row["To'langan summa"].astype('int') + int(row['Summa'])
#             counter_fish_set+=1
#             # continue
#         elif len(similar_words) == 0:
#             print(row['FISH'], 'topilmadi')
#         else: 
#             similar_words2 = find_similar_words_tester(row['FISH'], similar_words, len(similar_words))
#             if len(similar_words2)==0:
#                 pass
#                 # print('\n#############', similar_words, row['FISH'], similar_words2, '#############\n')
                
def find_similar_words(word_to_search, word_list, threshold=80):
    """
    Find words similar to the given word in a list using fuzzy matching.

    Parameters:
    - word_to_search: The word to find similar words for.
    - word_list: The list of words to search within.
    - threshold: The fuzzy matching threshold (default is 80).

    Returns:
    - A list of similar words.
    """
    similar_words = []
    for word in word_list:
        word = re.sub(r'[^a-zA-Z ]', '', word)
        similarity_score = fuzz.ratio(word_to_search, word)
        if similarity_score >= threshold:
            similar_words.append(word)
    return sorted(similar_words, reverse=True)