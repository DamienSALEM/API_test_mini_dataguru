"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

import flask
from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/')
def home():
    """Renders a home page."""
    return '''<h1>Test API mini dataguru</h1>
   <p> prototype API for manupulating data using flask and sqlite.</p>'''


@app.route('/images/tshirts/all', methods=['GET'])
def api_all():
    """
    It connects to the database, creates a cursor, executes a query, and returns the results as a JSON
    object
    :return: The function api_all() returns a jsonified version of all the tshirts in the database.
    """
    # Requête GET pour la lecture de toute la table tshirts de la base.
    conn = sqlite3.connect('images.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_tshirts = cur.execute('SELECT * FROM tshirts').fetchall()
    conn.close()
    return jsonify(all_tshirts)


@app.route('/images/tshirts/filters', methods=['GET'])
def api_filters():
    """
    It takes the query parameters from the URL, and if they exist, it adds them to the query. If they
    don't exist, it returns all the results
    :return: The results of the query
    """
    # Requête GET pour de la lecture de la base de donnée avec filtres
    query_parameters = request.args
    id = query_parameters.get('id')
    name = query_parameters.get('name')
    type = query_parameters.get('type')
    url = query_parameters.get('url')
    query = "SELECT * FROM tshirts WHERE "
    to_filter = []
    if id:
        query += 'id=? AND '
        to_filter.append(id)
    if name:
        query += 'name=? AND '
        to_filter.append(name)
    if type:
        query += 'type=? AND '
        to_filter.append(type)
    if url:
        query += 'url=? AND '
        to_filter.append(url)
    if not (id or name or type or url):
        return api_all()
    query = query[:-4]+';'
    conn = sqlite3.connect('images.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()
    conn.close()
    return jsonify(results)


@app.route('/images/tshirts', methods=['POST'])
def api_insert():
    """
    It inserts a new row into the tshirts table.
    :return: The values are being returned as a json object.
    """
    # Requête en POST par un json pour faire un INSERT dans la table tshirts
    request_data = request.get_json()
    name = request_data['tshirt_name']
    type = request_data['type']
    url = request_data['url']
    query = 'INSERT into tshirts ("tshirt_name","type","url") VALUES (?,?,?)'
    values = [name, type, url]
    conn = sqlite3.connect('images.db')
    cur = conn.cursor()
    results = cur.execute(query, values)
    conn.commit()
    conn.close()
    return jsonify(values)


@app.route('/images/tags', methods=['POST'])
def api_tags_create():
    """
    It takes a JSON object from a POST request, and inserts it into the database
    :return: The name of the tag
    """
    # Requête en POST par un json pour faire un insert dans la table tags
    request_data = request.get_json()
    name = request_data['tag-name']
    query = 'INSERT into tags ("tag_name") VALUES (?)'
    conn = sqlite3.connect('images.db')
    cur = conn.cursor()
    results = cur.execute(query, name)
    conn.commit()
    conn.close()
    return jsonify(name)


@app.route('/images/tags/all', methods=['GET'])
def api_tags_all():
    """
    It connects to the database, gets all the tags, and returns them as a JSON object
    :return: A JSON object containing all the tags in the database.
    """
    # Requête en GET pour récupérer tous les tags
    conn = sqlite3.connect('images.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_tags = cur.execute('SELECT * FROM tags').fetchall()
    conn.close()
    return jsonify(all_tags)


@app.route('/images/tshirts/tags', methods=['POST'])
def api_tshirt_tag():
    """
    It takes a POST request with a JSON object containing two keys, id_tag and id_tshirt, and inserts
    the values into the lien_tshirt_tag table
    :return: The return value is a string.
    """
    # Requête en POST pour ajouter un tag à une image
    request_data = request.get_json()
    id_tag = request_data['id_tag']
    id_tshirt = request_data['id_tshirt']
    query = 'INSERT into lien_tshirt_tag ("id_tshirt",id_tag") VALUES (?,?)'
    ids = [id_tshirt, id_tag]
    conn = sqlite3.connect('images.db')
    cur = conn.cursor()
    cur.execute(query, ids)
    conn.commit()
    conn.close()
    return '<p>Requête validée<p>'


@app.route('/images/tshirts/<int:id_tshirt>/tags')
def api_filter_tag(id_tshirt):
    """
    It takes the id of a t-shirt and returns a list of all the tags associated with that t-shirt

    :param id_tshirt: the id of the t-shirt
    :return: A list of dictionaries.
    """
    # Requête en GET pour obtenir tous les tags d'une image
    conn = sqlite3.connect('images.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    tshirt_tag = cur.execute(
        'SELECT tag_name FROM lien_tshirt_tag INNER JOIN tags on tags.ID=lien_tshirt_tag.id_tag WHERE id_tshirt=?', id_tshirt).fetchall()
    conn.close()
    return jsonify(tshirt_tag)


@app.route('/images/tshirts/tags/all')
def api_tshirt_tag_all():
    """
    It returns a jsonified list of dictionaries, each dictionary containing the name, type and url of a
    tshirt that has at least one tag.
    :return: A list of dictionaries.
    """
    # Requête en GET pour obtenir toutes les images qui ont au moins un tag
    conn = sqlite3.connect('images.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_tshirts_tags = cur.execute(
        'SELECT DISTINCT tshirt_name, type, url FROM tshirts INNER JOIN lien_tshirt_tag on lien_tshirt_tag.id_tshirt=tshirts.ID').fetchall()
    conn.close()
    return jsonify(all_tshirts_tags)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
