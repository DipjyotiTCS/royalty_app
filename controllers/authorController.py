
from models.author_model import AuthorData
from models.sales_data_model import SalesData
from models.author_model import AuthorAmountData
from database.db import get_db_connection
from flask import Blueprint, request, jsonify

author_bp = Blueprint("authorController", __name__, url_prefix="/author")

# API to fetch author data
@author_bp.route("/getAuthorDetails/<author_name>/<isbn>", methods=["GET"])
def getAuthorDetails(author_name: str, isbn: str):
    conn = get_db_connection()
    print(int(isbn))
    print(author_name)
    tabular_author_data = conn.execute("SELECT * FROM author_data WHERE isbn=? AND author=?", (int(isbn), author_name)).fetchone()
    conn.close()
    
    # Convert row to AuthorData object
    author_rate_data = AuthorData(
        title=tabular_author_data["title"],
        isbn=tabular_author_data["isbn"],
        author=tabular_author_data["author"],
        royalty_canada=tabular_author_data["royalty_canada"],
        royalty_chapter=tabular_author_data["royalty_chapter"],
        royalty_us=tabular_author_data["royalty_us"],
        royalty_foreign=tabular_author_data["royalty_foreign"],
        royalty_high_discount=tabular_author_data["royalty_high_discount"],
        royalty_state_adoption=tabular_author_data["royalty_state_adoption"],
        royalty_sub_us=tabular_author_data["royalty_sub_us"],
        royalty_sub_foreign=tabular_author_data["royalty_sub_foreign"],
        royalty_sub_trial=tabular_author_data["royalty_sub_trial"]
    )
    
    #Fetch data based on user and isbn
    conn = get_db_connection()
    tabular_sales_data = conn.execute("SELECT * FROM sales_data WHERE isbn=? AND author=?", (int(isbn), author_name)).fetchone()
    conn.close()
    
  # Convert row to SalesData object
    sales_data = SalesData(
        title=tabular_sales_data["title"],
        isbn=tabular_sales_data["isbn"],
        author=tabular_sales_data["author"],
        process_date=tabular_sales_data["process_date"],
        sales_total=tabular_sales_data["sales_total"],
        sales_canada=tabular_sales_data["sales_canada"],
        sales_chapter=tabular_sales_data["sales_chapter"],
        sales_us=tabular_sales_data["sales_us"],
        sales_foreign=tabular_sales_data["sales_foreign"],
        sales_high_discount=tabular_sales_data["sales_high_discount"],
        sales_state_adoption=tabular_sales_data["sales_state_adoption"],
        sales_sub_us=tabular_sales_data["sales_sub_us"],
        sales_sub_foreign=tabular_sales_data["sales_sub_foreign"],
        sales_sub_trial=tabular_sales_data["sales_sub_trial"]
    )
    
    canada_amount = (sales_data.sales_canada * author_rate_data.royalty_canada)/100
    chapter_amount = (sales_data.sales_chapter * author_rate_data.royalty_chapter)/100
    us_amount = (sales_data.sales_us * author_rate_data.royalty_us)/100
    foreign_amount = (sales_data.sales_foreign * author_rate_data.royalty_foreign)/100
    high_discount_amount = (sales_data.sales_high_discount * author_rate_data.royalty_high_discount)/100
    state_adoption_amount = (sales_data.sales_state_adoption * author_rate_data.royalty_state_adoption)/100
    sub_us_amount = (sales_data.sales_sub_us * author_rate_data.royalty_sub_us)/100
    sub_foreign_amount = (sales_data.sales_sub_foreign * author_rate_data.royalty_sub_foreign)/100
    sub_trail_amount = (sales_data.sales_sub_trial * author_rate_data.royalty_sub_trial)/100
    
    total = canada_amount+chapter_amount+us_amount+foreign_amount+high_discount_amount+state_adoption_amount+sub_us_amount+sub_foreign_amount+sub_trail_amount

    #Formulate and return the response
    author_amount = AuthorAmountData(title=sales_data.title, 
                    isbn=sales_data.isbn, 
                    author=sales_data.author, 
                    royalty_canada_amount=round(canada_amount, 3),
                    royalty_chapter_amount=round(chapter_amount, 3),
                    royalty_us_amount=round(us_amount, 3),
                    royalty_foreign_amount=round(foreign_amount, 3),
                    royalty_high_discount_amount=round(high_discount_amount, 3),
                    royalty_state_adoption_amount=round(state_adoption_amount, 3),
                    royalty_sub_us_amount=round(sub_us_amount, 3),
                    royalty_sub_foreign_amount=round(sub_foreign_amount, 3),
                    royalty_sub_trial_amount=round(sub_trail_amount, 3),
                    royalty_total_amount=round(total, 3),
                    royalty_canada = author_rate_data.royalty_canada,
                    royalty_chapter = author_rate_data.royalty_chapter,
                    royalty_us = author_rate_data.royalty_us,
                    royalty_foreign=author_rate_data.royalty_foreign,
                    royalty_high_discount=author_rate_data.royalty_high_discount,
                    royalty_state_adoption=author_rate_data.royalty_state_adoption,
                    royalty_sub_us=author_rate_data.royalty_sub_us,
                    royalty_sub_foreign=author_rate_data.royalty_sub_foreign,
                    royalty_sub_trial=author_rate_data.royalty_sub_trial,
                    sales_total=sales_data.sales_total,
                    sales_canada=sales_data.sales_canada,
                    sales_chapter=sales_data.sales_chapter,
                    sales_us=sales_data.sales_us,
                    sales_foreign=sales_data.sales_foreign,
                    sales_high_discount=sales_data.sales_high_discount,
                    sales_state_adoption=sales_data.sales_state_adoption,
                    sales_sub_us=sales_data.sales_sub_us,
                    sales_sub_foreign=sales_data.sales_sub_foreign,
                    sales_sub_trial=sales_data.sales_sub_trial)
    
    return jsonify(author_amount.model_dump())
    


# API to add new sales data
@author_bp.route("/getAuthorRoyaltyRate", methods=["GET"])
def addSalesData():
    conn = get_db_connection()
    tabular_author_data = conn.execute("SELECT * FROM author_data").fetchall()
    conn.close()
    return jsonify([dict(data) for data in tabular_author_data])


# API to update author rates data
@author_bp.route("/updateAuthorRates", methods=["POST"])
def updateAuthorRates():
    
    request_data = request.get_json() or {}
    author = request_data["author"]
    isbn = request_data["isbn"]
    rows = request_data["rows"]

    conn = get_db_connection()
    tabular_author_data = conn.execute("SELECT * FROM author_data WHERE author=? AND isbn=?", (author, int(isbn))).fetchone()

    author_current_rate_data = AuthorData(
        title = tabular_author_data["title"],
        isbn = tabular_author_data["isbn"],
        author = tabular_author_data["author"],
        royalty_canada = tabular_author_data["royalty_canada"],
        royalty_chapter = tabular_author_data["royalty_chapter"],
        royalty_us = tabular_author_data["royalty_us"],
        royalty_foreign = tabular_author_data["royalty_foreign"],
        royalty_high_discount = tabular_author_data["royalty_high_discount"],
        royalty_state_adoption = tabular_author_data["royalty_state_adoption"],
        royalty_sub_us = tabular_author_data["royalty_sub_us"],
        royalty_sub_foreign = tabular_author_data["royalty_sub_foreign"],
        royalty_sub_trial = tabular_author_data["royalty_sub_trial"]
    )

    for row in rows:
        if row["id"] == "us-domestic":
            author_current_rate_data.royalty_us = float(row["latestRate"])
        if row["id"] == "canadian":
            author_current_rate_data.royalty_canada = float(row["latestRate"])
        if row["id"] == "chapter-sales":
            author_current_rate_data.royalty_chapter = float(row["latestRate"])
        if row["id"] == "foreign":
            author_current_rate_data.royalty_foreign = float(row["latestRate"])
        if row["id"] == "high-discount":
            author_current_rate_data.royalty_high_discount = float(row["latestRate"])
        if row["id"] == "state-adoption":
            author_current_rate_data.royalty_state_adoption = float(row["latestRate"])
        if row["id"] == "subscription-trial":
            author_current_rate_data.royalty_sub_trial = float(row["latestRate"])
        if row["id"] == "subscription-domestic":
            author_current_rate_data.royalty_sub_us = float(row["latestRate"])
        if row["id"] == "subscription-foreign":
            author_current_rate_data.royalty_sub_foreign = float(row["latestRate"])    
                                    

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO author_data (
            title, isbn, author, royalty_canada, royalty_chapter,
            royalty_us, royalty_foreign, royalty_high_discount,
            royalty_state_adoption, royalty_sub_us, royalty_sub_foreign,
            royalty_sub_trial
        )
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
        (
            author_current_rate_data.title,
            author_current_rate_data.isbn,
            author_current_rate_data.author,
            author_current_rate_data.royalty_canada,
            author_current_rate_data.royalty_chapter,
            author_current_rate_data.royalty_us,
            author_current_rate_data.royalty_foreign,
            author_current_rate_data.royalty_high_discount,
            author_current_rate_data.royalty_state_adoption,
            author_current_rate_data.royalty_sub_us,
            author_current_rate_data.royalty_sub_foreign,
            author_current_rate_data.royalty_sub_trial
        )
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Sales data updated successfully"})




# API to update author rates data
@author_bp.route("/resetAuthorRates", methods=["POST"])
def resetAuthorRates():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO author_data (
            title, isbn, author, royalty_canada, royalty_chapter,
            royalty_us, royalty_foreign, royalty_high_discount,
            royalty_state_adoption, royalty_sub_us, royalty_sub_foreign,
            royalty_sub_trial
        )
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
        ("Reading Program", 1234567890123, "John Doe", 0.15, 0.1, 0.15, 0.15, 0.075, 0.15, 0.15, 0.15, 0)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Sales data updated successfully"})