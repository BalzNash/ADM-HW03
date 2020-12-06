from bs4 import BeautifulSoup
from langdetect import detect
import os
import csv
import re


#--------------------------------- HELPER FUNCTIONS ---------------------------------


def replace_all(text, dic):
    '''

    Args:
        text: A string to be cleaned from unneccessary characters
        dic: A dictionary containing all the characters that have to be replaced as keys and the strings that have to replace
        the unwanted characters as values

    Returns: A cleaned string from all the unwanted characters

    '''    
    for i, j in dic.items():
        text = text.replace(i,j)
    return text


def create_file_name(directory, idx_start):
    '''

    Args:
        directory: Local directory
        idx_start: Variable used for indexing

    Returns: The path of the tsv file

    '''
    return directory+'article_'+str(idx_start)+'.tsv'


#--------------------------------- PARSING FUNCTIONS --------------------------------


def get_bookTitle(page_source):
    '''

    Args:
        page_source: The link of the html book

    Returns: The title of the book

    '''
    bookTitle = page_source.find_all('h1', id='bookTitle')[0]
    return bookTitle.text.strip()


def get_bookSeries(page_source):
    '''

    Args:
        page_source: The link of the html book

    Returns: The book series if there is one, else an empty string

    '''    
    replace_dict = {'(': "", ')': "", '\t': "", '\n': ""}
    book_series = page_source.find_all('h2', id='bookSeries')[0]
    return replace_all(book_series.text.strip(), replace_dict)


def get_bookAuthors(page_source):
    '''

    Args:
        page_source: The link of the html book

    Returns: The authors of the book

    '''    
    listOfAuthors = [element.text for element in page_source.find_all('span', {'itemprop': 'name'})]
    return ", ".join(listOfAuthors)

def get_ratingValue(page_source):
    '''

    Args:
        page_source: The link of the html book

    Returns: The rating value of the book

    '''    
    return page_source.find('span',{'itemprop':'ratingValue'}).text.strip()


def get_ratingCount(page_source):
    '''

    Args:
        page_source: The link of the html book

    Returns: The rating count of the book

    '''    
    return page_source.find('meta',{'itemprop':'ratingCount'})['content']


def get_reviewCount(page_source):
    '''

    Args:
        page_source: The link of the html book

    Returns: The number of the reviews of the book

    '''
    return page_source.find('meta',{'itemprop':'reviewCount'})['content']


def get_plot(page_source):
    '''

    Args:
        page_source: The link of the html book

    Returns: The plot of the book if it exists, else an empty string; If the plot is in English the function
    return the string "notEnglish"

    '''

    # Selecting the main tag containing the plot
    description_box = page_source.select("div[id=descriptionContainer]")[0]

    # The plot doesn't exist
    if description_box.find_all("span", id=re.compile(".")) == []:
        return ""

    # The plot exists
    else:

        plot = str(description_box.find_all("span", id=re.compile("."))[-1])

        # Cleaning the plot from all the tags
        cleanr = re.compile('<.*?>')
        plot = re.sub(cleanr, '', plot)

        try:
            # Checking if book is not in English
            if detect(plot) != 'en':
                return "notEnglish"

            # Cleaning the plot from unneccessary characters and spaces
            plot = plot.strip()

            if plot.startswith("."):
                plot = plot[1:]

            return plot

        # Handling exceptions that are given by books not in English because land.detect doesn't detect all languages
        except:
            try:
                if page_source.find('div', {'itemprop': "inLanguage"}).text != "English":
                    return "notEnglish"
                else:
                    return ""
            except:
                return ""



def get_numberOfPages(page_source):
    '''

    Args:
        page_source: The link of the html book

    Returns: The number of the pages of the book if it exists, else an empty string

    '''
    numberOfPages = page_source.find('span',{'itemprop':'numberOfPages'})
    if numberOfPages is not None:
        return numberOfPages.contents[0].split()[0]
    else:
        return ""


def get_publishingDate(page_source):
    '''

    Args:
        page_source: The link of the html book

    Returns: The first publishing date of the book if it exists, else an empty string

    '''
    try:    
        publishingDate = page_source.find('div', {'class': 'row'}).find_next_sibling()
        replace_dict = {'\n': "", '(': "", ')': "", '\t': ""}

        if publishingDate.find_all('nobr') != []:
            publishingDate = publishingDate.find('nobr').text
            return " ".join(replace_all(publishingDate, replace_dict).strip().split()[2:])
        else:
            return " ".join(replace_all(publishingDate.contents[0], replace_dict).split()[1:4])
    except:
        return ""


def get_characters(page_source):
    '''

    Args:
        page_source: The link of the html book

    Returns: The characters of the book if they exist, else an empty string

    '''
    bookDataBox = page_source.select("div[class=buttons] > div[id=bookDataBox]")[0]
    characters = bookDataBox.find_all("a", href=lambda value: value.startswith("/characters"))
    characters = [i.text for i in characters]
    return ", ".join(characters) if characters != [] else ""


def get_setting(page_source):
    '''

    Args:
        page_source: The link of the html book

    Returns: The setting of the book if it exists, else an empty string

    '''
    if page_source.select("div[class=buttons] > div[id=bookDataBox] > div[class=infoBoxRowTitle]") == []:
        return ""
    else:
        setting_box = page_source.select("div[class=buttons] > div[id=bookDataBox] > div[class=infoBoxRowItem]")[0]
        setting = setting_box.find_all("a", href=lambda value: value.startswith("/places"))
        setting = [i.text for i in setting]
        return " ".join(setting)


def get_url(page_source):
    '''

    Args:
        page_source: The link of the html book

    Returns: The url of the book

    '''
    url = page_source.find_all('link', rel='canonical')[0]['href']
    return url


# A dictionary that has all the fields to be parsed as keys, and the corresponding parsing functions as values
field_function_map = {'bookTitle': get_bookTitle,
                      'bookSeries': get_bookSeries,
                      'bookAuthors': get_bookAuthors,
                      'ratingValue': get_ratingValue,
                      'ratingCount': get_ratingCount,
                      'reviewCount': get_reviewCount,
                      'plot': get_plot,
                      'numberOfPages': get_numberOfPages,
                      'publishingDate': get_publishingDate,
                      'characters': get_characters,
                      'setting': get_setting,
                      'url': get_url}


# ------------------------------------ MAIN FUNCTIONS ------------------------------------


def open_and_read_html(file_name):
    """takes the name of a html file as input, reads the file, parses the content with Beautiful soup and returns the page_source as a bs4 object

    Args:
        file_name (list): the name of a html file

    Returns:
        [bs4.object] the page_source in Beautiful Soup format
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        page_source = BeautifulSoup(f, features= 'lxml')
        return page_source


def get_field_values(page_source, field_function_map):
    """Takes a parsed html file and a mapping between fields to be retrieved and corresponding functions, returns a list with the content of the fields 

    Args:
        page_source (bs4 object): html file parsed with Beautiful Soup
        field_function_map (dict): mapping between fields to be retrieved and functions to retrieve them

    Returns:
        list: list of retrieved fields
    """
    replace_dict = {'\n': "", '\t': ""}
    field_values = []
    for item in field_function_map:
        field_value = replace_all(field_function_map[item](page_source), replace_dict)
        field_values.append(field_value)
    return field_values


def write_tsv_files(field_values, idx, dic):
    """Takes a list of the parsed values for each field, the index of the current page and a dictionary with the field names as keys.
       Writes a new .tsv file in the \\tsv directory containing the name of the fields as headers and the corresponding values below.

    Args:
        field_values (list): list of the parsed values for each field
        idx (int): index of current page (e.g file1 -> idx = 1)
        dic (dict): mapping from field names to parsing function (here we're interested only in its keys)
    
    Returns:
        None, it only writes on the new file
    """
    directory = os.getcwd()+'\\tsvs\\'
    if field_values[6] == 'NotEnglish':
        pass
    else:
        with open(create_file_name(directory, idx), 'w', encoding = 'utf-8') as g:
            headers = dic.keys()
            tsv_writer = csv.writer(g, delimiter='\t')
            tsv_writer.writerow(headers)
            tsv_writer.writerow(field_values)

#-------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    
    for i in range(30000):
        page_source = open_and_read_html('./htmls//article_'+str(i+1)+'.html')
        field_values = get_field_values(page_source, field_function_map)
        write_tsv_files(field_values, i+1, field_function_map)
        print(i+1)