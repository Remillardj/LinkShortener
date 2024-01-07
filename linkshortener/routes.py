from markupsafe import escape
from flask import redirect, Flask

import storage.redis_storage

# establish redis connection
r = storage.redis_storage.redis_connection()

app = Flask(__name__)

@app.route('/<shortened_link>', methods=['GET'])
def reroute_to_full_link(shortened_link: str):
    cleaned_shortened_link: str = escape(shortened_link)
    if (r.exists(cleaned_shortened_link)):
        full_link: str = str(r.get(cleaned_shortened_link), encoding='utf-8')
        return redirect(full_link, code=302)
    else:
        return 'Error! Unable to retrieve a link'