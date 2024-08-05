from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    error = None
    try:
        base_salary = request.form['base_salary']
        if not base_salary.isdigit():
            raise ValueError("Invalid salary. Salary must be a whole number.")
        base_salary = int(base_salary)
        if base_salary < 0 or base_salary > 999999:
            raise ValueError("Invalid salary. Salary must be between 0 and 999,999.")

        commute = request.form['commute']
        try:
            commute = float(commute)
            if commute < 0:
                raise ValueError("Invalid commute distance entered. It must be a positive number.")
        except ValueError:
            raise ValueError("Invalid commute distance entered. Please enter a number.")

        lunch_percent = float(request.form['lunch_percent'])
        if lunch_percent <0 or lunch_percent > 1:
            raise ValueError("Invalid lunch percentage")

        new_clothes = request.form['new_clothes']



    except ValueError as e:
        error = str(e)
        return render_template('index.html', error=error)


    # Calculations
    commute_cost = ((commute * 2) * .58) * 261
    lunch_cost = 10 * 261 * lunch_percent
    if new_clothes:
        apparel_cost = 1754
    else:
        apparel_cost = 0
    total_salary = commute_cost + base_salary + lunch_cost + apparel_cost

    return render_template('result.html', total_salary=total_salary)


if __name__ == '__main__':
    app.run(debug=True)
