from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestCalculateCost:

    def post_calculate_cost(self, payload, expected_status, expected_response=None, expected_message=None):
        """
        Helper function for sending POST requests and asserting responses
        """
        response = client.post("/calculate_cost/", json=payload)
        assert response.status_code == expected_status

        if expected_response:
            assert response.json() == expected_response

        if expected_message:
            assert response.json()['detail'] == expected_message
        return response



    def test_no_payload(self):
        """
        Test for no payload
        """
        self.post_calculate_cost(None, 422)


    def test_correct_data_variants(self):
        """
        Test for correct data with various scenarios
        """
        scenarios = [
            ({"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-02-21T14:40:00Z"}, {"delivery_fee": 710}),
            ({"cart_value": 1, "delivery_distance": 1000, "number_of_items": 4, "time": "2024-02-21T14:40:00Z"}, {"delivery_fee": 1199}),
			({"cart_value": 12700, "delivery_distance": 1000, "number_of_items": 4, "time": "2024-02-21T14:40:00Z"}, {"delivery_fee": 200}),
            ({"cart_value": 790, "delivery_distance": 2235, "number_of_items": 20, "time": "2024-03-21T14:40:00Z"}, {"delivery_fee": 1500}),
            ({"cart_value": 20000, "delivery_distance": 2235, "number_of_items": 20, "time": "2024-03-21T14:40:00Z"}, {"delivery_fee": 0}),
			({"cart_value": 21000, "delivery_distance": 2235, "number_of_items": 20, "time": "2024-03-21T14:40:00Z"}, {"delivery_fee": 0}),
        ]
        for data, expected in scenarios:
            self.post_calculate_cost(data, 200, expected)


    def test_missing_required_fields(self):
        """
        Test for missing required fields
        """
        scenarios = [
            ({"delivery_distance": 2235, "number_of_items": 4, "time": "2024-02-21T14:40:00Z"}, 422),
            ({"cart_value": 790, "number_of_items": 4, "time": "2024-02-21T14:40:00Z"}, 422),
            ({"cart_value": 790, "delivery_distance": 2235, "time": "2024-02-21T14:40:00Z"}, 422),
			({"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4}, 422),
            ({"cart_value": 790, "delivery_distance": 2235}, 422),
            ({"cart_value": 790, "number_of_items": 4}, 422),
            ({"delivery_distance": 2235, "number_of_items": 4}, 422),
            ({"cart_value": 790}, 422),
            ({"delivery_distance": 2235}, 422),
            ({"number_of_items": 4}, 422),
			({"time": "2024-02-21T14:40:00Z"}, 422),
        ]
        for data, expected_status in scenarios:
            self.post_calculate_cost(data, expected_status)


    def test_incorrect_field_names(self):
        """
        Test for incorrect field names
        """
        data = {"cart_value": 790, "delivery_dis": 2235, "number_of_items": 4, "time": "2024-03-21T14:40:00Z"}
        self.post_calculate_cost(data, 422)


    def test_invalid_field_values(self):
        """
        Test for invalid field values
        """
        scenarios = [
            ({"cart_value": -10, "delivery_distance": 1000, "number_of_items": 4, "time": "2024-02-21T14:40:00Z"}, 422),
            ({"cart_value": 3000, "delivery_distance": -100, "number_of_items": 4, "time": "2024-02-21T14:40:00Z"}, 422),
            ({"cart_value": 3000, "delivery_distance": 1000, "number_of_items": -1, "time": "2024-02-21T14:40:00Z"}, 422),
			({"cart_value": 0, "delivery_distance": 1000, "number_of_items": 4, "time": "2024-02-21T14:40:00Z"}, 422),
            ({"cart_value": 3000, "delivery_distance": 0, "number_of_items": 4, "time": "2024-02-21T14:40:00Z"}, 422),
            ({"cart_value": 3000, "delivery_distance": 1000, "number_of_items": 0, "time": "2024-02-21T14:40:00Z"}, 422),
        ]
        for data, expected_status in scenarios:
            self.post_calculate_cost(data, expected_status)


    def test_date_related_errors(self):
        """
        Test for date-related errors (past date, incorrect timezone, etc.)
        """
        scenarios = [
            ({"cart_value": 21000, "delivery_distance": 2235, "number_of_items": 20, "time": "2013-03-21T14:40:00Z"}, 400, "The Wolt company was not founded before 6 October 2014"),
            ({"cart_value": 21000, "delivery_distance": 2235, "number_of_items": 20, "time": "2024-03-21T14:40:00"}, 400, "Timezone must be specified and in UTC"),
            ({"cart_value": 21000, "delivery_distance": 2235, "number_of_items": 20, "time": "2024-03-21T14:40:00:02:00"}, 400, "Invalid time format, must be ISO 8601"),
            ({"cart_value": 21000, "delivery_distance": 2235, "number_of_items": 20, "time": "2024-03-21T14:40:00+02:00"}, 400, "Timezone must be specified and in UTC"),
        ]
        for data, expected_status, expected_message in scenarios:
            self.post_calculate_cost(data, expected_status, expected_message=expected_message)


    def test_correct_time_format(self):
        """
        Test for correct time format
        """
        data = {"cart_value": 21000, "delivery_distance": 2235, "number_of_items": 20, "time": "2022-03-21T14:40:00+00:00"}
        self.post_calculate_cost(data, 200, {'delivery_fee': 0})
