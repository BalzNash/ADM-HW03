import pickle
import os
from text_preprocessing import preprocess_text


def create_inverted_idx(cwd, encoded_files_folder):
    inverted_idx = {}
    #for file_name in os.listdir(cwd+encoded_files_folder):
    file_list = os.listdir(cwd+encoded_files_folder)
    file_list = sorted(file_list, key=lambda x:int(os.path.splitext(x)[0]))
    for file_name in file_list:
        with open(cwd+encoded_files_folder + file_name,'rb') as f:
            dict_repr = pickle.load(f)
            for key in dict_repr:
                inverted_idx.setdefault(key, []).append(int(file_name[:-7]))
    with open('inverted_idx.pickle', "wb") as g:
        pickle.dump(inverted_idx, g)


def encode_query(query, vocabulary):
    encoded = []
    for token in query:
        if token in vocabulary:
            encoded.append(vocabulary[token])
        else:
            return False
    return encoded



def search_engine(encoded_query, inverted_idx):
    result = []
    if not encoded_query:
        return result
    else:
        selected_lists = [inverted_idx[token] for token in encoded_query]
        idx = [0] * len(selected_lists)
        lists_len = [len(my_list) for my_list in selected_lists]
        selected_lists2 = list(enumerate(selected_lists))
        while all([k < m for k, m in zip(idx, lists_len)]):
            max_num = max([docs[idx[list_num]] for list_num, docs in selected_lists2])
            if all([docs[idx[list_num]] == max_num for list_num, docs in selected_lists2]):
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
        return result


if __name__ == "__main__":
    
    cwd = os.getcwd()
    encoded_files_folder = "\\encoded_files\\"
    
    create_inverted_idx(cwd, encoded_files_folder)
    
    with open('inverted_idx.pickle', 'rb') as h:
        inverted_idx = pickle.load(h)

    with open('vocabulary.pickle', 'rb') as q:
        vocabulary = pickle.load(q)

    query = input('enter your query:\n')
    preprocessed_query = preprocess_text(query)
    encoded_query = encode_query(preprocessed_query, vocabulary)
    print(search_engine(encoded_query, inverted_idx))

