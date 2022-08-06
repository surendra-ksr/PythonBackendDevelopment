import sqlite3
import json

db_connection = sqlite3.connect('quotes.db')

cursor_object = db_connection.cursor()
print("Connected to database")



def creating_quotes_tags_authors_table():
    create_quotes_table_command = """CREATE TABLE quotes (
    quote_id INTEGER PRIMARY KEY,
    quote TEXT,
    author VARCHAR(200));"""

    create_authors_table_command = """CREATE TABLE authors (
    name VARCHAR(200) PRIMARY KEY,
    born TEXT,
    reference_url VARCHAR(250));"""

    create_tags_table_command = """CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY,
    tag VARCHAR(100),
    quote_id INTEGER,
    FOREIGN KEY(quote_id) REFERENCES quotes(quote_id) on DELETE CASCADE );"""

    cursor_object.execute(create_quotes_table_command)
    cursor_object.execute(create_authors_table_command)
    cursor_object.execute(create_tags_table_command)

creating_quotes_tags_authors_table()


def get_json_data_from_json_file():

    # Opening quotes.json file with 'read' access and loading data to a variable
    json_file = open("quotes.json","r")
    json_data = json.load(json_file)
    return json_data

json_data = get_json_data_from_json_file()


def insert_data_into_authors_table(authors_list):
    insert_authors_command = "INSERT INTO authors VALUES(?,?,?);"
    for author in authors_list:
        name = author["name"]
        born = author["born"]
        reference = author["reference"]
        cursor_object.execute(insert_authors_command,(name,born,reference))
        

def inserting_data_into_tables(json_data):
    quotes_list = json_data["quotes"]
    authors_list = json_data["authors"]

    #initialising quote_count and tag_count to create 'quote_id' and 'tag_id' in the tables
    quote_count = 1
    tag_count = 1
    insert_quotes_command = "INSERT INTO quotes VALUES(?,?,?);"
    insert_tags_command = "INSERT INTO tags VALUES(?,?,?);"
    
    #getting individual Quote and inserting it into 'quote' table
    for quote_object in quotes_list:
        quote = quote_object["quote"]
        author = quote_object["author"]
        cursor_object.execute(insert_quotes_command,(quote_count,quote,author))
   
        for each in quote_object["tags"]:
            cursor_object.execute(insert_tags_command,(tag_count,each,quote_count))
            tag_count +=1
        
        quote_count +=1

    insert_data_into_authors_table(authors_list)

inserting_data_into_tables(json_data)


db_connection.commit()

db_connection.close()
