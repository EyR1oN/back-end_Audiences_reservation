import requests
from app_test import *


class TestUser(MyTest):
    def setUp(self):
        self.user_username = "default"
        self.user_password = "password"
        self.user_userStatus = 1
        self.user_firstName = "Name"
        self.user_auth = self.user_username, self.user_password
        self.user_data = {"username": self.user_username, "password": self.user_password,
                          "userStatus": self.user_userStatus}
        self.header = {"Content-Type": "application/json", }

    def test1_post_user(self):
        resp = self.client.post("http://localhost:5000/user", headers=self.header, data=json.dumps(self.user_data))
        self.assertEqual(200, resp.status_code)
        # self.assertGreaterEqual(resp.json().items(), dict(username="default").items())

    def test2_post_user(self):
        resp = self.client.post("http://localhost:5000/user", headers=self.header, data=json.dumps(self.user_data))
        self.assertEqual(409, resp.status_code)
        # self.assertGreaterEqual(resp.json().items(), dict(username="default").items())

    def test3_get_user(self):
        resp = self.client.get("http://localhost:5000/user/" + self.user_username, headers=self.header)
        self.assertEqual(resp.status_code, 200)

    def test4_update_user(self):
        resp = self.client.put("http://localhost:5000/user/" + self.user_username, headers=self.header,
                               auth=self.user_auth, data=json.dumps({"first_name": self.user_firstName}))
        self.assertEqual(resp.status_code, 200)

    def test5_update_user(self):
        resp = self.client.put("http://localhost:5000/user/3213" + self.user_username, headers=self.header,
                               auth=self.user_auth, data=json.dumps({"username": self.user_username}))
        self.assertEqual(resp.status_code, 404)

    def test6_update_user(self):
        resp = self.client.put("http://localhost:5000/user/" + self.user_username, headers=self.header,
                               auth=self.user_auth, data=json.dumps({"username": self.user_username}))
        self.assertEqual(resp.status_code, 409)

    def test7_del_user(self):
        resp = self.client.delete("http://localhost:5000/user/" + self.user_username, headers=self.header,
                                  auth=self.user_auth)
        self.assertEqual(resp.status_code, 200)

    def test8_del_user(self):
        resp = self.client.delete("http://localhost:5000/user/" + self.user_username, headers=self.header,
                                  auth=self.user_auth)
        self.assertEqual(resp.status_code, 401)

    def test9_get_user(self):
        resp = self.client.get("http://localhost:5000/user/asdfafsd", headers=self.header)
        self.assertEqual(resp.status_code, 401)

    def test10_update_user(self):
        resp = self.client.put("http://localhost:5000/user/asfdasdf" + self.user_username, headers=self.header,
                               auth=self.user_auth, data=json.dumps({"first_name": self.user_firstName}))
        self.assertEqual(resp.status_code, 401)
