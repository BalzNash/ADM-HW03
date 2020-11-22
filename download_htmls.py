from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
import os




def create_file_name(idx, directory):
    return directory+'article_'+str(idx)+'.html'

def get_and_store_html(line, driver, idx, directory):
    url = line.strip()
    driver.get(url)
    book_source = driver.page_source
    with open(create_file_name(idx, directory), 'w', encoding="utf-8") as g:
        g.write(book_source)


def run_html_downloader(driver, start, end, directory):
    with open('books_urls.txt', 'r') as f:
        idx = 0
        for line in f.readlines():
            idx+=1
            if idx < start:
                print('skip')
                continue
            if idx > end:
                print('done')
                break
            else:
                get_and_store_html(line, driver, idx, directory)


if __name__ == "__main__":
    directory = os.getcwd()+'\htmls\\'
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    run_html_downloader(driver, 5, 10, directory)








