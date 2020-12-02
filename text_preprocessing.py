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
    with open(file_name, 'r', encoding = 'utf-8') as f:
        all_fields = f.readlines()[2].split('\t')
        plot = all_fields[6]
    return plot


def to_lowercase(text):
    return text.lower()


def tokenize_text(text):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    return tokenizer.tokenize(text)


def remove_stopwords(tokenized_text):
    return [word for word in tokenized_text if not word in stopwords.words()]


def lemmatize_text(tokenized_text):
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
    for func in [to_lowercase, tokenize_text, remove_stopwords, lemmatize_text]:
        seed = func(seed)
    return seed


def update_vocabulary(text, vocabulary):
    for word in text:
        if word not in vocabulary:
            if not vocabulary:
                idx = 1
            else:
                idx = max(vocabulary.values()) + 1
            vocabulary[word] = idx
    return vocabulary


def save_vocabulary(vocabulary):
    with open('vocabulary.pickle', 'wb') as g:
        pickle.dump(vocabulary, g)


def encode_plot(preprocessed_plot, vocabulary, idx, cwd):
    encoded_plots_folder = '\\encoded_files\\'
    dict_repr = {}
    for token in preprocessed_plot:
        dict_repr[vocabulary[token]] = dict_repr.get(vocabulary[token], 0) + 1
    with open(cwd+encoded_plots_folder+str(idx)+".pickle", "wb") as h:
        pickle.dump(dict_repr, h)


if __name__ == "__main__":

    tsv_folder = '\\tsvs\\'
    cwd = os.getcwd()
    vocabulary = {}
    idx = 1
    
    file_list = os.listdir(cwd+tsv_folder)
    file_list = sorted(file_list, key=lambda x:int(os.path.splitext(x)[0][8:]))
    for file_name in file_list[:1000]:
        plot = get_plot_from_tsv(cwd+tsv_folder+file_name)
        preprocessed_plot = preprocess_text(plot)
        vocabulary = update_vocabulary(preprocessed_plot, vocabulary)
        encode_plot(preprocessed_plot, vocabulary, idx, cwd) #idx needs to be replaced with tsv file number
        print(idx)
        idx += 1 # to be removed
    save_vocabulary(vocabulary)


    
    # with open(cwd+'\\tsvs\\'+'article_31.tsv', 'r', encoding = 'utf-8') as h:
    #     all_fields = h.readlines()[2].split('\t')
    #     plot = all_fields[6]
    #     print(plot)
    #     preprocessed_plot = preprocess_text('ones')
    #     print(preprocessed_plot)
        # dict_repr = {}
        # for token in preprocessed_plot:
        #     dict_repr[vocabulary[token]] = dict_repr.get(vocabulary[token], 0) + 1
        # print(dict_repr)







#STEPS:
#1. Remove duplicate whitespace
#2. Remove punctuation and special characters (maybe do it before #1)
#3. Capital letter removal
#4. Remove stopwords
#5. Stemming


