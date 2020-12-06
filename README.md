# Homework 3 - Which book would you recomend?

_Authors:_
* _Manuel Balzan,_
* _Mohammad Iman Sayyadzadeh and_
* _Adrienn Timea Aszalos_

_for "La Sapienza" University of Rome, Master in Data Science, class 2020-2021_

<br>
<br>

The goal of the homework is to build a search engine over the "best books ever" list of GoodReads. Each book is downloaded as an html file and then parsed in order to retrieve important informations of the books, like the title, the authors, the publishing date and so on. There are a total of 30 000 html files downloaded and only the 27 174 English books are kept. 

<br>

Other tasks: 
* The search engines give the user the opportunity to do queries and perform metrics over the plots of the remaining 27 174 books.
* The homework also contains a 2d plot of the first ten book series in order of appearance and an algorithmic question using dynamic programming.

<br>

For utter information please check the file **main.ipynb**.

<br>

In the following lines you can find the **content of the repository**:
* _encoded_files_: (**TO BE COMPLETED**)
* _tsvs_: contains all the tsv files for the 27174 English books 
* _get_urls.py_: using this code we get the URLs of the books from Goodreads website and store them in books_urls.txt.
* _books_urls.txt_: In this file, we collected the URLs of all the books in the first 300 pages of the "best books ever" list.
* _download_htmls.py_: Using this code we downloaded the HTML files of the books.
* _inverted_idx.pickle_: This file is a dictionary that specifies for each word the document that the word is present.
* _inverted_idx2.pickle_: This file is similar to inverted_idx, but it also contains the the relative tfIdf score for each document.
* _main.ipynb_: is the main file containing the outputs of the exercises
* _parse_htmls.py_: stores all the parsing functions perfomed for the html web scraping 
* _plot_book_series.py_: contains the functions that generate the plot of the first ten book series in order of appearance (ex. 4)
* _search_engines.py_: contains the three search engines (**TO BE COMPLETED**)
* _squared_tfidf_per_document.pickle_: (**TO BE COMPLETED**)
* _text_preprocessing.py_: contains the pre-processing functions used to tokanize the plot for each book
* _vocabulary.pickle_: stores the codifications of the words contained in every book plot

