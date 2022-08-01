import sqlite3

dbConnection = sqlite3.connect('quotes.db')

cursorObject = dbConnection.cursor()

def totalQuotesCount():
    getTotalQuotes = """SELECT COUNT(*) FROM quotes"""
    cursorObject.execute(getTotalQuotes)
    totalQuotes = cursorObject.fetchall()
    for each in totalQuotes:
        for item in each:
            print(item)



totalQuotesCount()