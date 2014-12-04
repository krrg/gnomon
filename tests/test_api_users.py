
# LIST all users in system:     GET     /users
# LOOKUP id of specific:        GET     /users?username=USERNAME
# GET information on user:      GET     /users/<id>
# CREATE new user:              POST    /users
# UPDATE new user:              PUT     /users/<id>

import requests as r
import unittest
import json
import time

class ApiUsersTest(unittest.TestCase):

    def setUp(self):
        self.URL_PRE = "http://localhost:5000/api/v1"
        pass

    def test_list_users(self):
        response = r.get(self.URL_PRE + "/users")
        print "Testing LIST USERS\t\t",
        self.assertTrue(response.status_code == 200)
        print "PASSED"

    def test_create_users(self):

        ##########################################################
        print "Testing CREATE USER ENDPOINT\t\t",
        username = "UnitTest@" + str(int(time.time()))

        resp = r.post(self.URL_PRE + "/users", data=json.dumps({
            "user": {
                "username": username,
                "password": username + "pw",
                "email": username + "email"
            }
        }))
        self.assertTrue(resp.status_code == 200)
        print "PASSED"
        ##########################################################


        ##########################################################
        userid = resp.json()['user']['id']

        print "Testing CREATE USER actually worked\t",
        resp = r.get(self.URL_PRE + "/users/" + userid)
        self.assertTrue(resp.status_code)
        jsonresp = resp.json()
        self.assertTrue(jsonresp['user']['id'] == userid)
        self.assertTrue(jsonresp['user']['username'] == username)
        print "PASSED"
        ##########################################################


