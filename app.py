from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    base_salary = int(request.form['base_salary'])
    commute = int(request.form['commute'])
    lunch_percent = float(request.form['lunch_percent'])

    # Validate inputs
    if base_salary < 0 or base_salary > 999999:
        return render_template('index.html', error="Invalid salary input")

    # Calculations
    commute_cost = ((commute * 2) * .58) * 261
    lunch_cost = 10 * 261 * lunch_percent
    apparel_cost = 1754
    total_salary = commute_cost + base_salary + lunch_cost + apparel_cost

    return render_template('result.html', total_salary=total_salary)


if __name__ == '__main__':
    app.run(debug=True)
