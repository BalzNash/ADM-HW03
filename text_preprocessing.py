import nltk
from nltk.corpus import stopwords
from nltk.sem.logic import AllExpression
#nltk.download('popular')
#nltk.download('stopwords')
from nltk.tokenize import word_tokenize
import os


def get_plot_from_tsv(file_name):
    with open(file_name, 'r', encoding = 'utf-8') as f:
        all_fields = f.readlines()[2].split('\t')
        plot = all_fields[6]
    return plot

cwd = os.getcwd()
plot = get_plot_from_tsv(cwd+'\\tsvs\\article_1.tsv')
lower_case_plot = plot.lower()
tokenizer = nltk.RegexpTokenizer(r"\w+")
tokens = tokenizer.tokenize(lower_case_plot)
tokens_without_sw = [word for word in tokens if not word in stopwords.words()]
print(tokens_without_sw)




#STEPS:
#1. Remove duplicate whitespace
#2. Remove punctuation and special characters (maybe do it before #1)
#3. Capital letter removal
#4. Remove stopwords
#5. Stemming


