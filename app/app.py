from elasticsearch import Elasticsearch
from flask import Flask, render_template, request

from backend.search import search
from constants import INDEX_NAME

app = Flask(__name__)
es = Elasticsearch()

# homepage
@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(
        size=20,
        body={
            "query": {
                "multi_match" : {
                    "query": search_term,
                    "fields": [
                        '*'
                    ]
                }
            }
        }
    )
    return render_template('results.html', res=res )
@app.route('/search', methods=['GET', 'POST'])
def search_single_product():
    """
    Execute a search for a specific search term.

    Return the top 50 results.
    """
    # get the query from the website
    query = request.args.get('search')
    num_results = 50
    file_id = (query, search(query))
    print(file_id[1])
    return render_template(
        'search.html',
        product_json = file_id[1],
        search_term=query,
    )

if __name__ == "__main__":
    app.run()