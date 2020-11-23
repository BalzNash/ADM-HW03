from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
import time


def get_one_page_urls(driver, url_prefix):
    temp_urls_list = []
    page_source = BeautifulSoup(driver.page_source, features='lxml')
    urls_tag = page_source.find_all('a', class_='bookTitle')
    for tag in urls_tag:
        temp_urls_list.append(url_prefix + tag.get('href'))
    return temp_urls_list


def get_all_pages_urls(target_page, pages_num, url_prefix, page_prefix):
    urls_list = []
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    for i in range(pages_num):
        driver.get(target_page)
        urls_list.extend(get_one_page_urls(driver,url_prefix))
        target_page = page_prefix + str(i+2)
    return urls_list


def store_in_txt(urls, file_name):
    with open(file_name, "w") as f:
        f.write("\n".join(urls))

        
if __name__ == "__main__":
    target_page = 'https://www.goodreads.com/list/show/1.Best_Books_Ever'
    url_prefix = 'https://www.goodreads.com'
    page_prefix = 'https://www.goodreads.com/list/show/1.Best_Books_Ever?page='
    
    urls = get_all_pages_urls(target_page, 300, url_prefix, page_prefix)
    store_in_txt(urls,'books_urls.txt')
