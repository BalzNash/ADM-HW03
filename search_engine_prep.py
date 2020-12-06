import pickle
import os
from text_preprocessing import preprocess_text
import math
import heapq


#--------------------------------------------------------STORING_DATA_FUNCTIONS------------------------------------------------------------------


def create_inverted_idx(cwd, encoded_files_folder) -> None: 
    """Creates and stores a dictionary which maps from encoded words to all the documents containing that word.
       Stores the output in a .pickle file and returns None.

    Args:
        cwd (str): Current working directory
        encoded_files_folder (str): subfolder where the encoded plots are stored
    """
    inverted_idx = {}

    # sorts the files in numerical order (to avoid reading in this order 1 -> 10 -> 100)
    file_list = os.listdir(cwd+encoded_files_folder)
    file_list = sorted(file_list, key=lambda x:int(os.path.splitext(x)[0]))
    
    # iterates over each word in each document. Inserts key-value pairs in the inverted_idx, where the key is a word (encoded) and the value is a list of all documents containing the word  
    for file_name in file_list:
        with open(cwd+encoded_files_folder + file_name,'rb') as f:
            dict_repr = pickle.load(f)
            for key in dict_repr:
                inverted_idx.setdefault(key, []).append(int(file_name[:-7]))
    
    with open('inverted_idx.pickle', "wb") as g:
        pickle.dump(inverted_idx, g)


def create_inverted_idx_2(cwd, encoded_files_folder) -> None:
    """Creates and stores a dictionary which maps from encoded words to all the documents containing that word + the corresponding tfidf score.
       Stores the output in a .pickle file and returns None.

    Args:
        cwd (str): Current working directory
        encoded_files_folder (str): subfolder where the encoded plots are stored
    """
    inverted_idx2 = {}

    #sorts the files in numerical order (to avoid reading in this order 1 -> 10 -> 100)
    file_list = os.listdir(cwd+encoded_files_folder)
    file_list = sorted(file_list, key=lambda x:int(os.path.splitext(x)[0]))
    
    # iterates over each word in each document. Inserts key-value pairs in the inverted_idx2, where the key is a word (encoded) and the value is a list of tuples of this format (doc_name, term frequency) 
    docs_count = 0
    for file_name in file_list:
        docs_count += 1
        with open(cwd+encoded_files_folder + file_name,'rb') as f:
            dict_repr = pickle.load(f)
            for key in dict_repr:
                inverted_idx2.setdefault(key, []).append((int(file_name[:-7]), dict_repr[key]))
    
    # iterates over each word in the dict and substitutes the term frequency with the term frequency multiplied by the inverse document frequency
    for key in inverted_idx2:
        for idx, value in enumerate(inverted_idx2[key]):
            inverted_idx2[key][idx] = (value[0], value[1] * math.log(docs_count / len(inverted_idx2[key])))
    
    with open('inverted_idx2.pickle', "wb") as g:
        pickle.dump(inverted_idx2, g)


def store_squared_tfidf_per_document(inverted_idx2) -> None:
    """Computes the sum of the squared tfidf scores of a document ( |d| in the cosine similarity formula ),
       stores a dictionary with the documents as keys, and the squared sum as values. 

    Args:
        inverted_idx2 (dict): the inverted index with tfidf scores
    """
    squared_tfidfs = {}
    
    # iterates over each value and each key of the inverted_idx2, updates the squared_tfidfs per document
    for term in inverted_idx2:
        for doc, tfidf in inverted_idx2[term]:
            squared_tfidfs.setdefault(doc, []).append(tfidf**2)
    
    #sums the squared tfidfs
    for doc in squared_tfidfs:
        squared_tfidfs[doc] = sum(squared_tfidfs[doc])
    
    with open('squared_tfidf_per_document.pickle', "wb") as g:
        pickle.dump(squared_tfidfs,g)


#------------------------------------------------------------HELPER FUNCTIONS----------------------------------------------------------


def encode_query(query, vocabulary):
    """Takes a textual query and a vocabulary (mapping from words to integers), returns the encoded query in a list.
       If a word is not in the dictionary, the function returns False.

    Args:
        query (list): A textual query
        vocabulary (dict): Mapping from all words

    Returns:
        [list or bool]: the encoded query in a list or False
    """
    encoded = []
    for token in query:
        if token in vocabulary:
            encoded.append(vocabulary[token])
        else:
            return False
    return encoded


def get_top_k(dic):
    """[summary] TODO add description

    Args:
        dic ([type]): [description]

    Returns:
        [type]: [description]
    """
    heap = [(-value, key) for key,value in dic.items()]
    largest = heapq.nsmallest(3, heap)
    return [(key, -value) for value, key in largest]


def compute_cosine_similarity(encoded_query, docs_scores, squared_tfidf_per_document) -> dict:
    """Compares a textual query with some documents (which contain all the words in the query)
       and computes for each pair their cosine similarity.
       We assume that each term of the query has always a score of 1

    Args:
        encoded_query (list): a textual query, encoded in integers
        docs_scores (dict): a dict with documents as keys, and the sum of their tfidf scores for ONLY the words in the query as values
        squared_tfidf_per_document (dict): a dict with documents as keys, and the sum of their squared tfidf scores for ALL their words

    Returns:
        [dict]: a dict with documents as keys, and their cosine similarity with respect to the query as values
    """
    similarity_scores = {}
    
    for doc in docs_scores:
        cos_similarity = docs_scores[doc] / ((math.sqrt(squared_tfidf_per_document[doc]))*(math.sqrt(len(encoded_query)))) 
        similarity_scores[doc] = cos_similarity
    
    return similarity_scores


#------------------------------------------------------------PRINT FUNCTIONS-----------------------------------------------------------


def print_search_engine_result(result):
    """Prints the first search engine results,
       Fetching the data from tsv files.

    Args:
        result (list): a list of all the documents selected by the search engine
    """
    for book in result:
        with open(os.getcwd()+'\\tsvs\\'+'article_'+str(book)+'.tsv', 'r', encoding = 'utf-8') as f:
            all_fields = f.readlines()[2].split('\t')
            print("")
            print('--BOOKTITLE--')
            print(all_fields[0] + '\n')
            print('--PLOT--')
            print(all_fields[6] + '\n')
            print('--URL--')
            print(all_fields[-1] + '\n')
            print('----------------------------------------------------------------------------------------------' + '\n')
    

def print_search_engine_2_result(result):
    """Prints the second search engine results,
       Fetching the data from tsv files.

    Args:
        result (dict): a dict of all the documents selected by the search engine and their similarity score
    """    
    for book, score in result:
        with open(os.getcwd()+'\\tsvs\\'+'article_'+str(book)+'.tsv', 'r', encoding = 'utf-8') as f:
            all_fields = f.readlines()[2].split('\t')
            print("")
            print('--BOOKTITLE--')
            print(all_fields[0] + '\n')
            print('--PLOT--')
            print(all_fields[6] + '\n')
            print('--URL--')
            print(all_fields[-1] + '\n')
            print('--SIMILARITY--')
            print(round(score,2), '\n')
            print('----------------------------------------------------------------------------------------------' + '\n')


#------------------------------------------------------------SEARCH ENGINES---------------------------------------------------------------


def search_engine(encoded_query, inverted_idx):
    """[summary]

    Args:
        encoded_query ([type]): [description]
        inverted_idx ([type]): [description]

    Returns:
        [type]: [description]
    """
    result = []

    if not encoded_query:
        return result
    else:  
        # selects only the list corresponding to the words that appear in the query
        selected_lists = [inverted_idx[token] for token in encoded_query]

        idx = [0] * len(selected_lists) # start at index 0 for each list
        lists_len = [len(my_list) for my_list in selected_lists]
        selected_lists2 = list(enumerate(selected_lists))

        # checks if any list index surpasses the last element
        while all([k < m for k, m in zip(idx, lists_len)]):
            max_num = max([docs[idx[list_num]] for list_num, docs in selected_lists2]) # get the max document number
            
            # handles the case when each list is pointing at the same value
            if all([docs[idx[list_num]] == max_num for list_num, docs in selected_lists2]):
                result.append(max_num)
                idx = [i+1 for i in idx]
            
            # handles all the other cases, increasing idx on all lists that are not pointing at the max value
            else:
                j = 0
                for my_list in selected_lists:
                    if my_list[idx[j]] == max_num:
                        pass
                    else:
                        idx[j] += 1
                    j += 1
        
        return result


def search_engine_2(encoded_query, inverted_idx2, squared_tfidf_per_document):
    """[summary]

    Args:
        encoded_query ([type]): [description]
        inverted_idx2 ([type]): [description]
        squared_tfidf_per_document ([type]): [description]

    Returns:
        [type]: [description]
    """
    result = []
    docs_scores = {}
    
    if not encoded_query:
        return result
    else:
        # selects only the list corresponding to the words that appear in the query 
        selected_lists = [inverted_idx2[token] for token in encoded_query]
        
        idx = [0] * len(selected_lists) # start at index 0 for each list
        lists_len = [len(my_list) for my_list in selected_lists]
        selected_lists2 = list(enumerate(selected_lists)) # enumerate each of our lists
        
        # checks if any list idx surpasses the last element
        while all([k < m for k, m in zip(idx, lists_len)]):
            max_num = max([docs[idx[list_num]][0] for list_num, docs in selected_lists2])  # get the max document number between the selected ones
            
            # handles the case when each list is pointing at the same value -> add the document and its score to the result
            if all([docs[idx[list_num]][0] == max_num for list_num, docs in selected_lists2]):
                docs_scores[max_num] = sum([docs[idx[list_num]][1] for list_num, docs in selected_lists2])
                idx = [i+1 for i in idx]
            
            # handles all the other cases, increasing idx on all lists that are not pointing at the max value
            else:
                j = 0
                for my_list in selected_lists:
                    if my_list[idx[j]][0] == max_num:
                        pass
                    else:
                        idx[j] += 1
                    j += 1
        
        # computes the cosine similarity for each of the selected docs
        all_scores = compute_cosine_similarity(encoded_query, docs_scores, squared_tfidf_per_document)
        
        # returns the top k documents ordered by cos similarity (using heaps)
        return get_top_k(all_scores)


def search_engine_3(encoded_query, inverted_idx2, squared_tfidf_per_document, uncoded_query):
    """Uses search engine 2 to get only the documents with a plot containing the query,
       then prompts the user to specify new info, related to the other book fields (e.g. bookTitle, setting, etc.),
       adjusts the score based on the new info #TODO complete description

    Args:
        encoded_query (list): a textual query, encoded in integer
        inverted_idx2 (dict): the inverted index with tfidf scores
        squared_tfidf_per_document (dict): |d| of the cosine similarity formula (before sqrt) 
        uncoded_query (list): the same textual query, not encoded in integers

    Returns:
        [dic]: the top k documents ranked by the new adjusted score
        #TODO add top k function, improve score
    """
    
    # apply the second search engine (plot only)
    plot_result = search_engine_2(encoded_query, inverted_idx2, squared_tfidf_per_document)
    
    # define scores for each field of the book
    scores = {
        0: 1,   #BookTitle
        1: 1,   #BookSeries
        2: 1,   #BookAuthors
        3: 1,   #RatingValue
        4: 1,   #RatingCount
        5: 1,   #ReviewCount
        6: 0,   #Plot
        7: 1,   #NumberOfPages
        8: 1,   #PublishingDate
        9: 1,   #Characters
        10: 1,  #Setting
        11: 0   #URL
    }
    final_score = {}

    # Iterates over each book, and adjust the score for each of them based on the other fields
    for doc, score in plot_result:
        total_score = score
        with open('.\\tsvs\\article_'+str(doc)+'.tsv', 'r', encoding = 'utf-8') as f:
            all_fields = f.readlines()[2].split('\t')
            all_fields = [preprocess_text(field) for field in all_fields] # preprocess each field without encoding
            i = 0
            for field in all_fields:
                for token in uncoded_query:
                    if token in field:
                        total_score += scores[i]
                        break
                i += 1
        final_score[doc] = total_score
    
    return final_score


#--------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    
    cwd = os.getcwd()
    encoded_files_folder = "\\encoded_files\\"
    
    #create_inverted_idx(cwd, encoded_files_folder)
    #create_inverted_idx_2(cwd, encoded_files_folder)

    with open('inverted_idx.pickle', 'rb') as h:
        inverted_idx = pickle.load(h)
    
    with open('inverted_idx2.pickle', 'rb') as h:
        inverted_idx2 = pickle.load(h)
    
    with open('vocabulary.pickle', 'rb') as q:
        vocabulary = pickle.load(q)

    #store_squared_tfidf_per_document(inverted_idx2)
    
    with open('squared_tfidf_per_document.pickle', "rb") as q:
        squared_tfidf_per_document = pickle.load(q)


    # for query ('could', 'one') the preprocessing function returns only 'could' (remove stopwords probably) so the search engine incorrectly uses only 'could'
    query = input('enter your query:\n')
    preprocessed_query = preprocess_text(query)
    encoded_query = encode_query(preprocessed_query, vocabulary)
    p = search_engine(encoded_query, inverted_idx)
    y = search_engine_2(encoded_query, inverted_idx2, squared_tfidf_per_document)
    print_search_engine_result(p)
    print(y)
    print_search_engine_2_result(y)
    #print(search_engine_3(encoded_query, inverted_idx2, squared_tfidf_per_document, preprocessed_query))
    
