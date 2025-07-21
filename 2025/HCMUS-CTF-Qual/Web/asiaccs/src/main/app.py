import flask
import sqlite3

app = flask.Flask(__name__)

def query_by_author(name):
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT p.title, a.name, pa.affiliation
            FROM paper p
            JOIN paper_author pa ON p.id = pa.paper_id
            JOIN author a ON a.id = pa.author_id
            WHERE a.name LIKE ?
        """, (f"%{name}%",))
        return cur.fetchall()

def query_by_affiliation(affiliation):
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT p.title, a.name, pa.affiliation
            FROM paper p
            JOIN paper_author pa ON p.id = pa.paper_id
            JOIN author a ON a.id = pa.author_id
            WHERE pa.affiliation LIKE '%{affiliation}%'
        """)
        return cur.fetchall()

@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route('/api/search_by_author', methods=['POST'])
def search_by_author():
    req = flask.request.get_json()
    if 'name' not in req:
        flask.abort(400, "Missing author name")

    name = req['name']
    results = query_by_author(name)
    if not results:
        flask.abort(404, "No matching authors")

    return {"results": [{"title": r[0], "author": r[1], "affiliation": r[2]} for r in results]}

@app.route('/api/search_by_affiliation', methods=['POST'])
def search_by_affiliation():
    req = flask.request.get_json()
    if 'affiliation' not in req:
        flask.abort(400, "Missing affiliation name")

    aff = req['affiliation']
    results = query_by_affiliation(aff)
    if not results:
        flask.abort(404, "No matching affiliation")

    return {"results": [{"title": r[0], "author": r[1], "affiliation": r[2]} for r in results]}

if __name__ == '__main__':
    app.run()
