from flask import Flask, render_template, request

from backend.search import search

app = Flask(__name__)


@app.route('/')
@app.route('/search', methods=['GET', 'POST'])
def search_single_product():
    """
    Execute a search for a specific search term.

    Return the top 50 results.
    """
    query = request.args.get('search')
    num_results = 50
    file_id = (query, search(query))
    return render_template(
        'index.html',
        product_json= file_id[1],
        search_term=query,
    )
