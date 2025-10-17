from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

final_report = pd.read_csv('finaldatareport.csv')
summary_report = pd.read_csv('Summaryfinalreport.csv')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.json["message"]
    company_input = request.json.get("company", "Microsoft")
    fiscal_year = request.json.get("year", 2023)

    response = financial_chatbot(user_query, company_input, fiscal_year)
    return jsonify({"reply": response})

def financial_chatbot(user_query, company_input, fiscal_year):
    user_query = user_query.lower()

    try:
        if "total revenue" in user_query:
            revenue = final_report[(final_report['Year'] == fiscal_year) &
                                   (final_report['Company'].str.lower() == company_input.lower())]['Total Revenue'].values[0]
            return f"The total revenue for {company_input} in {fiscal_year} is ${revenue:,}"

        elif "net income" in user_query:
            net_income = final_report[(final_report['Year'] == fiscal_year) &
                                      (final_report['Company'].str.lower() == company_input.lower())]['Net Income'].values[0]
            return f"The net income for {company_input} in {fiscal_year} is ${net_income:,}"

        elif "assets" in user_query:
            assets = final_report[(final_report['Year'] == fiscal_year) &
                                  (final_report['Company'].str.lower() == company_input.lower())]['Total Assets'].values[0]
            return f"The total assets for {company_input} in {fiscal_year} are ${assets:,}"

        elif "liabilities" in user_query:
            liabilities = final_report[(final_report['Year'] == fiscal_year) &
                                       (final_report['Company'].str.lower() == company_input.lower())]['Total Liabilities'].values[0]
            return f"The total liabilities for {company_input} in {fiscal_year} are ${liabilities:,}"

        elif "cash flow" in user_query:
            cash_flow = final_report[(final_report['Year'] == fiscal_year) &
                                     (final_report['Company'].str.lower() == company_input.lower())]['Cash Flow from Operating Activities'].values[0]
            return f"The cash flow from operating activities for {company_input} in {fiscal_year} is ${cash_flow:,}"

        else:
            return "Sorry, I can only provide predefined financial information such as revenue, net income, assets, or cash flow."

    except IndexError:
        return f"No data found for {company_input} in {fiscal_year}."

if __name__ == "__main__":
    app.run(debug=True)