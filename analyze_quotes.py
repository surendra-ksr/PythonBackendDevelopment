import sqlite3

dbConnection = sqlite3.connect('quotes.db')

cursorObject = dbConnection.cursor()

def totalQuotesCount():
    getTotalQuotes_command = """SELECT COUNT(*) FROM quotes"""
    cursorObject.execute(getTotalQuotes_command)
    totalQuotes = cursorObject.fetchall()
    stringStatement = "Total no. of quotations on the website are :"
    for each in totalQuotes:
        for item in each:
            print("\n") #To get Line Space
            print(stringStatement + str(item))

def totalQuotesBy(authorName):
    getCountOfQuotesByAuthor_Command = """SELECT COUNT(*) FROM quotes WHERE author LIKE ?""" 
    cursorObject.execute(getCountOfQuotesByAuthor_Command,(authorName,))
    quotesCount = cursorObject.fetchall()
    for each in quotesCount:
        for item in each:
            resultStatement = "No. of quotations authored by the given {} : ".format(authorName)
            print("\n") #To get Line Space
            print(resultStatement + str(item))
            print("\n") #To get Line Space


def analyseTagsCount():
    getAnalysisOfTags_Command = """SELECT MIN(tagCount), MAX(tagCount), ROUND(AVG(tagCount),2) FROM (SELECT COUNT(tag_id) AS tagCount FROM tags GROUP BY quote_id)""" 
    cursorObject.execute(getAnalysisOfTags_Command)
    tagsAnalysis = cursorObject.fetchall()
    strings = ["Minimum no. of tags on the quotations: ", "Maximun no. of tags on the quotations: ","Average no. of tags on the quotations: "]
    for each in tagsAnalysis:
        for i in range(len(each)):
            print(strings[i] + str(each[i]))
        print("\n") #To get Line Space
            
def getTopNnoOfAuthors(N):
    getAnalysisOfTags_Command = """SELECT author, COUNT(author) AS countQuotes FROM quotes GROUP BY author ORDER BY countQuotes DESC LIMIT ? """ 
    cursorObject.execute(getAnalysisOfTags_Command,(N,))
    authors = cursorObject.fetchall()
    print("\n") #To get Line Space
    print("Top {} authors who authored the maximum number of quotations are : ".format(N))
    for each in authors:
        for i in range(len(each)):
            print(each[0])
            break
    print("\n") #To get Line Space      


totalQuotesCount()

totalQuotesBy("Albert Einstein")

analyseTagsCount()

getTopNnoOfAuthors(5)