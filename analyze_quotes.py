import sqlite3

dbConnection = sqlite3.connect('quotes.db')

cursorObject = dbConnection.cursor()

def totalQuotesCount():
    getTotalQuotes_command = """SELECT COUNT(*) FROM quotes"""
    cursorObject.execute(getTotalQuotes_command)
    totalQuotes = cursorObject.fetchall()
    stringStatement = "Total no. of quotations on the website are :"
    print("\n") #To get Line Space
    print(stringStatement + str(totalQuotes[0][0]))
    

def totalQuotesBy(authorName):
    getCountOfQuotesByAuthor_Command = """SELECT COUNT(*) FROM quotes WHERE author LIKE ?""" 
    cursorObject.execute(getCountOfQuotesByAuthor_Command,(authorName,))
    quotesCount = cursorObject.fetchall()
    resultStatement = "No. of quotations authored by the given {} : ".format(authorName)
    print("\n") #To get Line Space
    print(resultStatement + str(quotesCount[0][0]))
    


def analyseTagsCount():
    getAnalysisOfTags_Command = """SELECT MIN(tagCount), MAX(tagCount), ROUND(AVG(tagCount),2) FROM (SELECT COUNT(tag_id) AS tagCount FROM tags GROUP BY quote_id)""" 
    cursorObject.execute(getAnalysisOfTags_Command)
    tagsAnalysis = cursorObject.fetchall()
    strings = ["Minimum no. of tags on the quotations: ", "Maximun no. of tags on the quotations: ","Average no. of tags on the quotations: "]
    
    for i in range(3):
        print(strings[i] + str(tagsAnalysis[0][i]))
    print("\n") #To get Line Space
    
            
def getTopNnoOfAuthors(N):
    getAnalysisOfTags_Command = """SELECT author, COUNT(author) AS countQuotes FROM quotes GROUP BY author ORDER BY countQuotes DESC LIMIT ? """ 
    cursorObject.execute(getAnalysisOfTags_Command,(N,))
    authors = cursorObject.fetchall()
    print("\n") #To get Line Space
    print("Top {} authors who authored the maximum number of quotations are : ".format(N))
    for i in range(N):
        print(authors[i][0])
    print("\n") #To get Line Space      


totalQuotesCount()

totalQuotesBy("Albert Einstein")

analyseTagsCount()

getTopNnoOfAuthors(5)