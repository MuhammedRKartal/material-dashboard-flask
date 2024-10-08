# home/models.py

from apps import db

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    place_of_birth = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    citizenship = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    number_of_children = db.Column(db.Integer, nullable=False)
    marital_status = db.Column(db.String(50), nullable=False)
    occupation = db.Column(db.String(255), nullable=False)
    customer_registration_date = db.Column(db.DateTime, nullable=False)
    monthly_income = db.Column(db.Numeric(15, 2), nullable=False)
    education_level = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    number_of_loans = db.Column(db.Integer, nullable=False)

    # Relationships
    credit_scores = db.relationship('CreditScore', backref='customer', lazy=True)
    customer_loans = db.relationship('CustomerLoan', backref='customer', lazy=True)
    surveys = db.relationship('Survey', backref='customer', lazy=True)


class CreditScore(db.Model):
    __tablename__ = 'credit_scores'
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False, primary_key=True)
    credit_score = db.Column(db.Integer, nullable=False)


class CustomerLoan(db.Model):
    __tablename__ = 'customer_loans'
    document_id = db.Column(db.String(50), primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    product_type = db.Column(db.String(100), nullable=False)
    loan_type = db.Column(db.String(100), nullable=False)
    currency_type = db.Column(db.String(10), nullable=False)
    loan_start_date = db.Column(db.DateTime, nullable=False)
    loan_end_date = db.Column(db.DateTime, nullable=False)
    loan_status = db.Column(db.String(50), nullable=False)
    requested_amount = db.Column(db.Numeric(15, 2), nullable=False)
    approved_amount = db.Column(db.Numeric(15, 2), nullable=False)
    principal_debt = db.Column(db.Numeric(15, 2), nullable=False)
    total_debt = db.Column(db.Numeric(15, 2), nullable=False)
    secondary_purpose_code = db.Column(db.String(50), nullable=True)
    secondary_purpose_description = db.Column(db.String(255), nullable=True)
    tertiary_purpose_code = db.Column(db.String(50), nullable=True)
    tertiary_purpose_description = db.Column(db.String(255), nullable=True)


class Survey(db.Model):
    __tablename__ = 'surveys'
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False, primary_key=True)
    country_of_residence = db.Column(db.String(100), nullable=False)
    citizenship = db.Column(db.String(100), nullable=False)
    is_politician = db.Column(db.String(10), nullable=False)
    has_political_affiliation = db.Column(db.String(10), nullable=False)
    account_purpose = db.Column(db.String(255), nullable=False)
    annual_account_activity_range = db.Column(db.String(50), nullable=False)
    current_account_local_currency_balance = db.Column(db.String(50), nullable=False)
    number_of_current_accounts = db.Column(db.String(50), nullable=False)
    savings_account_local_currency_balance = db.Column(db.String(50), nullable=False)
    number_of_savings_accounts = db.Column(db.String(50), nullable=False)
    investment_account_local_currency_balance = db.Column(db.String(50), nullable=False)
    number_of_investment_accounts = db.Column(db.String(50), nullable=False)
    authorized_signatory_country_of_residence = db.Column(db.String(100), nullable=True)
    authorized_signatory_citizenship = db.Column(db.String(100), nullable=True)
    company_partner_citizenship = db.Column(db.String(100), nullable=True)
    number_of_family_members = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    marital_status = db.Column(db.String(50), nullable=False)
    education_level = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    additional_income = db.Column(db.Float, nullable=True)
    has_collateral = db.Column(db.String(10), nullable=False)
    owns_valuable_items = db.Column(db.String(10), nullable=False)
    owns_real_estate = db.Column(db.String(10), nullable=False)
    loan_purpose = db.Column(db.String(255), nullable=False)
    loan_branch = db.Column(db.String(100), nullable=False)
    number_of_loans = db.Column(db.Integer, nullable=False)
    loan_month = db.Column(db.String(50), nullable=False)
    primary_income_percentage = db.Column(db.String(20), nullable=False)
    income_type = db.Column(db.String(100), nullable=False)
    expense_to_income_ratio = db.Column(db.Float, nullable=False)
    negative_comment_from_loan_department = db.Column(db.String(10), nullable=False)
    years_of_employment = db.Column(db.String(50), nullable=False)
    years_in_same_residence = db.Column(db.Integer, nullable=False)
    job_position = db.Column(db.String(255), nullable=False)
    movable_property_value_in_usd = db.Column(db.Numeric(15, 2), nullable=False)
    immovable_property_value_land_in_usd = db.Column(db.Numeric(15, 2), nullable=False)
    second_property_value_in_usd = db.Column(db.Numeric(15, 2), nullable=False)
    immovable_property_value_house_in_usd = db.Column(db.Numeric(15, 2), nullable=False)
    is_customer_on_banned_list = db.Column(db.String(10), nullable=False)
    is_regular_customer = db.Column(db.String(10), nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
