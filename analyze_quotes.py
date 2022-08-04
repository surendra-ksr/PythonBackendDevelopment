import sqlite3

dbConnection = sqlite3.connect('quotes.db')

cursorObject = dbConnection.cursor()

# To get total no. of quotations on the website.
def total_quotes_count():
    getTotalQuotes_command = """SELECT COUNT(*) FROM quotes"""
    cursorObject.execute(getTotalQuotes_command)
    totalQuotes = cursorObject.fetchall()
    stringStatement = "Total no. of quotations on the website are :"
    print("\n") #To get Line Space
    totalQuotes = stringStatement + str(totalQuotes[0][0])
    return totalQuotes
    
# To get no. of quotations authored by the given author’s name with 'authorName' as parameter.
def total_quotes_by(authorName):
    getCountOfQuotesByAuthor_Command = """SELECT COUNT(*) FROM quotes WHERE author = ?""" 
    cursorObject.execute(getCountOfQuotesByAuthor_Command,(authorName,)) # "authorName" is the parameter
    quotesCount = cursorObject.fetchall()
    resultStatement = "No. of quotations authored by the given {} : ".format(authorName)
    totalQuotesBy = resultStatement + str(quotesCount[0][0])
    return totalQuotesBy

# To get Minimum, Maximum, and Average no. of tags on the quotations.
def analyse_tags_count():
    getAnalysisOfTags_Command = """SELECT MIN(tagCount), MAX(tagCount), ROUND(AVG(tagCount),2) FROM (SELECT COUNT(tag_id) AS tagCount FROM tags GROUP BY quote_id)""" 
    cursorObject.execute(getAnalysisOfTags_Command)
    tagsAnalysis = cursorObject.fetchall()
    strings = ["Minimum no. of tags on the quotations: ", "Maximun no. of tags on the quotations: ","Average no. of tags on the quotations: "]
    MinMaxAvg = []
    for i in range(3):
        MinMaxAvg.append(strings[i] + str(tagsAnalysis[0][i]))
    return MinMaxAvg
    
"""To get top N(with 'N' as parameter) authors who authored 
    the maximum number of quotations sorted in descending order of no. of quotes"""        
def get_top_n_no_of_authors(N):
    getAnalysisOfTags_Command = """SELECT author, COUNT(author) AS countQuotes FROM quotes GROUP BY author ORDER BY countQuotes DESC LIMIT ? """ 
    cursorObject.execute(getAnalysisOfTags_Command,(N,))  # "N" is the parameter
    authors = cursorObject.fetchall()
    print("Top {} authors who authored the maximum number of quotations are : ".format(N))
    topAuthorsList = []
    for i in range(N):
        topAuthorsList.append(authors[i][0]) 
    return topAuthorsList   

def get_tags_of_author(author):
    getAnalysisOfTags_Command = """SELECT tag FROM quotes LEFT JOIN tags ON quotes.quote_id = tags.quote_id WHERE author=?""" 
    cursorObject.execute(getAnalysisOfTags_Command,(author,))   # "author" is the parameter
    tags = cursorObject.fetchall()
    print("Tags related to author {} are : ".format(author))
    tagsOfAuthor = []
    for i in tags:
        tagsOfAuthor.append(i[0])
    return tagsOfAuthor

def get_link_of_an_author(author):
    getLinkOfAuthor_command = """SELECT reference_url FROM authors WHERE name=?"""
    cursorObject.execute(getLinkOfAuthor_command,(author,)) # "author" is the parameter
    link = cursorObject.fetchall()
    exactLink = link[0][0]
    return exactLink


total_quotes_count()

total_quotes_by("Albert Einstein")

analyse_tags_count()

get_top_n_no_of_authors(5)

get_tags_of_author("Albert Einstein")

get_link_of_an_author("Albert Einstein")

print(get_link_of_an_author("Albert Einstein"))
print(get_tags_of_author("Albert Einstein"))
print(get_top_n_no_of_authors(5))
print(analyse_tags_count())
print(total_quotes_by("Albert Einstein"))
print(total_quotes_count())

