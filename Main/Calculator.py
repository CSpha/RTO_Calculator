print("Welcome to the Return to Office Calculator!\n")
base_salary = int(input("Please enter your current salary rounding to the nearest whole number and with no commas: "))


if base_salary < 0 or base_salary > 999999:
    print("Invalid input")
else:
    print("Thank you")

commute = int(input("Please enter (in miles) how far the work location is from your house: "))
commute_cost = (commute * 2) * .41

total_salary = commute_cost + base_salary


print("The salary of your next position must be equal or greater than " + str(total_salary) + " to ensure that you will be making more money by switching jobs.")


