import requests
from bs4 import BeautifulSoup
import json

quotesFinalObject = dict()
quotes = []
authors = []
# flag is used to stop the function if the last page is reached.
flag = True
pageNo = 1
authorUrlsSet = set()
while flag:
    quotesUrl = f"http://quotes.toscrape.com/page/{pageNo}"
    quotesPage = requests.get(quotesUrl)
    pageSoup = BeautifulSoup(quotesPage.content, "html.parser")
    nextElement = pageSoup.find_all("li", class_="next")

    quoteDivs = pageSoup.find_all("div",class_="quote")
    for quoteDiv in quoteDivs:
        quoteData = dict()
        tags=[]
        
        quoteElements = quoteDiv.find_all("span",class_="text")
        for quoteItem in quoteElements:
            # Using replace() to remove the extra quotes(") from the quotes extracted
            quoteItem = quoteItem.text.replace('\u201c', '').replace('\u201d', '')
            quoteData["quote"] = quoteItem

        authorElements = quoteDiv.find_all("small",class_="author")
        for authorItem in authorElements:
            quoteData["author"] = authorItem.text

        authorLinks = quoteDiv.find_all("a")
        for link in authorLinks:
            linkUrl = link["href"]
            if "/author/" in linkUrl:
                authorUrlsSet.add(linkUrl)


        tagElements = quoteDiv.find_all("a", class_="tag")
        for tag  in tagElements:
            tags.append(tag.text)

        quoteData["tags"] = tags
        quotes.append(quoteData)
    # Checking if the last page is reached.
    if nextElement==[]:
        flag = False
    pageNo +=1

authorUrlsList = list(authorUrlsSet)


for authorUrl in authorUrlsList:
    authorPageUrl = f"http://quotes.toscrape.com/{authorUrl}"
    authorPage = requests.get(authorPageUrl)
    authorPageSoup = BeautifulSoup(authorPage.content, "html.parser")
    authorBornDate = authorPageSoup.find_all("span", class_="author-born-date")
    authorLocation = authorPageSoup.find_all("span", class_="author-born-location")
    author= dict()
    for date in authorBornDate:
        dateEle = date.text
        
    for each in authorLocation:
        locatonEle = each.text

    born = dateEle+" "+locatonEle
        
    authorNameDiv = authorPageSoup.find("h3", class_="author-title")
    for each in authorNameDiv:
        author["name"] = each
        
        break

    author["born"] = born
    author["reference"] = authorPageUrl

    authors.append(author)

quotesFinalObject["quotes"] = quotes
quotesFinalObject["authors"] = authors


#Opening json file with 'write' access mode.
jsonFile = open("quotes.json","w")

# Writing the data into json file.
json.dump(quotesFinalObject,jsonFile, indent=4)
