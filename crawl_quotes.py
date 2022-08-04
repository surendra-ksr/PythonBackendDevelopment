import requests
from bs4 import BeautifulSoup
import json


def get_quotes(quoteElements):
    for quoteItem in quoteElements:
        # Using replace() to remove the extra quotes(") from the quotes extracted
        quoteItem = quoteItem.text.replace('\u201c', '').replace('\u201d', '')
        return quoteItem

def get_author_of_quote(authorElements):
    for authorItem in authorElements:
        return authorItem.text

def get_author_urls(authorLinks):
    for link in authorLinks:
        linkUrl = link["href"]
        if "/author/" in linkUrl:
            return linkUrl
            
def get_tags_of_each_quote(tagElements): 
    tags = []
    for tag  in tagElements:
        tags.append(tag.text)
    return tags

def get_each_quote_data(quoteDiv):
    quoteData = dict()
    quoteElements = quoteDiv.find_all("span",class_="text")
    quoteData["quote"] = get_quotes(quoteElements)

    authorElements = quoteDiv.find_all("small",class_="author")
    quoteData["author"] = get_author_of_quote(authorElements)

    authorLinks = quoteDiv.find_all("a")
    eachAuthorLink = get_author_urls(authorLinks)

    tagElements = quoteDiv.find_all("a", class_="tag")
    quoteData["tags"] = get_tags_of_each_quote(tagElements)

    quoteDataAndAuthorUrl = [quoteData,eachAuthorLink]
    return quoteDataAndAuthorUrl
    

def get_all_quotes_and_Author_urls_list():
    # flag is used to stop the function if the last page is reached.
    flag = True
    pageNo = 1
    authorUrlsSet = set()
    quotes = []
    while flag:
        quotesUrl = f"http://quotes.toscrape.com/page/{pageNo}"
        quotesPage = requests.get(quotesUrl)
        pageSoup = BeautifulSoup(quotesPage.content, "html.parser")
        nextElement = pageSoup.find_all("li", class_="next")
        if (nextElement!=[]):
            nextItemUrl = nextElement[0].find("a")["href"]

        quoteDivs = pageSoup.find_all("div",class_="quote")
        for quoteDiv in quoteDivs:
            quoteDataAndAuthorUrl = get_each_quote_data(quoteDiv)
            
            quotes.append(quoteDataAndAuthorUrl[0])
            authorUrlsSet.add(quoteDataAndAuthorUrl[1])

        # Checking if the last page is reached.
        if nextElement==[]:
            flag = False
        pageNo +=1

    authorUrlsList = list(authorUrlsSet)
    quotesListAndAuthorUrlsList = [quotes,authorUrlsList]
    return quotesListAndAuthorUrlsList

quotesListAndAuthorUrlsList = get_all_quotes_and_Author_urls_list()

def get_author_name(authorNameDiv):
    for each in authorNameDiv:
        name = each
        break
    return name

def get_author_born_details(authorBornDate,authorLocation):
    for date in authorBornDate:
        dateEle = date.text
        
    for each in authorLocation:
        locatonEle = each.text
# Born date and location is converted into a single string
    bornDetails = dateEle+" "+locatonEle
    return bornDetails


def get_author_details(authorPageSoup):
    #To get author name and born date and location from authorPageSoup
    author = dict()
    authorBornDate = authorPageSoup.find_all("span", class_="author-born-date")
    authorLocation = authorPageSoup.find_all("span", class_="author-born-location")
    authorNameDiv = authorPageSoup.find("h3", class_="author-title")

    author["name"] = get_author_name(authorNameDiv)
    author["born"] = get_author_born_details(authorBornDate,authorLocation)
    
    return author

authorUrlsList = quotesListAndAuthorUrlsList[1]

def get_authors_list(authorUrlsList):
    quotesFinalObject = dict()
    authors = []
    for authorUrl in authorUrlsList:
        authorPageUrl = f"http://quotes.toscrape.com{authorUrl}"
        authorPage = requests.get(authorPageUrl)
        authorPageSoup = BeautifulSoup(authorPage.content, "html.parser")

        author = get_author_details(authorPageSoup)
        
        author["reference"] = authorPageUrl

        authors.append(author)
        
    return authors

def get_final_data(quotesListAndAuthorUrlsList):
    quotesFinalObject = dict()
    authorUrlsList = quotesListAndAuthorUrlsList[1]
    quotesFinalObject["quotes"] = quotesListAndAuthorUrlsList[0]
    quotesFinalObject["authors"] = get_authors_list(authorUrlsList)

    return quotesFinalObject
    
quotesFinalObject = get_final_data(quotesListAndAuthorUrlsList)

#Opening json file with 'write' access mode.
jsonFile = open("quotes.json","w")

# Writing the data into json file.
json.dump(quotesFinalObject,jsonFile, indent=4)
