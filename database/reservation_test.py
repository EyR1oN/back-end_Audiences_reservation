import requests
from app_test import *


class TestReservation(MyTest):
    def setUp(self):
        self.user_username = "default"
        self.user_password = "password"
        self.user_userStatus = 1
        self.user_firstName = "Name"
        self.user_auth = self.user_username, self.user_password
        self.user_data = {"username": self.user_username, "password": self.user_password,
                          "userStatus": self.user_userStatus}

        self.reservation_idAudience = 1
        self.reservation_idStatus = 1
        self.reservation_start = "2021-01-01 1:00:00"
        self.reservation_end = "2021-01-01 3:00:00"

        self.reservation_data = {
            "idReservation": 42,
            "idAudience": self.reservation_idAudience,
            "idStatus": self.reservation_idStatus,
            "amountOfHours": 2,
            "dateTimeOfReservation": self.reservation_start,
            "dateTimeOfEndReservation": self.reservation_end
        }
        self.header = {"Content-Type": "application/json", }

    def test11_post_user(self):
        resp = self.client.post("http://localhost:5000/user", headers=self.header, data=json.dumps(self.user_data))
        self.assertEqual(200, resp.status_code)

    def test12_post_reservation(self):
        u = Session.query(User).filter_by(username=self.user_username).first()
        self.reservation_data['idUser'] = u.idUser
        resp = self.client.post("http://localhost:5000/reservation",
                                headers=self.header,
                                auth=self.user_auth,
                                data=json.dumps(self.reservation_data)
                                )
        self.assertEqual(200, resp.status_code)

    def test13_get_reservation(self):
        resp = self.client.get("http://localhost:5000/reservation/" + str(self.reservation_data.get('idReservation')),
                               headers=self.header,
                               auth=self.user_auth)
        self.assertEqual(resp.status_code, 200)

    def test14_get_reservation(self):
        resp = self.client.get("http://localhost:5000/reservation/" + str(self.reservation_data.get('idReservation')),
                               headers=self.header,
                               auth=(self.user_auth, "gadjkdfhjkjkcxv"))
        self.assertEqual(resp.status_code, 401)

    def test15_get_reservation(self):
        resp = self.client.get(
            "http://localhost:5000/reservation/" + str(self.reservation_data.get('idReservation') + 1),
            headers=self.header,
            auth=self.user_auth)
        self.assertEqual(resp.status_code, 404)

    def test16_put_reservation(self):
        resp = self.client.put("http://localhost:5000/reservation/" + str(self.reservation_data.get('idReservation')),
                               headers=self.header,
                               auth=self.user_auth,
                               data=json.dumps({"idAudience": self.reservation_idAudience}))
        self.assertEqual(resp.status_code, 200)

    def test17_put_reservation(self):
        resp = self.client.put("http://localhost:5000/reservation/1" + str(self.reservation_data.get('idReservation')),
                               headers=self.header,
                               auth=self.user_auth,
                               data=json.dumps({"idAudience": self.reservation_idAudience}))
        self.assertEqual(resp.status_code, 404)

    def test18_delete_reservation(self):
        resp = self.client.delete(
            "http://localhost:5000/reservation/" + str(self.reservation_data.get('idReservation')),
            headers=self.header,
            auth=self.user_auth)
        self.assertEqual(resp.status_code, 200)

    def test19_delete_reservation(self):
        resp = self.client.delete(
            "http://localhost:5000/reservation/" + str(self.reservation_data.get('idReservation')),
            headers=self.header,
            auth=self.user_auth)
        self.assertEqual(resp.status_code, 404)

    def test20_del_user(self):
        resp = self.client.delete("http://localhost:5000/user/" + self.user_username, headers=self.header,
                                  auth=self.user_auth)
        self.assertEqual(resp.status_code, 200)
