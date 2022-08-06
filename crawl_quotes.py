import requests
from bs4 import BeautifulSoup
import json


def get_all_quotes_and_Author_urls_list():
    # "is_last_page_reached" is used to stop the function if the last page is reached.
    is_last_page_not_reached = True
    next_page_url = ""
    author_urls_set = set()
    quotes = []
    while is_last_page_not_reached:
        page_soup = get_page_soup(next_page_url)
        next_element = page_soup.find_all("li", class_="next")
        get_quotes_and_authors_set(page_soup,author_urls_set,quotes)
        # Checking if the last page is reached.
        if (next_element!=[]):
            next_page_url = next_element[0].find("a")["href"]
        else:
            is_last_page_not_reached = False

    author_urls_list = list(author_urls_set)
    quotes_list_and_author_urls_list = [quotes,author_urls_list]
    return quotes_list_and_author_urls_list

def get_page_soup(next_page_url):
    quotes_url = f"http://quotes.toscrape.com{next_page_url}"
    quotes_page = requests.get(quotes_url)
    page_soup = BeautifulSoup(quotes_page.content, "html.parser")
    return page_soup


def get_quotes_and_authors_set(page_soup,author_urls_set,quotes):
    quote_divs = page_soup.find_all("div",class_="quote")
    for quote_div in quote_divs:
        quote_data_and_author_url = get_each_quote_data(quote_div)
            
        quotes.append(quote_data_and_author_url[0])
        author_urls_set.add(quote_data_and_author_url[1])

def get_each_quote_data(quote_div):
    quote_data = dict()
    quote_elements = quote_div.find_all("span",class_="text")
    quote_data["quote"] = get_quotes(quote_elements)

    author_elements = quote_div.find_all("small",class_="author")
    quote_data["author"] = get_author_of_quote(author_elements)

    author_links = quote_div.find("a")
    each_author_link = author_links["href"]

    tag_elements = quote_div.find_all("a", class_="tag")
    quote_data["tags"] = get_tags_of_each_quote(tag_elements)

    quote_data_and_author_url = [quote_data,each_author_link]
    return quote_data_and_author_url


def get_quotes(quote_elements):
    for quote_item in quote_elements:
        # Using replace() to remove the extra quotes(") from the quotes extracted
        quote_item = quote_item.text.strip("\u201c,\u201d").replace("\u2032","")
        return quote_item

def get_author_of_quote(author_elements):
    for author_item in author_elements:
        return author_item.text

            
def get_tags_of_each_quote(tag_elements): 
    tags = []
    for tag  in tag_elements:
        tags.append(tag.text)
    return tags


quotes_list_and_author_urls_list = get_all_quotes_and_Author_urls_list()


def get_author_details(author_page_soup):
    #To get author name and born date and location from author_page_soup
    author = dict()
    author_born_date = author_page_soup.find_all("span", class_="author-born-date")
    author_location = author_page_soup.find_all("span", class_="author-born-location")
    author_name_div = author_page_soup.find("h3", class_="author-title")

    author["name"] = get_author_name(author_name_div)
    author["born"] = get_author_born_details(author_born_date,author_location)
    
    return author

def get_author_name(author_name_div):
    for each in author_name_div:
        name = each
        break
    return name

def get_author_born_details(author_born_date,author_location):
    date_element = ""
    locaton_element = ""
    for date in author_born_date:
        date_element = date.text
   
    for each in author_location:
        locaton_element = each.text
# Born date and location is converted into a single string
    born_details = date_element+" "+locaton_element
    return born_details


author_urls_list = quotes_list_and_author_urls_list[1]

def get_authors_list(author_urls_list):
    quotes_final_object = dict()
    authors = []
    for author_url in author_urls_list:
        author = each_author_page_soup(author_url)
        authors.append(author)
        
    return authors

def each_author_page_soup(author_url):
    author_page_url = f"http://quotes.toscrape.com{author_url}"
    author_page = requests.get(author_page_url)
    author_page_soup = BeautifulSoup(author_page.content, "html.parser")
    author = get_author_details(author_page_soup)
    author["reference"] = author_page_url
    return author


def get_final_data(quotes_list_and_author_urls_list):
    quotes_final_object = dict()
    author_urls_list = quotes_list_and_author_urls_list[1]
    quotes_final_object["quotes"] = quotes_list_and_author_urls_list[0]
    quotes_final_object["authors"] = get_authors_list(author_urls_list)

    return quotes_final_object
    
quotes_final_object = get_final_data(quotes_list_and_author_urls_list)

#Opening json file with 'write' access mode.
jsonFile = open("quotes.json","w")

# Writing the data into json file.
json.dump(quotes_final_object,jsonFile, indent=4)
