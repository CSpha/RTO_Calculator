import unittest

from app import app


class RTOCalculatorValidationTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def post_form(self, **overrides):
        payload = {
            "base_salary": "85000",
            "commute": "12.5",
            "lunch_percent": "0.5",
        }
        payload.update(overrides)
        return self.client.post("/calculate", data=payload)

    def test_valid_submission_returns_result(self):
        response = self.post_form()

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Calculation Result", response.data)
        self.assertIn(b"$91,843.50", response.data)

    def test_empty_fields_show_required_errors(self):
        response = self.post_form(base_salary="", commute="", lunch_percent="")

        self.assertIn(b"Salary is required.", response.data)
        self.assertIn(b"Commute distance is required.", response.data)
        self.assertIn(b"Lunch percentage is required.", response.data)

    def test_salary_rejects_decimal_input(self):
        response = self.post_form(base_salary="85000.50")

        self.assertIn(b"Salary must be a whole number with no commas or symbols.", response.data)

    def test_commute_rejects_scientific_notation_and_extra_precision(self):
        scientific_notation = self.post_form(commute="1e2")
        extra_precision = self.post_form(commute="12.55")

        self.assertIn(b"Commute distance must be a plain number with no commas or symbols.", scientific_notation.data)
        self.assertIn(b"Commute distance can have at most 1 decimal place.", extra_precision.data)

    def test_lunch_percent_rejects_out_of_range_and_extra_precision(self):
        out_of_range = self.post_form(lunch_percent="1.5")
        extra_precision = self.post_form(lunch_percent="0.125")

        self.assertIn(b"Lunch percentage must be between 0 and 1.", out_of_range.data)
        self.assertIn(b"Lunch percentage can have at most 2 decimal places.", extra_precision.data)


if __name__ == "__main__":
    unittest.main()
