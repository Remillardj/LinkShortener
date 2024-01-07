from flask import Flask, redirect, request, jsonify
import random
import string
from markupsafe import escape
import validators

import storage.redis_storage
import storage.mysql_storage

# establish redis connection
r = storage.redis_storage.redis_connection()

# create the table
mydb = storage.mysql_storage.mysql_connection()
mycursor = mydb.cursor()
storage.mysql_storage.create_table(mydb, mycursor)

app = Flask(__name__)

# Return the URL
@app.route('/<shortened_link>', methods=['GET'])
def reroute_to_full_link(shortened_link: str):
    cleaned_shortened_link: str = escape(shortened_link)
    if (r.exists(cleaned_shortened_link)):
        full_link: str = str(r.get(cleaned_shortened_link), encoding='utf-8')
        return redirect(full_link, code=302)
    else:
        return 'Error! Unable to retrieve a link'
    
# Generate a new shortened link
@app.route('/shorten', methods=['POST'])
def generate_shortened_link():
    request_data = request.get_json()
    url = request_data['url']

    if validators.url(url):
        url_key = shorten_link(url)

    storage.mysql_storage.insert_into_table(mydb, mycursor, url_key, url)
    
    return "URL key is 127.0.0.1:5000/{}".format(url_key)

# Generate a random string for the shortened link
def generate_random(length: int = None) -> str | None:
    if length == None:
        length = 8
    letters: str = string.ascii_lowercase
    result_str: str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# Set the shortened link in Redis
def shorten_link(link: str):
    url_key = generate_random()
    if (r.exists(url_key) == True):
        shorten_link(link)
    try:
        if r.set(url_key, link): # set the shortener
            return url_key
    except Exception as e:
        print("Error: ", e)
        return False

# Obtain all shortened links
@app.route('/all', methods=['GET'])
def get_all_redis():
    try:
        # Retrieve all keys and values from Redis
        keys = [key.decode('utf-8') for key in r.keys('*')]
        data = {}

        for key in keys:
            value_type = r.type(key).decode('utf-8')

            if value_type == 'string':
                data[key] = r.get(key).decode('utf-8')
            elif value_type == 'hash':
                data[key] = {field.decode('utf-8'): value.decode('utf-8') for field, value in r.hgetall(key).items()}

        # Return the data as JSON
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(port=8000)