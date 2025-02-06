"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest
from src import app
from http import HTTPStatus

@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndpoints:
    """Test cases for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        response = client.post('/counters/test_counter')
        assert response.status_code == HTTPStatus.CREATED
        assert response.get_json() == {"test_counter": 0}

    def test_prevent_duplicate_counter(self, client):
        """It should not allow duplicate counters"""
        client.post('/counters/test_counter')
        response = client.post('/counters/test_counter')
        assert response.status_code == HTTPStatus.CONFLICT

    def test_retrieve_existing_counter(self, client):
        """It should retrieve an existing counter"""
        client.post('/counters/test_counter')
        response = client.get('/counters/test_counter')
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"test_counter": 0}

    def test_return_404_for_non_existent_counter(self, client):
        """It should return 404 if counter does not exist"""
        response = client.get('/counters/non_existent')
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_increment_counter(self, client):
        """It should increment an existing counter"""
        client.post('/counters/test_counter')
        response = client.put('/counters/test_counter')
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"test_counter": 1}

    def test_prevent_updating_non_existent_counter(self, client):
        """It should return 404 if trying to increment a non-existent counter"""
        response = client.put('/counters/non_existent')
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_counter(self, client):
        """It should delete an existing counter"""
        client.post('/counters/test_counter')
        response = client.delete('/counters/test_counter')
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_prevent_deleting_non_existent_counter(self, client):
        """It should return 404 if trying to delete a non-existent counter"""
        response = client.delete('/counters/non_existent')
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_reset_all_counters(self, client):
        """It should reset all counters"""
        client.post('/counters/test_counter')
        response = client.post('/counters/reset')
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"message": "All counters have been reset"}

    def test_list_all_counters(self, client):
        """It should list all counters"""
        client.post('/counters/test_counter1')
        client.post('/counters/test_counter2')
        response = client.get('/counters')
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"test_counter1": 0, "test_counter2": 0}

    def test_handle_invalid_http_methods(self, client):
        """It should return 405 for unsupported HTTP methods"""
        response = client.patch('/counters/test_counter')
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    
    
    """Test cases for Extended Counter API"""

    # ===========================
    # Test: Retrieve total count of all counters
    # Author: Student 1
    # ===========================
    def test_get_total_counters(self, client):
        """It should return the total sum of all counter values"""
        client.post('/counters/test1')
        client.post('/counters/test2')
        client.put('/counters/test1')
        response = client.get('/counters/total')
        
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"total": 1}  # TODO: Verify correct count

    # ===========================
    # Test: Retrieve top N highest counters
    # Author: Student 2
    # ===========================
    def test_top_n_counters(self, client):
        """It should return the top N highest counters"""
        client.post('/counters/reset')
        client.post('/counters/a')
        client.post('/counters/b')
        client.put('/counters/b')
        
        response = client.get('/counters/top/1')
        
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"b": 1}  # TODO: Ensure correct top counter

    # ===========================
    # Test: Retrieve top N lowest counters
    # Author: Student 3
    # ===========================
    def test_bottom_n_counters(self, client):
        """It should return the bottom N lowest counters"""
        client.post('/counters/reset')
        client.post('/counters/a')
        client.post('/counters/b')
        client.put('/counters/a')

        response = client.get('/counters/bottom/1')
        
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"b": 0}  # TODO: Ensure correct bottom counter

    # ===========================
    # Test: Set a counter to a specific value
    # Author: Student 4
    # ===========================
    def test_set_counter_to_value(self, client):
        """It should set a counter to a specific value"""
        client.post('/counters/test1')
        response = client.put('/counters/test1/set/5')

        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"test1": 5}  # TODO: Verify correct value

    # ===========================
    # Test: Prevent negative counter values
    # Author: Student 5
    # ===========================
    def test_prevent_negative_counter_values(self, client):
        """It should prevent setting a counter to a negative value"""
        client.post('/counters/test1')
        response = client.put('/counters/test1/set/-3')

        assert response.status_code == HTTPStatus.BAD_REQUEST  # TODO: Verify rejection
        assert "Counter value cannot be negative" in response.get_json()["error"]

    # ===========================
    # Test: Reset a single counter
    # Author: Student 6
    # ===========================
    def test_reset_single_counter(self, client):
        """It should reset a specific counter"""
        client.post('/counters/test1')
        client.put('/counters/test1/set/5')
        response = client.post('/counters/test1/reset')

        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"test1": 0}  # TODO: Verify reset success

    # ===========================
    # Test: Prevent resetting a non-existent counter
    # Author: Student 7
    # ===========================
    def test_prevent_resetting_non_existent_counter(self, client):
        """It should return an error when resetting a non-existent counter"""
        response = client.post('/counters/non_existent/reset')

        assert response.status_code == HTTPStatus.NOT_FOUND  # TODO: Ensure correct error

    # ===========================
    # Test: Get total number of counters
    # Author: Student 8
    # ===========================
    def test_get_total_number_of_counters(self, client):
        """It should return the total number of counters"""
        client.post('/counters/reset')
        client.post('/counters/test1')
        client.post('/counters/test2')
        
        response = client.get('/counters/count')
        
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"count": 2}  # TODO: Ensure correct count

    # ===========================
    # Test: Retrieve counters with values greater than a threshold
    # Author: Student 9
    # ===========================
    def test_counters_greater_than_threshold(self, client):
        """It should return counters greater than the threshold"""
        client.post('/counters/a')
        client.post('/counters/b')
        client.put('/counters/a/set/10')

        response = client.get('/counters/greater/5')

        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"a": 10}  # TODO: Ensure correct filtering

    # ===========================
    # Test: Retrieve counters with values less than a threshold
    # Author: Student 10
    # ===========================
    def test_counters_less_than_threshold(self, client):
        """It should return counters less than the threshold"""
        client.post('/counters/reset')
        client.post('/counters/a')
        client.post('/counters/b')
        client.put('/counters/a/set/2')

        response = client.get('/counters/less/5')

        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"a": 2, "b": 0}  # TODO: Ensure correct filtering

    # ===========================
    # Test: Validate counter names (prevent special characters)
    # Author: Student 11
    # ===========================
    def test_validate_counter_name(self, client):
        """It should prevent creating counters with special characters"""
        response = client.post('/counters/test@123')

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Invalid counter name" in response.get_json()["error"]  # TODO: Ensure correct error
