import nltk
from nltk.corpus import stopwords
from nltk.sem.logic import AllExpression
#nltk.download('popular')
#nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import os
import pickle


def get_plot_from_tsv(file_name):
    """Opens a .tsv file and returns only the plot of the book

    Args:
        file_name (str): file name

    Returns:
        [str]: plot of the book
    """
    with open(file_name, 'r', encoding = 'utf-8') as f:
        all_fields = f.readlines()[2].split('\t')
        plot = all_fields[6]
    return plot


def to_lowercase(text):
    return text.lower()


def tokenize_text(text):
    """Tokenize a text and removes punctuation

    Args:
        text (str): a text

    Returns:
        [list]: a list with tokens as elements
    """
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    return tokenizer.tokenize(text)


def remove_stopwords(tokenized_text):
    return [word for word in tokenized_text if not word in stopwords.words()]


def lemmatize_text(tokenized_text):
    """takes a tokenized text, applies the lemmatization and returns the processed text

    Args:
        tokenized_text (list): a tokenized text

    Returns:
        [list]: lemmatized text
    """
    lemmatizer = WordNetLemmatizer()
    
    def get_wordnet_pos(word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    return [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in tokenized_text]


def preprocess_text(seed):
    """applies consecutive functions on the input and returns the result

    Args:
        seed (list): a text

    Returns:
        [list]: the pre-processed text
    """
    for func in [to_lowercase, tokenize_text, remove_stopwords, lemmatize_text]:
        seed = func(seed)
    return seed


def update_vocabulary(text, vocabulary):
    """Takes a pre-processed text and for each token updates a dictionary that maps from words to integers (encoding)
    
    Args:
        text (list): pre-processed text
        vocabulary (dict): a dictionary that maps from words to integers

    Returns:
        [dict]: the updated vocabulary
    """
    for word in text:
        if word not in vocabulary:
            if not vocabulary:
                idx = 1
            else:
                idx = max(vocabulary.values()) + 1
            vocabulary[word] = idx
    return vocabulary


def save_vocabulary(vocabulary):
    """Stores the vocabulary in a .pickle file for future use

    Args:
        vocabulary (dict): mapping from word to integers
    """
    with open('vocabulary.pickle', 'wb') as g:
        pickle.dump(vocabulary, g)


def encode_plot(preprocessed_plot, vocabulary, idx, cwd):
    """Encodes the pre-processed plot in integer, based on the vocabulary mapping,
       stores the result in a pickle file for future use.

    Args:
        preprocessed_plot (list): pre-processed plot
        vocabulary (dict): mapping from word to integers
        idx (int): number of the .tsv we are considering
        cwd (str): current working directory
    """
    encoded_plots_folder = '\\encoded_files\\'
    dict_repr = {}
    
    # encoding based on vocabulary
    for token in preprocessed_plot:
        dict_repr[vocabulary[token]] = dict_repr.get(vocabulary[token], 0) + 1
    
    # store in pickle
    with open(cwd+encoded_plots_folder+str(idx)+".pickle", "wb") as h:
        pickle.dump(dict_repr, h)


if __name__ == "__main__":

    tsv_folder = '\\tsvs\\'
    cwd = os.getcwd()
    vocabulary = {}
    
    # sorts the files in numerical order (to avoid reading in this order 1 -> 10 -> 100)
    file_list = os.listdir(cwd+tsv_folder)
    file_list = sorted(file_list, key=lambda x:int(os.path.splitext(x)[0][8:]))
    
    for file_name in file_list:
        plot = get_plot_from_tsv(cwd+tsv_folder+file_name)
        preprocessed_plot = preprocess_text(plot)
        vocabulary = update_vocabulary(preprocessed_plot, vocabulary)
        encode_plot(preprocessed_plot, vocabulary, int(file_name[8:-4]), cwd)
    
    save_vocabulary(vocabulary)


