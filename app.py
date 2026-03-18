from decimal import Decimal, InvalidOperation
import re
from flask import Flask, request, render_template

app = Flask(__name__)

MAX_SALARY = 999999
MAX_COMMUTE = Decimal("500")
MAX_LUNCH_PERCENT = Decimal("1")
COMMUTE_DECIMAL_PLACES = 1
LUNCH_DECIMAL_PLACES = 2
PLAIN_NUMBER_PATTERN = re.compile(r"^(?:\d+|\d*\.\d+)$")


def count_decimal_places(raw_value):
    if "." not in raw_value:
        return 0
    return len(raw_value.split(".", maxsplit=1)[1])


def validate_salary(raw_value):
    if not raw_value:
        return None, "Salary is required."
    if not raw_value.isdigit():
        return None, "Salary must be a whole number with no commas or symbols."

    salary = int(raw_value)
    if salary < 0 or salary > MAX_SALARY:
        return None, f"Salary must be between 0 and {MAX_SALARY:,}."
    return salary, None


def validate_decimal_field(raw_value, *, label, max_value, max_decimal_places):
    if not raw_value:
        return None, f"{label} is required."
    if not PLAIN_NUMBER_PATTERN.fullmatch(raw_value):
        return None, f"{label} must be a plain number with no commas or symbols."

    try:
        value = Decimal(raw_value)
    except (InvalidOperation, ValueError):
        return None, f"{label} must be a number."

    if value < 0 or value > max_value:
        return None, f"{label} must be between 0 and {max_value}."
    if count_decimal_places(raw_value) > max_decimal_places:
        suffix = "" if max_decimal_places == 1 else "s"
        return None, f"{label} can have at most {max_decimal_places} decimal place{suffix}."
    return value, None


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

    base_salary, base_salary_error = validate_salary(form_data['base_salary'])
    if base_salary_error:
        errors['base_salary'] = base_salary_error

    commute, commute_error = validate_decimal_field(
        form_data['commute'],
        label="Commute distance",
        max_value=MAX_COMMUTE,
        max_decimal_places=COMMUTE_DECIMAL_PLACES,
    )
    if commute_error:
        errors['commute'] = commute_error

    lunch_percent, lunch_percent_error = validate_decimal_field(
        form_data['lunch_percent'],
        label="Lunch percentage",
        max_value=MAX_LUNCH_PERCENT,
        max_decimal_places=LUNCH_DECIMAL_PLACES,
    )
    if lunch_percent_error:
        errors['lunch_percent'] = lunch_percent_error

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
