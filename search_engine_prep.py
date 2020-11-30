import pickle
import os
from text_preprocessing import preprocess_text


cwd = os.getcwd()
encoded_files_folder = "\\encoded_files\\"
file = open("vocabulary.pickle",'rb')
dictionary = pickle.load(file)
file.close()

inverted_idx = {}
for file_name in os.listdir(cwd+encoded_files_folder):
    with open(cwd+encoded_files_folder + file_name,'rb') as f:
        dict_repr = pickle.load(f)
        for key in dict_repr:
            inverted_idx.setdefault(key, []).append(int(file_name[:-7]))


query = input('enter your query')

preprocessed_query = preprocess_text(query)

encoded_query = [dictionary[token] for token in preprocessed_query if token in dictionary]

result = []
if encoded_query:
        selected_lists = [inverted_idx[token] for token in encoded_query]
        idx = [0] * len(selected_lists)
        lists_len = [len(my_list) for my_list in selected_lists]
        selected_lists = list(enumerate(selected_lists))
        while all([k < m for k, m in zip(idx, lists_len)]):
            max_num = max([docs[idx[list_num]] for list_num, docs in selected_lists])
            if all([docs[idx[list_num]] == max_num for list_num, docs in selected_lists]):
                result.append(max_num)
                idx = [i+1 for i in idx]
            else:
                j = 0
                for my_list in selected_lists:
                    if my_list[idx[j]] == max_num:
                        pass
                    else:
                        idx[j] += 1
                    j += 1
else:
    pass

print(result)

