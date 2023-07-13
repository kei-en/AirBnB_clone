#!/usr/bin/python3
"""
Unittest for base module
"""
import io
import unittest
import os
import models
from models.base_model import BaseModel
from datetime import datetime
from models import storage
from models.engine.file_storage import FileStorage


class Test_BaseModel(unittest.TestCase):
    """ Test for
    Base_Model Class """

    def setUp(self):
        """set up the
        test for testing bae models"""
        FileStorage._FileStorage__file_path = "file.json"

    def test_noarg(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_None(self):
        Bsmodel = BaseModel(None)
        self.assertNotIn(None, Bsmodel.__dict__.values())

    def test_publicid(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_public_updateat(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_public_createat(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_all_storage_obj(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_all_str(self):
        date_tm = datetime.today()
        date_rep = repr(date_tm)
        Bsmodel = BaseModel()
        Bsmodel.id = "123456"
        Bsmodel.created_at = Bsmodel.updated_at = date_tm
        Bsmodel_str = Bsmodel.__str__()
        self.assertIn("[BaseModel] (123456)", Bsmodel_str)
        self.assertIn("'id': '123456'", Bsmodel_str)
        self.assertIn("'created_at': " + date_rep, Bsmodel_str)
        self.assertIn("'updated_at': " + date_rep, Bsmodel_str)

    def test_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_two_models(self):
        Bsmodel1 = BaseModel()
        Bsmodel2 = BaseModel()
        self.assertNotEqual(Bsmodel1.id, Bsmodel2.id)

    def test_kwargs(self):
        date_tm = datetime.today()
        date_f = date_tm.isoformat()
        Bsmodel = BaseModel(id="12345", created_at=date_f, updated_at=date_f)
        self.assertEqual(Bsmodel.id, "12345")
        self.assertEqual(Bsmodel.created_at, date_tm)
        self.assertEqual(Bsmodel.updated_at, date_tm)

    def testsave(self):
        Bsmodel = BaseModel()
        Update_at = Bsmodel.updated_at
        Bsmodel.save()
        self.assertLess(Update_at, Bsmodel.updated_at)

    def testsave_arg(self):
        Bsmodel = BaseModel()
        with self.assertRaises(TypeError):
            Bsmodel.save(None)

    def testsave_update(self):
        Bsmodel = BaseModel()
        Bsmodel.save()
        Bsmodelid = "BaseModel." + Bsmodel.id
        with open("file.json", "r") as f:
            self.assertIn(Bsmodelid, f.read())

    def testmulsave(self):
        Bsmodel = BaseModel()
        f_updated_at = Bsmodel.updated_at
        Bsmodel.save()
        s_updated_at = Bsmodel.updated_at
        self.assertLess(f_updated_at, s_updated_at)
        Bsmodel.save()
        self.assertLess(s_updated_at, Bsmodel.updated_at)


class Test_save(unittest.TestCase):

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp", "file.json")
        except IOError:
            pass


class Test_to_dict(unittest.TestCase):

    def testto_dict(self):
        dtm = datetime.today()
        Bsmodel = BaseModel()
        Bsmodel.id = "012"
        Bsmodel.created_at = Bsmodel.updated_at = dtm
        todict = {
            "id": "012",
            "created_at": dtm.isoformat(),
            "updated_at": dtm.isoformat(),
            "__class__": "BaseModel"
        }
        self.assertDictEqual(Bsmodel.to_dict(), todict)

    def testtype(self):
        Bsmodel = BaseModel()
        self.assertTrue(dict, type(Bsmodel.to_dict()))

    def testto_dict_updated_at(self):
        Bsmodel = BaseModel()
        DBsmodel = Bsmodel.to_dict()
        self.assertEqual(str, type(DBsmodel["updated_at"]))

    def testattr(self):
        Bsmodel = BaseModel()
        Bsmodel_nm = 'ALX'
        Bsmodel_num = 100
        self.assertNotIn('name', Bsmodel.to_dict())
        self.assertNotIn('my_number', Bsmodel.to_dict())

    def testmuldict(self):
        Bsmodel = BaseModel()
        with self.assertRaises(TypeError):
            Bsmodel.to_dict(None)

    def testto_dict_arg(self):
        Bsmodel = BaseModel()
        with self.assertRaises(TypeError):
            Bsmodel.to_dict(None)

    def testto_dict_arg(self):
        Bsmodel = BaseModel()
        self.assertNotEqual(Bsmodel.to_dict(), Bsmodel.__dict__)

    def testto_dict_created_at(self):
        Bsmodel = BaseModel()
        DBsmodel = Bsmodel.to_dict()
        self.assertEqual(str, type(DBsmodel["created_at"]))


if __name__ == "__main__":
    unittest.main()
