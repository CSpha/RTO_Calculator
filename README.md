# RTO_Calculator

Welcome to my RTO Calculator! This project is designed to help job seekers determine the cost of returning to the office.

The target user is someone that is currently working from home, does not eat out for lunch, and does not spend much (if any) 
money on clothes needed for work.


**USER GUIDE**

Users can enter their current salary, the mileage that they will need to travel to the office (one-way), and the frequency they 
believe they will be eating out for lunch. The application will automatically add in the average amount that a 
white-collar employee spends on attire each year. 

The application will display the salary required in order to ensure that the user does not end up losing money by 
switching to an on-site role.

**UPCOMING FEATURES**

1. Improve input validation
2. Improve UX
3. Add some type of map integration so users can input their home address and the office address so the application 
will determine the mileage used by the algorithm.
4. Add logic to account for users who don't believe their meal or clothing budget will change by returning to the office.

**BUILD & RUN**

- **Run the app:**

```powershell
python app.py
```

- **Or use `flask run`:**

```powershell
$env:FLASK_APP = "app.py"
flask run
```

The app serves templates from the `templates/` folder; open http://127.0.0.1:5000/ after starting.