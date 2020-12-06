
from collections import OrderedDict
from ordered_set import OrderedSet
import seaborn as sns
import matplotlib.pyplot as plt
import re


def get_series_from_tsv(file_name):
    '''

    Args:
        file_name: The path of the tsv file associated to a book

    Returns: The series of the book

    '''
    with open(file_name, 'r', encoding = 'utf-8') as f:
        all_fields = f.readlines()[2].split('\t')
        series = all_fields[1]
    return series


def get_title_from_tsv(file_name):
    '''

    Args:
        file_name: The path of the tsv file associated to a book

    Returns: The title of the book

    '''
    with open(file_name, 'r', encoding = 'utf-8') as f:
        all_fields = f.readlines()[2].split('\t')
        title = all_fields[0]
    return title


def get_publishing_year_from_tsv(file_name):
    '''

    Args:
        file_name: The path of the tsv file associated to a book

    Returns: The publishing date of the book

    '''
    with open(file_name, 'r', encoding = 'utf-8') as f:
        all_fields = f.readlines()[2].split('\t')
        date = all_fields[8]
    return date

# Get number the number of pages from a tsv file (of a book)
def get_npages_from_tsv(file_name):
    '''

    Args:
        file_name: The path of the tsv file associated to a book

    Returns: The number of the pages of the book

    '''
    with open(file_name, 'r', encoding = 'utf-8') as f:
        all_fields = f.readlines()[2].split('\t')
        nPages = all_fields[7]
    return nPages


def get_book_series_for_plot():
    '''

    Returns: The list of the first 10 book series in order of appearance (es.4)

    '''

    # Setting the patterns for the regexes
    filterSeries = r'.*#[0-9]{1,}'  # Pattern userd to filter series by the format The Hunger Games #1
                                    # (We are excluding series written like "To Kill a Mockingbird" and
                                    # "The Lord of The Rings #0-7")

    cleanTitle = r' #[0-9]{1,}'     # Pattern used to clean the series of the book in order to get the title
                                    # If we apply this filter to "The Hunger Games #1" we get "The Hunger Games"

    listOfBookSeries = list()       # List of the first 10 series in order of appearance

    # Considering the first 10 book series in order of appearance
    i = 1
    while len(listOfBookSeries) < 10:
        try:
            seriesName = get_series_from_tsv("./tsvs//article_" + str(i) + ".tsv")  # The name of the series of the book

            # Cleaning the name of the series to get the title
            cleanr = re.compile(cleanTitle)
            title = re.sub(cleanr, "", seriesName)

            # Checking if the field we got is not null, it matches the filterSeries filter and
            # it isn't already exist in the list of the books series
            if seriesName and re.fullmatch(filterSeries, seriesName) and title not in listOfBookSeries:

                # Cleaning the name of the series to get the title and adding it to the list f the books series
                cleanr = re.compile(cleanTitle)
                seriesName = re.sub(cleanr, "", seriesName)

                # Adding the new book series to the final list
                listOfBookSeries.append(seriesName)

        # Catching an exception we iterate over the tsv files; not all of them exist since some book were not in English
        except:
            pass

        i = i + 1

    return listOfBookSeries


def get_dict_book_series():
    '''

    Returns: A dictionary containing the title as keys and lists of tuples as values
             (Example: The Hunger Games : [(2008,374), (2009,391)], Harry Potter : [(...),(...)]
             (A tuple contains the pair: publishing year and number of pages for a book series)
             (The list of tuples is sorted respect to the publishing year for every book series)

    '''
    listOfBookSeries = get_book_series_for_plot()

    # Setting patterns for the regex
    filterSeries = r'.*#[0-9]{1,}'  # Pattern userd to filter series by the format The Hunger Games #1
                                    # (We are excluding series written like "To Kill a Mockingbird"
                                    # and "The Lord of The Rings #0-7")

    cleanTitle = r' #[0-9]{1,}'     # Pattern used to clean the series of the book in order to get the title
                                    # If we apply this filter to "The Hunger Games #1" we get "The Hunger Games"

    dicOfSeries = OrderedDict()

    # The range is defined about the total number of tsv files we obtained (some if them were excluded because not in English)
    for i in range(27175):
        try:
            # The name of the series of the book
            seriesName = get_series_from_tsv(
                "./tsvs//article_" + str(i + 1) + ".tsv")

            # Cleaning the name of the series to get the title
            cleanr = re.compile(cleanTitle)
            title = re.sub(cleanr, "", seriesName)

            # Checking if the field we got is not null, it matches the filterSeries filter and
            # if the name of the book is in the list of series we are looking for
            if seriesName and re.fullmatch(filterSeries, seriesName) and title in listOfBookSeries:

                # Getting the year in which the book series was published
                date = get_publishing_year_from_tsv("./tsvs//article_" + str(i + 1) + ".tsv")
                year = int(re.match(r'.*([0-9]{4})', date).group(1))

                # Getting the number of pages of the book series
                nPages = int(get_npages_from_tsv("./tsvs//article_" + str(i + 1) + ".tsv"))

                # Adding the title to the dictionary
                if title not in dicOfSeries:
                    dicOfSeries[title] = list()

                # Adding the tuple (publishing year, number of pages) of book series to the dictionary
                dicOfSeries[title].append((year, nPages))

        except:
            pass

        i = i + 1

    # Sorting the dictionary respect to the publishing year for each book
    for title in dicOfSeries.keys():
        dicOfSeries[title].sort(key=lambda tup: tup[0])

    return dicOfSeries


def prepare_plot_points():
    '''

    Returns: A dictionary containing for each book the final points to be plotted
             A point (a tuple) is made of the publishing year and and cumulative number of pages

    '''

    dict = get_dict_book_series()

    # Iterating over the dictionary
    for title, series_info in dict.items():

        # List containing year and number of pages of each book series
        res = []

        # The variable containing the cumulative number of pages
        sumPages = 0

        # Interating over the tuple of a book series
        for year, nPages in series_info:
            sumPages += nPages
            res.append((year-series_info[0][0], sumPages))

        # Adding new list contaning the new tuples of year and number of cumulative pages of a book series
        dict[title] = res

    return dict


def plotting_the_book_series():
    '''

    Returns: The final plot of the ten book series in order of appearance (es. 4)

    '''

    # Getting the points to plot
    dictOfPoints = prepare_plot_points()

    # Storing titles and years
    listOfTitles = list()
    listOfYears = list()

    sns.set_theme(style="darkgrid")
    fig = plt.gcf()
    fig.set_size_inches(16, 8)

    for title, series_info in dictOfPoints.items():
        x = [tup[0] for tup in series_info]  # Getting the year of a book series
        y = [tup[1] for tup in series_info]  # Getting the number of pages of a book series
        tt = sns.lineplot(x=x, y=y, marker="o")
        listOfTitles.append(title)
        listOfYears.append(x)

    # Creating a set of unique years to set the ticks of the plot
    listOfYears = [item for sublist in listOfYears for item in sublist]
    listOfYears = OrderedSet(listOfYears)

    plt.title("First ten book series in order of appearance")
    tt.set(xlabel="Year", ylabel="Number of pages")
    tt.set_xticks(listOfYears)
    tt.legend(listOfTitles)
    plt.show()



# -------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    plotting_the_book_series()































