import sqlite3
import json
from tkinter.tix import INTEGER

dbConnection = sqlite3.connect('quotes.db')

cursorObject = dbConnection.cursor()
print("Connected to database")



def creating_quotes_tags_authors_table():
    createQuotesTable_command = """CREATE TABLE quotes (
    quote_id INTEGER PRIMARY KEY,
    quote TEXT,
    author VARCHAR(200));"""

    createAuthorsTable_command = """CREATE TABLE authors (
    name VARCHAR(200) PRIMARY KEY,
    born TEXT,
    reference_url VARCHAR(250));"""

    createTagsTable_command = """CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY,
    tag VARCHAR(100),
    quote_id INTEGER,
    FOREIGN KEY(quote_id) REFERENCES quotes(quote_id) on DELETE CASCADE );"""

    cursorObject.execute(createQuotesTable_command)
    cursorObject.execute(createAuthorsTable_command)
    cursorObject.execute(createTagsTable_command)

"""creating_quotes_tags_authors_table()"""


def get_json_data_from_json_file():

    # Opening quotes.json file with 'read' access and loading data to a variable
    jsonFile = open("quotes.json","r")
    jsonData = json.load(jsonFile)
    return jsonData

jsonData = get_json_data_from_json_file()


def insert_data_into_authors_table(authorsList):
    insertAuthorsCommand = "INSERT INTO authors VALUES(?,?,?);"
    for author in authorsList:
        name = author["name"]
        born = author["born"]
        reference = author["reference"]
        cursorObject.execute(insertAuthorsCommand,(name,born,reference))
        

def inserting_data_into_tables(jsonData):
    quotesList = jsonData["quotes"]
    authorsList = jsonData["authors"]

    #initialising quoteCount and tagCount to create 'quote_id' and 'tag_id' in the tables
    quoteCount = 1
    tagCount = 1
    insertQuotesCommand = "INSERT INTO quotes VALUES(?,?,?);"
    insertTagsCommand = "INSERT INTO tags VALUES(?,?,?);"
    
    #getting individual Quote and inserting it into 'quote' table
    for quoteObject in quotesList:
        quote = quoteObject["quote"]
        author = quoteObject["author"]
        cursorObject.execute(insertQuotesCommand,(quoteCount,quote,author))
   
        for each in quoteObject["tags"]:
            cursorObject.execute(insertTagsCommand,(tagCount,each,quoteCount))
            tagCount +=1
        
        quoteCount +=1

    insert_data_into_authors_table(authorsList)

inserting_data_into_tables(jsonData)


dbConnection.commit()

dbConnection.close()
