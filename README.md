# Homework 3 - Which book would you recommend?

![alt text](https://github.com/BalzNash/ADM-HW03/blob/main/goodreads_logo.png "BookReads logo")

<br>

_Authors:_
* _Manuel Balzan_
* _Mohammad Iman Sayyadzadeh_
* _Adrienn Timea Aszalos_

_for "Algorithmic Methods of Data Mining", "La Sapienza" University of Rome, MSc in Data Science, 2020-2021._


<br>

The goal of the homework is to build a search engine over the ["best books ever"](https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1) list of GoodReads. Each book is downloaded as an .html file and then parsed in order to retrieve important informations of the books, like the title, the authors, the publishing date and so on. There are a total of 30 000 .html files downloaded and only the 27 174 English books are kept. 

<br>

Other tasks: 
* The search engines give the user the opportunity to do queries and perform metrics over the plots of the remaining 27 174 books.
* The homework also contains a 2d plot of the first ten book series in order of appearance as well as the answer to an algorithmic question using dynamic programming.

<br>

For utter information please check the file **[_main.ipynb_](../main/main.ipynb)**.

<br>

In the following lines you can find the **content of the repository**:

**JUPYTER NOTEBOOKS:**
* [_main.ipynb_](../main/main.ipynb): is the main file containing the outputs of the exercises


**FOLDERS:**
* [_encoded_files_](../main/encoded_files): contains all the pickle files that store the vectorized representation of the 27 174 English plots. 
* [_tsvs_](../main/tsvs) : contains all the tsv files for the 27 174 English books.

**.PY FILES:**
* [_get_urls.py_](../main/get_urls.py): Using this code we retrieved the URLs of the books from Goodreads website and stored them in [_books_urls.txt_](../main/books_urls.txt)
* [_download_htmls.py_](../main/download_htmls.py): Using this code we downloaded the HTMLs of all the books
* [_parse_htmls.py_](../main/parse_htmls.py): stores all the parsing functions perfomed for the html web scraping
* [_text_preprocessing.py_](../main/text_preprocessing.py): contains the pre-processing functions used to tokenize the plot for each book
* [_search_engines.py_](../main/search_engines.py): contains the three search engines
* [_plot_book_series.py_](../main/plot_book_series.py): contains the functions that generate the plot of the first ten book series in order of appearance (ex. 4)

**PICKLE DATA:**
* [_squared_tfidf_per_document.pickle_](../main/squared_tfidf_per_document.pickle): a dictionary that maps from each document to their |d| in the cos similarity formula 
* [_vocabulary.pickle_](../main/vocabulary.pickle): stores the codifications of the words contained in every book plot
* [_inverted_idx.pickle_](../main/inverted_idx.pickle): This file is a dictionary that for each word, specify the documents that contain that word.
* [_inverted_idx2.pickle_](../main/inverted_idx2.pickle): This file is similar to inverted_idx.pickle, but it also contains the corresponding tfIdf score for each document.


**OTHERS:**
* [_books_urls.txt_](../main/books_urls.txt): In this file, we collected the URLs of all the books in the first 300 pages of the "best books ever" list.
* [_goodreads_logo.png_](../main/goodreads_logo.png): The logo of ["GoodReads"](https://www.goodreads.com)


