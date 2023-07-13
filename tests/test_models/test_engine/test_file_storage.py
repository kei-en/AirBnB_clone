#!/usr/bin/python3
"""
Unittest for base module
"""
import json
import unittest
import os
import models
from datetime import datetime
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.state import State
from models.review import Review
from models.city import City


class Test_FileStorage(unittest.TestCase):
    """ Test for
    File_Storage Class """

    def setUp(self):
        """ set up the
        test for testing File_Storage """
        FileStorage._FileStorage__file_path = "file.json"

    def test_noarg(self):
        self.assertEqual(FileStorage, type(FileStorage()))

    def test_init(self):
        self.assertEqual(FileStorage, type(models.storage))

    def test_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_obj(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_path(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))


class Test_FileStorage_m(unittest.TestCase):

    @classmethod
    def SetUp(self):
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
            os.rename("temp", "file_json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new_all_cls(self):
        Bsmodel = BaseModel()
        models.storage.new(Bsmodel)
        models.storage.new(Amenity())
        models.storage.new(Place())
        models.storage.new(User())
        models.storage.new(State())
        models.storage.new(Review())
        models.storage.new(City())
        self.assertIn("BaseModel." + Bsmodel.id, models.storage.all().keys())
        self.assertIn(Bsmodel, models.storage.all().values())
        self.assertIn(Bsmodel, models.storage.all().values())
        self.assertIn("Amenity." + Amenity().id, models.storage.all().keys())
        self.assertIn(Amenity(), models.storage.all().values())
        self.assertIn("Place." + Place().id, models.storage.all().keys())
        self.assertIn(Place(), models.storage.all().values())
        self.assertIn("User." + User().id, models.storage.all().keys())
        self.assertIn(User(), models.storage.all().values())
        self.assertIn("State." + State().id, models.storage.all().keys())
        self.assertIn(State(), models.storage.all().values())
        self.assertIn("Review." + Review().id, models.storage.all().keys())
        self.assertIn(Review(), models.storage.all().values())
        self.assertIn("City." + City().id, models.storage.all().keys())
        self.assertIn(City(), models.storage.all().values())

    def testsave_args(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def testnew_none(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def testnew_arg(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def testsave(self):
        Bsmodel = BaseModel()
        Ame = Amenity()
        Pla = Place()
        Usr = User()
        Sta = State()
        Rvw = Review()
        Cty = City()
        models.storage.save()
        models.storage.new(Bsmodel)
        models.storage.new(Ame)
        models.storage.new(Pla)
        models.storage.new(Usr)
        models.storage.new(Sta)
        models.storage.new(Rvw)
        models.storage.new(Cty)
        bsave = ""
        with open("file.json", "r") as f:
            bsave = f.read()
        self.assertIn("BaseModel." + Bsmodel.id, bsave)
        self.assertIn("Amenity." + Ame.id, bsave)
        self.assertIn("Place." + Pla.id, bsave)
        self.assertIn("User." + Usr.id, bsave)
        self.assertIn("State." + Sta.id, bsave)
        self.assertIn("Review." + Rvw.id, bsave)
        self.assertIn("City." + Cty.id, bsave)

    def testreload(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)

    def test_reload(self):
        if os.path.exists("file.json"):
            os.remove("file.json")
        storage.save()
        storage.reload()
        all_objs = storage.all()
        for obj_id in all_objs.keys():
            obj = all_objs[obj_id]
            self.assertTrue(isinstance(obj, BaseModel))
            os.remove("file.json")

    def test_reload(self):
        Bsmodel = BaseModel()
        Ame = Amenity()
        Pla = Place()
        Usr = User()
        Sta = State()
        Rvw = Review()
        Cty = City()
        models.storage.reload()
        models.storage.save()
        models.storage.new(Bsmodel)
        models.storage.new(Ame)
        models.storage.new(Pla)
        models.storage.new(Usr)
        models.storage.new(Sta)
        models.storage.new(Rvw)
        models.storage.new(Cty)
        obj = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + Bsmodel.id, obj)
        self.assertIn("Amenity." + Ame.id, obj)
        self.assertIn("Place." + Pla.id, obj)
        self.assertIn("User." + Usr.id, obj)
        self.assertIn("State." + Sta.id, obj)
        self.assertIn("Review." + Rvw.id, obj)
        self.assertIn("City." + Cty.id, obj)

    def testsave_args(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def testnew_none(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def testnew_arg(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def testsave(self):
        Bsmodel = BaseModel()
        Ame = Amenity()
        Pla = Place()
        Usr = User()
        Sta = State()
        Rvw = Review()
        Cty = City()
        models.storage.save()
        models.storage.new(Bsmodel)
        models.storage.new(Ame)
        models.storage.new(Pla)
        models.storage.new(Usr)
        models.storage.new(Sta)
        models.storage.new(Rvw)
        models.storage.new(Cty)
        bsave = ""
        with open("file.json", "r") as f:
            bsave = f.read()
        self.assertIn("BaseModel." + Bsmodel.id, bsave)
        self.assertIn("Amenity." + Ame.id, bsave)
        self.assertIn("Place." + Pla.id, bsave)
        self.assertIn("User." + Usr.id, bsave)
        self.assertIn("State." + Sta.id, bsave)
        self.assertIn("Review." + Rvw.id, bsave)
        self.assertIn("City." + Cty.id, bsave)

    def testreload(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)

    def test_reload(self):
        Bsmodel = BaseModel()
        Ame = Amenity()
        Pla = Place()
        Usr = User()
        Sta = State()
        Rvw = Review()
        Cty = City()
        models.storage.reload()
        models.storage.save()
        models.storage.new(Bsmodel)
        models.storage.new(Ame)
        models.storage.new(Pla)
        models.storage.new(Usr)
        models.storage.new(Sta)
        models.storage.new(Rvw)
        models.storage.new(Cty)
        obj = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + Bsmodel.id, obj)
        self.assertIn("Amenity." + Ame.id, obj)
        self.assertIn("Place." + Pla.id, obj)
        self.assertIn("User." + Usr.id, obj)
        self.assertIn("State." + Sta.id, obj)
        self.assertIn("Review." + Rvw.id, obj)
        self.assertIn("City." + Cty.id, obj)

    def testsave_args(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def testnew_none(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def testnew_arg(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def testsave(self):
        Bsmodel = BaseModel()
        Ame = Amenity()
        Pla = Place()
        Usr = User()
        Sta = State()
        Rvw = Review()
        Cty = City()
        models.storage.save()
        models.storage.new(Bsmodel)
        models.storage.new(Ame)
        models.storage.new(Pla)
        models.storage.new(Usr)
        models.storage.new(Sta)
        models.storage.new(Rvw)
        models.storage.new(Cty)
        bsave = ""
        with open("file.json", "r") as f:
            bsave = f.read()
        self.assertIn("BaseModel." + Bsmodel.id, bsave)
        self.assertIn("Amenity." + Ame.id, bsave)
        self.assertIn("Place." + Pla.id, bsave)
        self.assertIn("User." + Usr.id, bsave)
        self.assertIn("State." + Sta.id, bsave)
        self.assertIn("Review." + Rvw.id, bsave)
        self.assertIn("City." + Cty.id, bsave)

    def testreload(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)

    def test_reload(self):
        if os.path.exists("file.json"):
            os.remove("file.json")
        storage.save()
        storage.reload()
        all_objs = storage.all()
        for obj_id in all_objs.keys():
            obj = all_objs[obj_id]
            self.assertTrue(isinstance(obj, BaseModel))
            os.remove("file.json")

    def test_reload(self):
        Bsmodel = BaseModel()
        Ame = Amenity()
        Pla = Place()
        Usr = User()
        Sta = State()
        Rvw = Review()
        Cty = City()
        models.storage.reload()
        models.storage.save()
        models.storage.new(Bsmodel)
        models.storage.new(Ame)
        models.storage.new(Pla)
        models.storage.new(Usr)
        models.storage.new(Sta)
        models.storage.new(Rvw)
        models.storage.new(Cty)
        obj = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + Bsmodel.id, obj)
        self.assertIn("Amenity." + Ame.id, obj)
        self.assertIn("Place." + Pla.id, obj)
        self.assertIn("User." + Usr.id, obj)
        self.assertIn("State." + Sta.id, obj)
        self.assertIn("Review." + Rvw.id, obj)
        self.assertIn("City." + Cty.id, obj)


if __name__ == "__main__":
    unittest.main()
