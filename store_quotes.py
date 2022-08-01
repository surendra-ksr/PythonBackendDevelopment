import sqlite3
import json
from tkinter.tix import INTEGER

dbConnection = sqlite3.connect('quotes.db')

cursorObject = dbConnection.cursor()
print("Connected to database")

createTable_command = """CREATE TABLE quotes (
    quote_id INTEGER PRIMARY KEY,
    quote TEXT,
    author VARCHAR(200));"""

createAuthorTable_command = """CREATE TABLE author (
    author_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    quote_id INTEGER,
    FOREIGN KEY(quote_id) REFERENCES quotes(quote_id) on DELETE CASCADE );"""

insertQuotesCommand = "INSERT INTO quotes VALUES(?,?,?);"
 
jsonFile = open("quotes.json","r")
jsonData = json.load(jsonFile)

for data in jsonData:
    quoteCount = 1
    dataObj = jsonData[data]
    """for i in dataObj:
        quote = i["quote"]
        author = i["author"]

        cursorObject.execute(insertQuotesCommand,(quoteCount,quote,author))
        quoteCount +=1
    break   """

authorsData = jsonData["authors"]
for author in authorsData:
    print(author["born"])


dbConnection.commit()
"""cursorObject.execute(createTable_command)"""
