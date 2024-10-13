# home/routes.py

import requests, os
from apps.home import blueprint
from flask import redirect, render_template, request, url_for, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.models import Customer, CustomerLoan, CreditScore, Survey
from apps import db

@blueprint.route('/customers', methods=['GET', 'POST'])
def index():
    # Get the search query from the form (POST request)
    if request.method == 'POST':
        search_query = request.form.get('search', '').lower()
        return redirect(url_for('home_blueprint.index', search=search_query))
    
    # Get the search query from the URL parameters (GET request)
    search_query = request.args.get('search', '').lower()

    # Get the current page number from the URL parameters, default to page 1
    page = request.args.get('page', 1, type=int)

    # Set the maximum number of customers per page
    per_page = 30

    # Filter customers based on the search query
    if search_query:
        customers = Customer.query.filter(
            db.or_(
                Customer.customer_id.ilike(f'%{search_query}%'),
                Customer.full_name.ilike(f'%{search_query}%')
            )
        ).paginate(page=page, per_page=per_page, error_out=False)
    else:
        customers = Customer.query.paginate(page=page, per_page=per_page, error_out=False)

    # Fetch credit scores for the current page of customers
    customer_ids = [customer.customer_id for customer in customers.items]
    credit_scores = CreditScore.query.filter(CreditScore.customer_id.in_(customer_ids)).all()

    # Create a dictionary mapping customer_id to credit_score
    credit_scores_dict = {score.customer_id: score.credit_score for score in credit_scores}

    return render_template('customers/index.html', customers=customers, credit_score=credit_scores_dict, segment='index')

@blueprint.route('/customers/<int:customer_id>')
def customer_profile(customer_id):
    # Query the database to find the customer and their financial information
    customer = Customer.query.get_or_404(customer_id)
    survey = Survey.query.filter_by(customer_id=customer.customer_id).first()
    customer_loan = CustomerLoan.query.filter_by(customer_id=customer.customer_id).first()
    credit_score = CreditScore.query.filter_by(customer_id=customer.customer_id).first()

    data = {
        "Number_of_Children": 1.0,
        "Monthly_Income": 4000.0,
        "Number_of_Loans": 1,
        "Full_Name_Fərdi - Fiziki şəxs - Rezident": True,
        "Full_Name_Fərdi - Sahibkar - Rezident": False,
        "Place_of_Birth_QIRĞIZISTAN": False,
        "Place_of_Birth_RUSİYA FEDERASİYASI": False,
        "Place_of_Birth_TACİKİSTAN": False,
        "Place_of_Birth_TATARISTAN": False,
        "Place_of_Birth_TÜRKMƏNİSTAN": False,
        "Place_of_Birth_ÖZBƏKİSTAN": True,
        "Place_of_Birth_ƏFQANİSTAN": False,
        "Age": 49.0,
        "Citizenship_TACİKİSTAN": True,
        "Gender_QADIN": True,
        "Marital_Status_DUL": False,
        "Marital_Status_EVLI": True,
        "Marital_Status_SUBAY": False,
        "Occupation_HAYVANCILIK": False,
        "Occupation_HIZMETLER": False,
        "Occupation_MORTGAGES": False,
        "Occupation_TARIM": False,
        "Occupation_TICARET": False,
        "Occupation_URETIM": False,
        "Log_Monthly_Income": 8.294049640102028,
        "Education_Level_Higher Education": True,
        "Education_Level_Incomplete Secondary Education": False,
        "Education_Level_Other Education": False,
        "Education_Level_Secondary Education": False,
        "Education_Level_Secondary Education with Specialisation": False,
        "Total_Loan_Amount": 10000.0,
        "Average_Loan_Amount": 10000.0,
        "Loan_Amount_Range": 0.0,
        "Average_Credit_Duration": 548.0,
        "Total_Credit_Duration": 548,
        "Product_Type_BİZNES KREDİTLƏRİ": 0,
        "Product_Type_PARTNYORLUQ KREDİTLƏERİ": 0,
        "Product_Type_İSTEHLAK": 1,
        "Product_Type_Ə.H. LAYİHƏLƏRİ": 0,
        "Total_Debt": 12.3,
        "Debt_Income_Ratio": 0.0,
        "Number_of_Family_Members": 4,
        "Is_Politician_Hayir": True,
        "Has_Political_Affiliation_Hayir": True,
        "Account_Purpose_SBER HESAP": False,
        "Account_Purpose_TASARRUF HESABI": False,
        "Account_Purpose_ULUSLARARASI PARA TRANSFERI": False,
        "Account_Purpose_YURTICI HAVALE": False,
        "Has_Collateral_Hayir": True,
        "Owns_Valuable_Items_Hayir": True,
        "Owns_Real_Estate_Hayir": True,
        "Loan_Purpose_ISLETME SERMAYESI": False,
        "Loan_Purpose_MULK ALIMI": False,
        "Loan_Purpose_SABIT VARLIKLAR": False,
        "Loan_Purpose_TADILAT": False,
        "Loan_Purpose_TARIM": False,
        "Income_Type_DIGER": True,
        "Income_Type_EK IS": False,
        "Income_Type_HAVALE": False,
        "Income_Type_KIRA GELIRI": False,
        "Negative_Comment_from_Loan_Department_Hayir": True,
        "Job_Position_Diger": False,
        "Job_Position_Ozel Sektor": False,
        "Job_Position_Ozel Sektor/Teknik": False,
        "Job_Position_Sirket Sahibi": True,
        "Job_Position_Yonetici": False,
        "Is_Customer_on_Banned_List_Hayir": True,
        "Is_Regular_Customer_Evet": True,
        "Annual_Account_Activity_Range_100.000-500.000": False,
        "Annual_Account_Activity_Range_30.000-100.000": False,
        "Annual_Account_Activity_Range_500.000-99999999999": False,
        "Annual_Account_Activity_Range_Diğer": False
    }

    url = os.getenv('API_ROUTE_MODEL', None)
    headers = {
        "x-api-key": os.getenv('API_KEY', None),
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        api_response = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


    return render_template('customers/customer_profile.html', customer=customer, survey=survey, customer_loan=customer_loan, credit_score=credit_score, api_response=api_response)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'
        segment = get_segment(request)
        return render_template("home/" + template, segment=segment)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except:
        return render_template('home/page-500.html'), 500

def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
