#!/usr/bin/python3
"""
Unittest for user module
"""
import os
import unittest
from models.user import User
import models
from datetime import datetime
from models.engine.file_storage import FileStorage


class Test_User(unittest.TestCase):
    """ Test for
    User Class """

    def setUp(self):
        """set up the
        test for testing users"""
        FileStorage._FileStorage__file_path = "file.json"

    def testargsNone(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def testkwargsNone(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

    def testpublic(self):
        self.assertEqual(str, type(User().id))

    def testargsNone(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def testkwargsNone(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

    def testpublic(self):
        self.assertEqual(str, type(User().id))

    def testnoarg(self):
        self.assertEqual(User, type(User()))

    def testnew_instance(self):
        self.assertIn(User(), models.storage.all().values())

    def testcreate_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def testupdate_time(self):
        self.assertEqual(datetime, type(User().updated_at))

    def testemail(self):
        self.assertEqual(str, type(User.email))

    def testpassword(self):
        self.assertEqual(str, type(User.password))

    def testfirsstname(self):
        self.assertEqual(str, type(User.first_name))

    def testlastname(self):
        self.assertEqual(str, type(User.last_name))

    def testmultipleuser(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def testmultipleuser_created(self):
        user1 = User()
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def testkawargs(self):
        datetm = datetime.today()
        datef = datetm.isoformat()
        user = User(id="13", created_at=datef, updated_at=datef)
        self.assertEqual(user.id, "13")
        self.assertEqual(user.created_at, datetm)
        self.assertEqual(user.updated_at, datetm)

    def testargs(self):
        datetm = datetime.today()
        datef = datetm.isoformat()
        dater = repr(datetm)
        user = User()
        user.id = "13"
        user.created_at = user.updated_at = datetm
        user_str = user.__str__()
        self.assertIn("[User] (13)", user_str)
        self.assertIn("'id': '13'", user_str)
        self.assertIn("'created_at': " + dater, user_str)
        self.assertIn("'updated_at': " + dater, user_str)


class TestSave(unittest.TestCase):

    def setUp(self):
        """set up the
        test for testing users"""
        FileStorage._FileStorage__file_path = "file.json"

    @classmethod
    def SetUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

    def testsavearg(self):
        user = User()
        with self.assertRaises(TypeError):
            user.save(None)

    def testsave(self):
        user = User()
        update = user.updated_at
        user.save()
        self.assertLess(update, user.updated_at)

    def testmultiplesave(self):
        user = User()
        update = user.updated_at
        user.save()
        update2 = user.updated_at
        self.assertLess(update, user.updated_at)
        user.save()
        self.assertLess(update2, user.updated_at)

    def testsaveupdated(self):
        user = User()
        user.save()
        userid = "User." + user.id
        with open("file.json", "r") as f:
            self.assertIn(userid, f.read())


class Testuser_dict(unittest.TestCase):

    def tesstNone(self):
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict(None)

    def testmuldict(self):
        user = User()
        self.assertNotEqual(user.to_dict(), user.__dict__)

    def testdicttype(self):
        self.assertTrue(dict, type(User().to_dict()))

    def testdict(self):
        user = User()
        self.assertIn("id", user.to_dict())
        self.assertIn("created_at", user.to_dict())
        self.assertIn("updated_at", user.to_dict())
        self.assertIn("__class__", user.to_dict())

    def testdictstr(self):
        user = User()
        Duser = user.to_dict()
        self.assertEqual(str, type(Duser['id']))
        self.assertEqual(str, type(Duser["created_at"]))
        self.assertEqual(str, type(Duser["updated_at"]))

    def testdictend(self):
        datetm = datetime.today()
        datef = datetm.isoformat()
        user = User()
        user.id = "13"
        user.created_at = user.updated_at = datetm
        Dict = {
            "id": "13",
            "__class__":  "User",
            "created_at": datef,
            "updated_at": datef,
        }

    def testdictarg(self):
        user = User()
        user.name = "Kezieh"
        user.number = 90
        self.assertEqual("Kezieh", user.name)
        self.assertIn("number", user.to_dict())


if __name__ == "__main__":
    unittest.main()
