# home/routes.py

import requests, os
from apps.home import blueprint
from flask import redirect, render_template, request, url_for, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.models import Customer, CustomerLoan, CreditScore, Survey, ModelData
from apps import db

@blueprint.route('/customers', methods=['GET', 'POST'])
@login_required
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

    # Base query: filter customers by search query, then join with model_data table
    base_query = Customer.query.join(
        ModelData, Customer.customer_id == ModelData.Customer_ID
    )

    # Filter customers based on the search query
    if search_query:
        customers = base_query.filter(
            db.or_(
                Customer.customer_id.ilike(f'%{search_query}%'),
                Customer.full_name.ilike(f'%{search_query}%')
            )
        ).paginate(page=page, per_page=per_page, error_out=False)
    else:
        customers = base_query.paginate(page=page, per_page=per_page, error_out=False)

    # Fetch credit scores for the current page of customers
    customer_ids = [customer.customer_id for customer in customers.items]
    credit_scores = CreditScore.query.filter(CreditScore.customer_id.in_(customer_ids)).all()

    # Create a dictionary mapping customer_id to credit_score
    credit_scores_dict = {score.customer_id: score.credit_score for score in credit_scores}

    return render_template('customers/index.html', customers=customers, credit_score=credit_scores_dict, segment='index')


@blueprint.route('/customers/<int:customer_id>')
@login_required
def customer_profile(customer_id):
    # Query the database to find the customer and their financial information
    customer = Customer.query.get_or_404(customer_id)
    survey = Survey.query.filter_by(customer_id=customer.customer_id).first()
    customer_loan = CustomerLoan.query.filter_by(customer_id=customer.customer_id).first()
    credit_score = CreditScore.query.filter_by(customer_id=customer.customer_id).first()

    model_data = ModelData.query.get_or_404(customer_id)

    data = {
        "Number_of_Children": float(model_data.Number_of_Children),
        "Monthly_Income": float(model_data.Monthly_Income),
        "Number_of_Loans": int(model_data.Number_of_Loans),
        "Full_Name_Fərdi - Fiziki şəxs - Rezident": bool(model_data.Full_Name_Ferdi_Fiziki_Shexs_Rezident),
        "Full_Name_Fərdi - Sahibkar - Rezident": bool(model_data.Full_Name_Ferdi_Sahibkar_Rezident),
        "Place_of_Birth_QIRĞIZISTAN": bool(model_data.Place_of_Birth_QIRGIZISTAN),
        "Place_of_Birth_RUSİYA FEDERASİYASI": bool(model_data.Place_of_Birth_RUSIYA_FEDERASIYASI),
        "Place_of_Birth_TACİKİSTAN": bool(model_data.Place_of_Birth_TACIKISTAN),
        "Place_of_Birth_TATARISTAN": bool(model_data.Place_of_Birth_TATARISTAN),
        "Place_of_Birth_TÜRKMƏNİSTAN": bool(model_data.Place_of_Birth_TURKMENISTAN),
        "Place_of_Birth_ÖZBƏKİSTAN": bool(model_data.Place_of_Birth_OZBEKISTAN),
        "Place_of_Birth_ƏFQANİSTAN": bool(model_data.Place_of_Birth_AFGANISTAN),
        "Age": float(model_data.Age),
        "Citizenship_TACİKİSTAN": bool(model_data.Citizenship_TACIKISTAN),
        "Gender_QADIN": bool(model_data.Gender_QADIN),
        "Marital_Status_DUL": bool(model_data.Marital_Status_DUL),
        "Marital_Status_EVLI": bool(model_data.Marital_Status_EVLI),
        "Marital_Status_SUBAY": bool(model_data.Marital_Status_SUBAY),
        "Occupation_HAYVANCILIK": bool(model_data.Occupation_HAYVANCILIK),
        "Occupation_HIZMETLER": bool(model_data.Occupation_HIZMETLER),
        "Occupation_MORTGAGES": bool(model_data.Occupation_MORTGAGES),
        "Occupation_TARIM": bool(model_data.Occupation_TARIM),
        "Occupation_TICARET": bool(model_data.Occupation_TICARET),
        "Occupation_URETIM": bool(model_data.Occupation_URETIM),
        "Log_Monthly_Income": float(model_data.Log_Monthly_Income),
        "Education_Level_Higher Education": bool(model_data.Education_Level_Higher_Education),
        "Education_Level_Incomplete Secondary Education": bool(model_data.Education_Level_Incomplete_Secondary_Education),
        "Education_Level_Other Education": bool(model_data.Education_Level_Other_Education),
        "Education_Level_Secondary Education": bool(model_data.Education_Level_Secondary_Education),
        "Education_Level_Secondary Education with Specialisation": bool(model_data.Education_Level_Secondary_Education_with_Specialisation),
        "Total_Loan_Amount": float(model_data.Total_Loan_Amount),
        "Average_Loan_Amount": float(model_data.Average_Loan_Amount),
        "Loan_Amount_Range": float(model_data.Loan_Amount_Range),
        "Average_Credit_Duration": float(model_data.Average_Credit_Duration),
        "Total_Credit_Duration": int(model_data.Total_Credit_Duration),
        "Product_Type_BİZNES KREDİTLƏRİ": int(model_data.Product_Type_BIZNES_KREDITLERI),
        "Product_Type_PARTNYORLUQ KREDİTLƏERİ": int(model_data.Product_Type_PARTNYORLUQ_KREDITLERI),
        "Product_Type_İSTEHLAK": int(model_data.Product_Type_ISTEHLAK),
        "Product_Type_Ə.H. LAYİHƏLƏRİ": int(model_data.Product_Type_AH_LAYIHELARI),
        "Total_Debt": float(model_data.Total_Debt),
        "Debt_Income_Ratio": float(model_data.Debt_Income_Ratio),
        "Number_of_Family_Members": int(model_data.Number_of_Family_Members),
        "Is_Politician_Hayir": bool(model_data.Is_Politician_Hayir),
        "Has_Political_Affiliation_Hayir": bool(model_data.Has_Political_Affiliation_Hayir),
        "Account_Purpose_SBER HESAP": bool(model_data.Account_Purpose_SBER_HESAP),
        "Account_Purpose_TASARRUF HESABI": bool(model_data.Account_Purpose_TASARRUF_HESABI),
        "Account_Purpose_ULUSLARARASI PARA TRANSFERI": bool(model_data.Account_Purpose_ULUSLARARASI_PARA_TRANSFERI),
        "Account_Purpose_YURTICI HAVALE": bool(model_data.Account_Purpose_YURTICI_HAVALE),
        "Has_Collateral_Hayir": bool(model_data.Has_Collateral_Hayir),
        "Owns_Valuable_Items_Hayir": bool(model_data.Owns_Valuable_Items_Hayir),
        "Owns_Real_Estate_Hayir": bool(model_data.Owns_Real_Estate_Hayir),
        "Loan_Purpose_ISLETME SERMAYESI": bool(model_data.Loan_Purpose_ISLETME_SERMAYESI),
        "Loan_Purpose_MULK ALIMI": bool(model_data.Loan_Purpose_MULK_ALIMI),
        "Loan_Purpose_SABIT VARLIKLAR": bool(model_data.Loan_Purpose_SABIT_VARLIKLAR),
        "Loan_Purpose_TADILAT": bool(model_data.Loan_Purpose_TADILAT),
        "Loan_Purpose_TARIM": bool(model_data.Loan_Purpose_TARIM),
        "Income_Type_DIGER": bool(model_data.Income_Type_DIGER),
        "Income_Type_EK IS": bool(model_data.Income_Type_EK_IS),
        "Income_Type_HAVALE": bool(model_data.Income_Type_HAVALE),
        "Income_Type_KIRA GELIRI": bool(model_data.Income_Type_KIRA_GELIRI),
        "Negative_Comment_from_Loan_Department_Hayir": bool(model_data.Negative_Comment_from_Loan_Department_Hayir),
        "Job_Position_Diger": bool(model_data.Job_Position_Diger),
        "Job_Position_Ozel Sektor": bool(model_data.Job_Position_Ozel_Sektor),
        "Job_Position_Ozel Sektor/Teknik": bool(model_data.Job_Position_Ozel_Sektor_Teknik),
        "Job_Position_Sirket Sahibi": bool(model_data.Job_Position_Sirket_Sahibi),
        "Job_Position_Yonetici": bool(model_data.Job_Position_Yonetici),
        "Is_Customer_on_Banned_List_Hayir": bool(model_data.Is_Customer_on_Banned_List_Hayir),
        "Is_Regular_Customer_Evet": bool(model_data.Is_Regular_Customer_Evet),
        "Annual_Account_Activity_Range_100.000-500.000": bool(model_data.Annual_Account_Activity_Range_100000_500000),
        "Annual_Account_Activity_Range_30.000-100.000": bool(model_data.Annual_Account_Activity_Range_30000_100000),
        "Annual_Account_Activity_Range_500.000-99999999999": bool(model_data.Annual_Account_Activity_Range_500000_99999999999),
        "Annual_Account_Activity_Range_Diğer": bool(model_data.Annual_Account_Activity_Range_Diger)
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
