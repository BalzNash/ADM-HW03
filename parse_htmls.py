from bs4 import BeautifulSoup
from bs4 import NavigableString


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i,j)
    return text


def get_bookTitle(page_source):
    bookTitle = page_source.find_all('h1', id='bookTitle')[0]
    return bookTitle.text.strip()


def get_bookSeries(page_source):
    #returns and empty string when there's no bookseries
    replace_dict = {'(': "", ')': ""}
    book_series = page_source.find_all('h2', id='bookSeries')[0]
    return replace_all(book_series.text.strip(), replace_dict)


def get_bookAuthors(page_source):
    #Timea
    return "tbd"


def get_ratingValue(page_source):
    #Timea
    return "tbd"


def get_ratingCount(page_source):
    ratingCount = page_source.find('meta',{'itemprop':'ratingCount'})['content']
    return int(ratingCount)


def get_reviewCount(page_source):
    reviewCount = page_source.find('meta',{'itemprop':'reviewCount'})['content']
    return int(reviewCount)


def get_plot(page_source):
    description_box = page_source.select("div[id=descriptionContainer]")[0]
    plot_and_comment = description_box.find_all('span')[-1]
    plot = ''
    for i in plot_and_comment:
        if isinstance(i, NavigableString):
            plot +=' '+i
    return plot.strip()


def get_numberOfPages(page_source):
    numberOfPages = int(page_source.find('span',{'itemprop':'numberOfPages'}).contents[0].split()[0])
    return numberOfPages


def get_publishingDate(page_source):
    publishingDate = page_source.find('div',{'class':'row'}).find_next_sibling()
    if publishingDate.find_all('nobr') != []:
        publishingDate = publishingDate.find('nobr').text
        replace_dict = {'\n': "", '(': "", ')': ""}
        return replace_all(publishingDate, replace_dict).strip().split()[2:]
    else:
        return publishingDate.contents[0].split()[1:4]


def get_characters(page_source):
    bookDataBox = page_source.select("div[class=buttons] > div[id=bookDataBox]")[0]
    characters = bookDataBox.find_all("a", href=lambda value: value.startswith("/characters"))
    characters = [i.text for i in characters]
    return characters if characters != [] else False


def get_setting(page_source):
    if page_source.select("div[class=buttons] > div[id=bookDataBox] > div[class=infoBoxRowTitle]") == []:
        return False
    else:
        setting_box = page_source.select("div[class=buttons] > div[id=bookDataBox] > div[class=infoBoxRowItem]")[0]
        setting = setting_box.find_all("a", href=lambda value: value.startswith("/places"))
        setting = [i.text for i in setting]
        return setting


def get_url(page_source):
    url = page_source.find_all('link', rel='canonical')[0]['href']
    return url


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


def open_and_read_html(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        parsed_page = BeautifulSoup(f, features= 'lxml')
        return parsed_page


def get_field_values(page_source, field_function_map):
    """Takes a parsed html file and a mapping between fields to be retrieved and corresponding functions, returns a list with the content of the fields 

    Args:
        page_source (bs4 object): html file parsed with Beautiful Soup
        field_function_map (dict): mapping between fields to be retrieved and functions to retrieve them

    Returns:
        list: list of retrieved fields
    """
    field_values = []
    for item in field_function_map:
        field_values.append(field_function_map[item](page_source)) #call function for each field
    return field_values
    #if field_values[6] == False:
    #    pass
        #do nothing
    #else:
         #write .tsv file
    #return field_values


if __name__ == "__main__":

     for i in range(1):
         page_source = open_and_read_html('./htmls//article_'+str(i+1)+'.html')
         field_values = get_field_values(page_source, field_function_map)
         for i in field_values:
             print(i)

    

 