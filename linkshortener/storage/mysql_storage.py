import mysql.connector

def mysql_connection():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="linkshortener"
        )
        return mydb
    except Exception as e:
        print("Error: ", e)
        exit(1)

def create_table(mydb, mycursor):
    try:
        # Create Table
        mycursor.execute("CREATE TABLE IF NOT EXISTS shortened_links (id INT AUTO_INCREMENT PRIMARY KEY, url_key VARCHAR(255) NOT NULL, full_url VARCHAR(255) NOT NULL)")
        mydb.commit()
    except Exception as e:
        print("Error: ", e)
        exit(1)

def insert_into_table(mydb, mycursor, url_key: str, url: str):
    query = "INSERT INTO shortened_links (url_key, full_url) VALUES ('" + url_key + "', '" + url + "');"
    print(query)
    try:
        mycursor.execute(query)
        mydb.commit()
        print(mycursor.rowcount, "records inserted")
    except Exception as e:
        print("Error: ", e)
        exit(1)