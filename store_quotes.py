import sqlite3
import json

db_connection = sqlite3.connect('quotes.db')

cursor_object = db_connection.cursor()
print("Connected to database")



def creating_quotes_table():
    create_quotes_table_command = """CREATE TABLE quotes (
    quote_id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT,
    author_id INTEGER,
    FOREIGN KEY(author_id) REFERENCES authors(author_id) on DELETE CASCADE);"""
    
    cursor_object.execute("DROP TABLE IF EXISTS quotes")
    cursor_object.execute(create_quotes_table_command)

def creating_authors_table():
    create_authors_table_command = """CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) ,
    born TEXT,
    reference_url VARCHAR(250));"""

    cursor_object.execute("DROP TABLE IF EXISTS authors")
    cursor_object.execute(create_authors_table_command)

def creating_tags_table():
    create_tags_table_command = """CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag VARCHAR(100) UNIQUE );"""

    cursor_object.execute("DROP TABLE IF EXISTS tags")
    cursor_object.execute(create_tags_table_command)

def creating_quote_tag_table():
    create_quote_tag_table_command = """CREATE TABLE quote_tag (
    id INTEGER NOT NULL PRIMARY KEY,
    tag_id INTEGER,
    quote_id INTEGER,
    FOREIGN KEY(tag_id) REFERENCES tags(tag_id) on DELETE CASCADE,
    FOREIGN KEY(quote_id) REFERENCES quotes(quote_id) on DELETE CASCADE );"""

    cursor_object.execute("DROP TABLE IF EXISTS quote_tag")
    cursor_object.execute(create_quote_tag_table_command)

def creating_quotes_tags_authors_table():
    creating_quotes_table()
    creating_authors_table()
    creating_tags_table()
    creating_quote_tag_table()

creating_quotes_tags_authors_table()

def get_json_data_from_json_file():

    # Opening quotes.json file with 'read' access and loading data to a variable
    json_file = open("quotes.json","r")
    json_data = json.load(json_file)
    return json_data

json_data = get_json_data_from_json_file()


def insert_data_into_authors_table(authors_list):
    insert_authors_command = "INSERT OR IGNORE INTO authors(name,born,reference_url) VALUES(?,?,?);"
    for author in authors_list:
        name = author["name"]
        born = author["born"]
        reference = author["reference"]
        cursor_object.execute(insert_authors_command,(name,born,reference))

authors_list = json_data["authors"]
insert_data_into_authors_table(authors_list)        

def inserting_data_into_tables(json_data):
    quotes_list = json_data["quotes"]
    authors_list = json_data["authors"]

    #initialising quote_count and tag_count to create 'quote_id' and 'tag_id' in the tables
    insert_quotes_command = "INSERT INTO quotes(quote,author_id) VALUES(?,(SELECT author_id FROM authors WHERE name=?));"
    
    #getting individual Quote and inserting it into 'quote' table
    for quote_object in quotes_list:
        quote = quote_object["quote"]
        author = quote_object["author"]
        tags = quote_object["tags"]
        cursor_object.execute(insert_quotes_command,(quote,author))

        inserting_in_tags_and_quote_tag_tables(tags,quote)

def inserting_in_tags_and_quote_tag_tables(tags,quote):
    insert_tags_command = "INSERT OR IGNORE INTO tags(tag) VALUES(?);"
    insert_quote_tag_command = "INSERT INTO quote_tag(tag_id,quote_id) VALUES((SELECT tag_id FROM tags WHERE tag=?),(SELECT quote_id FROM quotes WHERE quote=?));"
    for each in tags:
        cursor_object.execute(insert_tags_command,(each,))
        cursor_object.execute(insert_quote_tag_command,(each,quote))

inserting_data_into_tables(json_data)

authors_list = json_data["authors"]
insert_data_into_authors_table(authors_list)     

db_connection.commit()

db_connection.close()
print("completed")