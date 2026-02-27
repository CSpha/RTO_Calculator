from decimal import Decimal, InvalidOperation
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    error = None
    try:
        base_salary_raw = request.form.get('base_salary', '').strip()
        if not base_salary_raw.isdigit():
            raise ValueError("Invalid salary. Salary must be a whole number.")
        base_salary = int(base_salary_raw)
        if base_salary < 0 or base_salary > 999999:
            raise ValueError("Invalid salary. Salary must be between 0 and 999,999.")

        commute_raw = request.form.get('commute', '').strip()
        try:
            commute = Decimal(commute_raw)
        except (InvalidOperation, ValueError):
            raise ValueError("Invalid commute distance entered. Please enter a number.")
        if commute < 0 or commute > Decimal("500"):
            raise ValueError("Invalid commute distance entered. It must be between 0 and 500.")

        lunch_percent_raw = request.form.get('lunch_percent', '').strip()
        try:
            lunch_percent = Decimal(lunch_percent_raw)
        except (InvalidOperation, ValueError):
            raise ValueError("Invalid lunch percentage. Please enter a number between 0 and 1.")
        if lunch_percent < 0 or lunch_percent > 1:
            raise ValueError("Invalid lunch percentage. Please enter a number between 0 and 1.")

        no_new_clothes_cost = request.form.get('new_clothes') == 'on'



    except ValueError as e:
        error = str(e)
        return render_template('index.html', error=error)


    # Calculations
    commute_cost = float(((commute * Decimal("2")) * Decimal("0.58")) * Decimal("261"))
    lunch_cost = float(Decimal("10") * Decimal("261") * lunch_percent)
    if no_new_clothes_cost:
        apparel_cost = 0
    else:
        apparel_cost = 1754
    total_salary = commute_cost + base_salary + lunch_cost + apparel_cost
    total_salary_display = f"{total_salary:,.2f}"

    return render_template('result.html', total_salary_display=total_salary_display)


if __name__ == '__main__':
    app.run(debug=True)
