from bs4 import BeautifulSoup
import codecs


def get_bookTitle(page_source):
    bookTitle = page_source.find_all('h1', id='bookTitle')[0].contents
    bookTitle = "".join(bookTitle).strip()
    return bookTitle

def get_bookSeries():
    pass

def get_bookAuthors():
    pass

def get_ratingValue():
    pass

def get_ratingCount():
    pass

def get_reviewCount():
    pass

def get_plot():
    #check language
    pass

def get_numberOfPages():
    pass

def get_publishingDate():
    pass

def get_characters():
    pass

def get_setting():
    pass

def get_url():
    pass


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
    if field_values[6] == False:
        pass
        #do nothing
    #else:
         #write .tsv file
    #return field_values


if __name__ == "__main__":
    
    book_fields = []
    for i in range(100):
        open_and_read_html('./htmls//article_'+str(i+1)+'.html')
        source = open_and_read_html('./htmls//article_1.html')
        bookTitle = get_bookTitle(source)
        book_fields.append(bookTitle)
    print(book_fields)
