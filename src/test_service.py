import unittest
from service import app


class TestService(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_1(self):
        resp = self.client.get("/healthz")

        self.assertEqual(200, resp.status_code)

    def test_2(self):
        resp = self.client.post("/v1/user", data="{}")

        self.assertEqual(400, resp.status_code)

    def test_3(self):
        resp = self.client.get("/v1/user/self", data="{}")

        self.assertEqual(401, resp.status_code)

    def test_4(self):
        resp = self.client.put("/v1/user/self")

        self.assertEqual(401, resp.status_code)


if __name__ == "__main__":
    unittest.main()
