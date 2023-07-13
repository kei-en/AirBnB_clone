#!/usr/bin/python3
"""
Unittest for amenity module
"""
import os
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.amenity import Amenity


class Test_Amenity(unittest.TestCase):
    """ Test for
    Amenity Class """

    eg = Amenity()

    def setUp(self):
        """set up the
        test for testing amenities"""
        FileStorage._FileStorage__file_path = "test.json"
        self.amenity = Amenity()
        self.amenity.name = "Goods"
        self.amenity.save()

    def test_class_existance(self):
        """tests if class exists"""
        result = "<class 'models.amenity.Amenity'>"
        self.assertEqual(str(type(self.eg)), result)

    def testpublic(self):
        self.assertEqual(str, type(Amenity().id))

    def test_instance_User(self):
        """ Test subclasses of BaseModel """
        self.assertIsInstance(self.eg, Amenity)

    def test_atrr_type_Amenity(self):
        """test type for Amenity"""
        self.assertEqual(type(self.amenity.name), str)

    def test_attribute_name(self):
        """ Check name """
        self.assertEqual(hasattr(self.eg, "name"), True)

    def test_types(self):
        """ test type """
        self.assertEqual(type(self.eg.name), str)

    def test_str(self):
        eg = Amenity()
        """test that the str method has the correct output"""
        string = "[Amenity] ({}) {}".format(eg.id, eg.__dict__)
        self.assertEqual(string, str(eg))

    def testHasAttributes(self):
        """verify attributes"""
        self.assertTrue(hasattr(self.eg, 'name'))
        self.assertTrue(hasattr(self.amenity, 'id'))
        self.assertTrue(hasattr(self.eg, 'created_at'))
        self.assertTrue(hasattr(self.amenity, 'updated_at'))


if __name__ == "__main__":
    unittest.main()
