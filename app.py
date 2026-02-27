from decimal import Decimal, InvalidOperation
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    form_data = {
        'base_salary': request.form.get('base_salary', '').strip(),
        'commute': request.form.get('commute', '').strip(),
        'lunch_percent': request.form.get('lunch_percent', '').strip(),
        'new_clothes': request.form.get('new_clothes') == 'on',
    }
    errors = {}

    base_salary = None
    base_salary_raw = form_data['base_salary']
    if not base_salary_raw.isdigit():
        errors['base_salary'] = "Salary must be a whole number."
    else:
        base_salary = int(base_salary_raw)
        if base_salary < 0 or base_salary > 999999:
            errors['base_salary'] = "Salary must be between 0 and 999,999."

    commute = None
    commute_raw = form_data['commute']
    try:
        commute = Decimal(commute_raw)
        if commute < 0 or commute > Decimal("500"):
            errors['commute'] = "Commute distance must be between 0 and 500."
    except (InvalidOperation, ValueError):
        errors['commute'] = "Commute distance must be a number."

    lunch_percent = None
    lunch_percent_raw = form_data['lunch_percent']
    try:
        lunch_percent = Decimal(lunch_percent_raw)
        if lunch_percent < 0 or lunch_percent > 1:
            errors['lunch_percent'] = "Lunch percentage must be between 0 and 1."
    except (InvalidOperation, ValueError):
        errors['lunch_percent'] = "Lunch percentage must be a number between 0 and 1."

    if errors:
        return render_template('index.html', errors=errors, form_data=form_data)

    no_new_clothes_cost = form_data['new_clothes']


    # Calculations
    commute_cost = float(((commute * Decimal("2")) * Decimal("0.58")) * Decimal("261"))
    lunch_cost = float(Decimal("10") * Decimal("261") * lunch_percent)
    if no_new_clothes_cost:
        apparel_cost = 0
    else:
        apparel_cost = 1754
    total_salary = commute_cost + base_salary + lunch_cost + apparel_cost
    total_salary_display = f"{total_salary:,.2f}"
    breakdown = {
        'base_salary': f"{base_salary:,.2f}",
        'commute_cost': f"{commute_cost:,.2f}",
        'lunch_cost': f"{lunch_cost:,.2f}",
        'apparel_cost': f"{apparel_cost:,.2f}",
    }

    return render_template(
        'result.html',
        total_salary_display=total_salary_display,
        breakdown=breakdown,
    )


if __name__ == '__main__':
    app.run(debug=True)
