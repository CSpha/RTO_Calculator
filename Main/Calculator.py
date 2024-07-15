print("Welcome to the Return to Office Calculator!\n")
base_salary = int(input("Please enter your current salary rounding to the nearest whole number and with no commas: "))

if base_salary < 0 or base_salary > 999999:
    print("Invalid input")
else:
    print("Great! Just a few more questions.\n")

commute = int(input("Please enter (in miles) how far the work location is from your house: \n"))
# U.S. Department of Energy estimate of average cost per mile. Assuming round trip and 261 working days per year.
commute_cost = ((commute * 2) * .58) * 261

lunch_percent = float(input("What percentage of the time do you believe you will buy lunch? We will assume the cost "
                            "of a typical lunch is $10.00. \n"))
# ChatGPT estimate for average lunch cost, 261 working days per year, and user's estimate of eating out.
lunch_cost = 10 * 261 * lunch_percent

# Apparel costs for white-collar employees as reported by the U.S. Bureau of Labor
apparel_cost = 1754

print("The U.S. Bureau of Labor estimates that the typical white-collar employee spends $1754 on clothing each year so "
"we will factor that in as well.\n")

total_salary = commute_cost + base_salary + lunch_cost + apparel_cost

print("The salary of your next position must be equal or greater than $" + str(total_salary) + " to ensure that you "
      "will not be losing money by switching jobs.")


