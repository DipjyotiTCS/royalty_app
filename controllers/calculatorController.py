from models.request_model import Request
from models.response_model import Response
from models.sales_data_model import SalesData
from database.db import get_db_connection
from flask import Blueprint, request, jsonify

calculator_bp = Blueprint("calculatorController", __name__, url_prefix="/sales")

#API to perform calculation

@calculator_bp.route("/calculate", methods=["POST"])
def calculateSales():
    request_json = request.get_json() or {}
    print(request_json)
    request_data = Request(**request_json)
    #Fetch data based on user and isbn
    conn = get_db_connection()
    tabular_sales_data = conn.execute("SELECT * FROM sales_data WHERE isbn=? AND author=?", (request_data.isbn, request_data.author)).fetchone()
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
    
    #Perform calculation
    canada_old_amount = sales_data.sales_canada * request_data.royalty_table_canada
    canada_new_amount = sales_data.sales_canada * request_data.royalty_latest_canada
    canada_diff = 0 if canada_old_amount == canada_new_amount else (canada_new_amount - canada_old_amount)
    
    chapter_old_amount = sales_data.sales_chapter * request_data.royalty_table_chapter
    chapter_new_amount = sales_data.sales_chapter * request_data.royalty_latest_chapter
    chapter_diff = 0 if chapter_old_amount == chapter_new_amount else (chapter_new_amount - chapter_old_amount)
    
    us_old_amount = sales_data.sales_us * request_data.royalty_table_us
    us_new_amount = sales_data.sales_us * request_data.royalty_latest_us
    us_diff = 0 if us_old_amount == us_new_amount else (us_new_amount - us_old_amount)
    
    foreign_old_amount = sales_data.sales_foreign * request_data.royalty_table_foreign
    foreign_new_amount = sales_data.sales_foreign * request_data.royalty_latest_foreign
    foreign_diff = 0 if foreign_old_amount == foreign_new_amount else (foreign_new_amount - foreign_old_amount)
    
    
    highDiscout_old_amount = sales_data.sales_high_discount * request_data.royalty_table_high_discount
    highDiscout_new_amount = sales_data.sales_high_discount * request_data.royalty_latest_high_discount
    highDiscout_diff = 0 if highDiscout_old_amount == highDiscout_new_amount else (highDiscout_new_amount - highDiscout_old_amount)
    
    
    stateAdoption_old_amount = sales_data.sales_state_adoption * request_data.royalty_table_state_adoption
    stateAdoption_new_amount = sales_data.sales_state_adoption * request_data.royalty_latest_state_adoption
    stateAdoption_diff = 0 if stateAdoption_old_amount == stateAdoption_new_amount else (stateAdoption_new_amount - stateAdoption_old_amount)
    
    subUs_old_amount = sales_data.sales_sub_us * request_data.royalty_table_sub_us
    subUs_new_amount = sales_data.sales_sub_us * request_data.royalty_latest_sub_us
    subUs_diff = 0 if subUs_old_amount == subUs_new_amount else (subUs_new_amount - subUs_old_amount)
    
    subForeign_old_amount = sales_data.sales_sub_foreign * request_data.royalty_table_sub_foreign
    subForeign_new_amount = sales_data.sales_sub_foreign * request_data.royalty_latest_sub_foreign
    subForeign_diff = 0 if subForeign_old_amount == subForeign_new_amount else (subForeign_new_amount - subForeign_old_amount)
    
    subTrial_old_amount = sales_data.sales_sub_trial * request_data.royalty_table_sub_trial
    subTrial_new_amount = sales_data.sales_sub_trial * request_data.royalty_latest_sub_trial
    subTrial_diff = 0 if subTrial_old_amount == subTrial_new_amount else (subTrial_new_amount - subTrial_old_amount)
    
    total_db = canada_old_amount+chapter_old_amount+us_old_amount+foreign_old_amount+highDiscout_old_amount+stateAdoption_old_amount+subUs_old_amount+subForeign_old_amount+subTrial_old_amount
    
    total_new = canada_new_amount+us_new_amount+chapter_new_amount+foreign_new_amount+highDiscout_new_amount+stateAdoption_new_amount+subUs_new_amount+subForeign_new_amount+subTrial_new_amount
    
    total_diff = canada_diff+chapter_diff+us_diff+foreign_diff+highDiscout_diff+stateAdoption_diff+subUs_diff+subForeign_diff+subTrial_diff

    #Formulate and return the response
    response_data = Response(title=request_data.title, 
                    isbn=request_data.isbn, 
                    author=request_data.author, 
                    process_date=request_data.process_date,
                    royalty_canada_amount=canada_new_amount,
                    royalty_canada_discr=canada_diff,
                    royalty_chapter_amount=chapter_new_amount,
                    royalty_chapter_discr=chapter_diff,
                    royalty_us_amount=us_new_amount,
                    royalty_us_discr=us_diff,
                    royalty_foreign_amount=foreign_new_amount,
                    royalty_foreign_discr=foreign_diff,
                    royalty_high_discount_amount=highDiscout_new_amount,
                    royalty_high_discount_discr=highDiscout_diff,
                    royalty_state_adoption_amount=stateAdoption_new_amount,
                    royalty_state_adoption_discr=stateAdoption_diff,
                    royalty_sub_us_amount=subUs_new_amount,
                    royalty_sub_us_discr=subUs_diff,
                    royalty_sub_foreign_amount=subForeign_new_amount,
                    royalty_sub_foreign_discr=subForeign_diff,
                    royalty_sub_trial_amount=subTrial_new_amount,
                    royalty_sub_trial_discr=subTrial_diff,
                    royalty_total_DB=total_db,
                    royalty_total_latest=total_new,
                    royalty_total_disc=total_diff,
                    royalty_rate_us_response=request_data.royalty_rate_us_response,
                    royalty_rate_high_disc_response=request_data.royalty_rate_high_disc_response,
                    royalty_rate_sub_response=request_data.royalty_rate_sub_response,
                    royalty_rate_canada_response=request_data.royalty_rate_canada_response,
                    royalty_rate_chapter_response=request_data.royalty_rate_chapter_response,
                    royalty_us_discr_response=request_data.royalty_us_discr_response,
                    royalty_rate_foreign_response=request_data.royalty_rate_foreign_response,
                    royalty_rate_state_adoptions_response=request_data.royalty_rate_state_adoptions_response,
                    royalty_rate_sub_us_response=request_data.royalty_rate_sub_us_response,
                    royalty_rate_sub_foreign_response=request_data.royalty_rate_sub_foreign_response,
                    royalty_rate_sub_trial_response=request_data.royalty_rate_sub_trial_response)
    return jsonify(response_data.model_dump())