from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager


def get_one_page_urls(driver, url_prefix):
    """Takes a webdriver and an url_prefix as input,
       parses a webpage and returns a list of the urls of the books in that page

    Args:
        driver (selenium.webdriver): a webdriver pointing at a specific webpage
        url_prefix (str): prefix of the target books webpages

    Returns:
        [list]: list of all books' URLs in the current page
    """
    temp_urls_list = []
    
    # gets all books in the page
    page_source = BeautifulSoup(driver.page_source, features='lxml')
    urls_tag = page_source.find_all('a', class_='bookTitle')
    
    # iterates over each book and stores their URL
    for tag in urls_tag:
        temp_urls_list.append(url_prefix + tag.get('href'))
    return temp_urls_list


def get_all_pages_urls(target_page, pages_num, url_prefix, page_prefix):
    """Iterates over n webpages and stores the URL of all the contained books.

    Args:
        target_page (str): URL of the starting page
        pages_num ([type]): number of pages to be considered
        url_prefix (str): prefix of all books' URLs
        page_prefix (str): prefix of all pages after the starting page

    Returns:
        [list]: list of all books' URLs in the n (pages_num) pages
    """
    urls_list = []
    
    # initiates a Firefox webdriver, iterates over n (pages_num) pages and stores the URLs
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    for i in range(pages_num):
        driver.get(target_page)
        urls_list.extend(get_one_page_urls(driver,url_prefix))
        target_page = page_prefix + str(i+2)
    return urls_list


def store_in_txt(urls, file_name):
    """Stores the URLs in a .txt file

    Args:
        urls (list): list of all books' URLs
        file_name (str): name of the new .txt file
    """
    with open(file_name, "w") as f:
        f.write("\n".join(urls))

        
if __name__ == "__main__":
    
    target_page = 'https://www.goodreads.com/list/show/1.Best_Books_Ever'
    url_prefix = 'https://www.goodreads.com'
    page_prefix = 'https://www.goodreads.com/list/show/1.Best_Books_Ever?page='
    
    urls = get_all_pages_urls(target_page, 300, url_prefix, page_prefix)
    store_in_txt(urls,'books_urls.txt')