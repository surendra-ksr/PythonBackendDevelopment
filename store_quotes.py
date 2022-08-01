import sqlite3
import json
from tkinter.tix import INTEGER

dbConnection = sqlite3.connect('quotes.db')

cursorObject = dbConnection.cursor()
print("Connected to database")

createQuotesTable_command = """CREATE TABLE quotes (
    quote_id INTEGER PRIMARY KEY,
    quote TEXT,
    author VARCHAR(200));"""

cursorObject.execute(createQuotesTable_command)

createTagsTable_command = """CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY,
    tag VARCHAR(100),
    quote_id INTEGER,
    FOREIGN KEY(quote_id) REFERENCES quotes(quote_id) on DELETE CASCADE );"""

cursorObject.execute(createTagsTable_command)

insertQuotesCommand = "INSERT INTO quotes VALUES(?,?,?);"
insertTagsCommand = "INSERT INTO tags VALUES(?,?,?);"
 
jsonFile = open("quotes.json","r")
jsonData = json.load(jsonFile)

for data in jsonData:
    quoteCount = 1
    tagCount = 1
    dataObj = jsonData[data]
    for quoteObject in dataObj:
        quote = quoteObject["quote"]
        author = quoteObject["author"]
        cursorObject.execute(insertQuotesCommand,(quoteCount,quote,author))
        for each in quoteObject["tags"]:
            cursorObject.execute(insertTagsCommand,(tagCount,each,quoteCount))
            tagCount +=1
        quoteCount +=1
    break

dbConnection.commit()

dbConnection.close()
