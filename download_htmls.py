from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
import os


def create_file_name(idx, directory):
    return directory+'article_'+str(idx)+'.html'


def get_and_store_html(line, driver, idx, directory):
    """Opens a book webpage, gets the source code and stores it in an html file

    Args:
        line (str): URL of a single book
        driver (selenium.webdriver): Firefox webriver
        idx (int): book number
        directory (str): directory where we want to store the html
    """
    url = line.strip()
    driver.get(url)
    book_source = driver.page_source
    with open(create_file_name(idx, directory), 'w', encoding="utf-8") as g:
        g.write(book_source)


def run_html_downloader(driver, start, end, directory):
    """Opens the .txt containing all the books' URLs,
       iterates over each of them and applies the 'get_and_store_html function to store their source code

    Args:
        driver (selenium.webdriver): Firefox webriver
        start (int): first book number to consider
        end (int): last book number to consider
        directory (str): directory where we want to store the html
    """
    with open('books_urls.txt', 'r') as f:
        idx = start
        lines = f.readlines()[start-1:end]
        for line in lines:
            get_and_store_html(line, driver, idx, directory)
            idx += 1


if __name__ == "__main__":
    
    directory = os.getcwd()+'\htmls\\'
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    run_html_downloader(driver, 1, 30000, directory)





