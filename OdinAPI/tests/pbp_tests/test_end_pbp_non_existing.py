import unittest
import json
from main import app
from tests.pbp_tests.pbp_data import data

class TestEndVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_end_pbp_invalid(self):
        response = self.client.post('/pbp/end',data=json.dumps(data["non_exists_id"]),content_type='application/json', follow_redirects=True)
        expected_msg = "PBP sequence does not exist."
        self.assertEqual(response.status_code, 403)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

if __name__ == "__main__":
    unittest.main()