import unittest
from service import app


class TestService(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_1(self):
        resp = self.client.get("/", data={})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["Content-Type"], "application / json")


if __name__ == "__main__":
    unittest.main()
