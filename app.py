from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_cors import CORS


from controllers.calculatorController import calculator_bp
from controllers.authorController import author_bp
from controllers.wisdomnextRouterController import wisdomnext_bp
import sqlite3
# once you convert these to Flask blueprints (see below):
# from controllers.authorController import author_bp
# from controllers.WishdomnextRouterController import wishdom_bp

app = Flask(__name__, static_folder="dist/assets", static_url_path="/assets", template_folder="dist")

CORS(app)

app.register_blueprint(calculator_bp)
app.register_blueprint(author_bp)
app.register_blueprint(wisdomnext_bp)
# app.register_blueprint(wishdom_bp)


# Initialize DB tables if not exist
conn = sqlite3.connect("local_sales_db.sqlite")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS sales_data (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, isbn INTEGER, author TEXT, process_date TEXT, sales_total INTEGER, sales_canada INTEGER, sales_chapter INTEGER, sales_us INTEGER, sales_foreign INTEGER, sales_high_discount INTEGER, sales_state_adoption INTEGER, sales_sub_us INTEGER, sales_sub_foreign INTEGER, sales_sub_trial INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS author_data (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, isbn INTEGER, author TEXT, royalty_canada REAL, royalty_chapter REAL, royalty_us REAL, royalty_foreign REAL, royalty_high_discount REAL, royalty_state_adoption REAL, royalty_sub_us REAL, royalty_sub_foreign REAL, royalty_sub_trial REAL, UNIQUE(isbn, author))")
conn.commit()

# Insert a sample user if table is empty
cursor.execute("SELECT COUNT(*) FROM sales_data")
count = cursor.fetchone()[0]
if count == 0:
    cursor.execute("INSERT INTO sales_data (title, isbn, author, process_date, sales_total, sales_canada, sales_chapter, sales_us, sales_foreign, sales_high_discount, sales_state_adoption, sales_sub_us, sales_sub_foreign, sales_sub_trial) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ("Reading Program", 1234567890123, "John Doe", "23-Nov-2025​", 337500, 20000, 15000, 70000, 30000, 8000, 15000, 36000, 7000, 15000))
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM author_data")
count = cursor.fetchone()[0]
if count == 0:
    cursor.execute("""INSERT INTO author_data (title, isbn, author, royalty_canada, royalty_chapter, royalty_us, royalty_foreign, royalty_high_discount, royalty_state_adoption, royalty_sub_us, royalty_sub_foreign, royalty_sub_trial) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(isbn, author) DO UPDATE SET
                        title = excluded.title,
                        royalty_canada = excluded.royalty_canada,
                        royalty_chapter = excluded.royalty_chapter,
                        royalty_us = excluded.royalty_us,
                        royalty_foreign = excluded.royalty_foreign,
                        royalty_high_discount = excluded.royalty_high_discount,
                        royalty_state_adoption = excluded.royalty_state_adoption,
                        royalty_sub_us = excluded.royalty_sub_us,
                        royalty_sub_foreign = excluded.royalty_sub_foreign,
                        royalty_sub_trial = excluded.royalty_sub_trial
                   """, 
                   ("Reading Program", 1234567890123, "John Doe", 0.15, 0.1, 0.15, 0.15, 0.075, 0.15, 0.15, 0.15, 0))
    conn.commit()

conn.close()


@app.route("/")
def index():
    # Serve the pre-built SPA frontend
    return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory("dist", "favicon.ico")

@app.route("/robots.txt")
def robots():
    return send_from_directory("dist", "robots.txt")


# 🔹 Your new API route
@app.route("/getAuthorDetails/{author_name}/{isbn}", methods=["GET"])
def api_search():
    data = request.get_json() or {}
    query = data.get("query", "").strip()

    # TODO: replace this with your real logic
    # For demo, just echo something back
    results = [
        {"id": 1, "name": "Dummy result 1", "query": query},
        {"id": 2, "name": "Dummy result 2", "query": query},
    ]

    return jsonify({"results": results})

if __name__ == "__main__":
    # For local development only; in production use a proper WSGI server (gunicorn, uWSGI, etc.)
    app.run(host="0.0.0.0", port=5000, debug=True)
