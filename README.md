# Homework 3 - Which book would you recomend?

The goal of the homework is to build a search engine over the "best books ever" list of GoodReads. Each book is downloaded as an html file and then parsed in order to retrieve important informations of the books, like the title, the authors, the publishing date and so on. There are a total of 30 000 html files downloaded and only the 27 174 English books are kept. 

Other tasks: 
* The search engines give the user the opportunity to do queries and perform metrics over the plots of the remaining 27 174 books.
* The homework also contains a 2d plot of the first ten book series in order of appearance and an algorithmic question using dynamic programming.

For utter information please check the file **main.ipynb**.

In the folowwing lines you can find the content of the repository:
* get_urls.py: using this code we get the URLs of the books from Goodreads website and store them in books_urls.txt.
* books_urls.txt: In this file, we collected the URLs of all the books in the first 300 pages of the "best books ever" list.
* download_htmls.py: Using this code we downloaded the HTML files of the books.
* inverted_idx.pickle: This file is a dictionary that specifies for each word the document that the word is present.
* inverted_idx2.pickle: This file is similar to inverted_idx, but it also contains the the relative tfIdf score for each document.
* main.ipynb: is the main file containing the outputs of the exercises
* parse_htmls.py: stores all the parsing functions perfomed for the html web scraping 
* plot_book_series.py: contains the functions that generate the plot of the first ten book series in order of appearance (ex. 4)
* search_engines.py: contains the three search engines
* squared_tfidf_per_document.pickle: 
* text_preprocessing.py:
* vocabulary.pickle:
