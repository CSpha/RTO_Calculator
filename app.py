from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    error = None
    try:
        base_salary = (request.form['base_salary'])
        if not base_salary.isdigit():
            raise ValueError("Invalid salary. Salary must be a whole number.")
        base_salary = int(base_salary)
        if base_salary < 0 or base_salary > 999999:
            raise ValueError("Invalid salary. Salary must be between 0 and 999,999.")

        commute = int(request.form['commute'])
        if commute < 0:
            raise ValueError("Invalid commute distance")

        lunch_percent = float(request.form['lunch_percent'])
        if lunch_percent <0 or lunch_percent > 1:
            raise ValueError("Invalid lunch percentage")

    except ValueError as e:
        error = str(e)
        return render_template('index.html', error=error)


    # Calculations
    commute_cost = ((commute * 2) * .58) * 261
    lunch_cost = 10 * 261 * lunch_percent
    apparel_cost = 1754
    total_salary = commute_cost + base_salary + lunch_cost + apparel_cost

    return render_template('result.html', total_salary=total_salary)


if __name__ == '__main__':
    app.run(debug=True)
