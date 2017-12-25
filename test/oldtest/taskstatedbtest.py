import unittest
import requests

class TestTaskStateDB(unittest.TestCase):

    def testSetState(self):
        rep = requests.post('http://localhost:8083/api/task/taskstate/db', json = {
            'test': 'test'
        })
        print rep
        print rep.content
