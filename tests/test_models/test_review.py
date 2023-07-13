#!/usr/bin/python3
"""
Unittest for review module
"""
import os
import pep8
import unittest
from models.review import Review
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class Test_Review(unittest.TestCase):
    """ Test for
    Review Class """

    rvw = Review()

    def setUp(self):
        """set up the
        test for testing Reviews"""
        FileStorage._FileStorage__file_path = "test.json"
        self.review = Review()
        self.review.place_id = "12"
        self.review.user_id = "13"
        self.review.text = "good"
        self.review.save()

    def test_atrr_type_review(self):
        """test attribute for Review"""
        self.assertEqual(type(self.rvw.place_id), str)
        self.assertEqual(type(self.rvw.user_id), str)
        self.assertEqual(type(self.rvw.text), str)

    def test_attribute_place_id(self):
        """ Tests attr """
        self.assertEqual(hasattr(self.rvw, "place_id"), True)
        self.assertEqual(hasattr(self.rvw, "user_id"), True)
        self.assertEqual(hasattr(self.rvw, "text"), True)

    def test_subcls_Review(self):
        """subclass  BaseModel"""
        self.assertTrue(issubclass(self.review.__class__, BaseModel), True)
        self.assertIsInstance(self.review, Review)

    def test_pep8_conformance_review(self):
        """Test that model is right by PEP8."""
        pep8s = pep8.StyleGuide(okay=True)
        result = pep8s.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0, "Found errors.")

    def test_docstring_Review(self):
        """checking for docstrings"""
        self.assertIsNotNone(Review.__doc__)

    def testpublic(self):
        self.assertEqual(str, type(Review().id))


if __name__ == "__main__":
    unittest.main()
