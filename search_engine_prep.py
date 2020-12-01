import pickle
import os
from text_preprocessing import preprocess_text
import math


def create_inverted_idx(cwd, encoded_files_folder):
    inverted_idx = {}
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


def create_inverted_idx_2(cwd, encoded_files_folder):
    inverted_idx2 = {}
    file_list = os.listdir(cwd+encoded_files_folder)
    file_list = sorted(file_list, key=lambda x:int(os.path.splitext(x)[0]))
    docs_count = 0
    for file_name in file_list:
        docs_count += 1
        with open(cwd+encoded_files_folder + file_name,'rb') as f:
            dict_repr = pickle.load(f)
            for key in dict_repr:
                inverted_idx2.setdefault(key, []).append((int(file_name[:-7]), dict_repr[key]))
    for key in inverted_idx2:
        for idx, value in enumerate(inverted_idx2[key]):
            inverted_idx2[key][idx] = (value[0], value[1] * math.log(docs_count / len(inverted_idx2[key])))
    with open('inverted_idx2.pickle', "wb") as g:
        pickle.dump(inverted_idx2, g)
    pass


def store_tfidf_per_document(inverted_idx2):
    docs = {}
    for term in inverted_idx2:
        for doc, tfidf in inverted_idx2[term]:
            docs.setdefault(doc, []).append(tfidf)
    for doc in docs:
        docs[doc] = sum(docs[doc])
    with open('tfidf_per_document.pickle', "wb") as g:
        pickle.dump(docs,g)


def search_engine_3(encoded_query, inverted_idx2):
    result = []
    docs_scores = {}
    if not encoded_query:
        return result
    else:
        selected_lists = [inverted_idx2[token] for token in encoded_query]
        idx = [0] * len(selected_lists)
        lists_len = [len(my_list) for my_list in selected_lists]
        selected_lists2 = list(enumerate(selected_lists))
        while all([k < m for k, m in zip(idx, lists_len)]):
            max_num = max([docs[idx[list_num]][0] for list_num, docs in selected_lists2])
            if all([docs[idx[list_num]][0] == max_num for list_num, docs in selected_lists2]):
                docs_scores[max_num] = sum([docs[idx[list_num]][1] for list_num, docs in selected_lists2])
                idx = [i+1 for i in idx]
            else:
                j = 0
                for my_list in selected_lists:
                    if my_list[idx[j]][0] == max_num:
                        pass
                    else:
                        idx[j] += 1
                    j += 1
        return docs_scores


if __name__ == "__main__":
    
    cwd = os.getcwd()
    encoded_files_folder = "\\encoded_files\\"
    
    create_inverted_idx(cwd, encoded_files_folder)
    create_inverted_idx_2(cwd, encoded_files_folder)

    with open('inverted_idx.pickle', 'rb') as h:
        inverted_idx = pickle.load(h)
    print(len(inverted_idx))
    with open('inverted_idx2.pickle', 'rb') as h:
        inverted_idx2 = pickle.load(h)
    print(len(inverted_idx2))
    with open('vocabulary.pickle', 'rb') as q:
        vocabulary = pickle.load(q)

    query = input('enter your query:\n')
    preprocessed_query = preprocess_text(query)
    print(preprocessed_query) # for query ('could', 'one') the preprocessing function returns only 'could' (remove stopwords probably) so the search engine incorrectly uses only 'could'
    encoded_query = encode_query(preprocessed_query, vocabulary)
    print(search_engine(encoded_query, inverted_idx))
    print(search_engine_3(encoded_query, inverted_idx2))
    #print(store_tfidf_per_document(inverted_idx2))

