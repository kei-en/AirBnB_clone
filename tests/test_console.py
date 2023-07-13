#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
    TestHBNBCommand_prompting
    TestHBNBCommand_help
    TestHBNBCommand_exit
    TestHBNBCommand_create
    TestHBNBCommand_show
    TestHBNBCommand_all
    TestHBNBCommand_destroy
    TestHBNBCommand_update
"""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommand_prompting(unittest.TestCase):
    """Unittests for testing prompts input to the HBNB command interpreter."""

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", op.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
    """Unittests for testing help messages of the HBNB command interpreter."""

    def test_help_quit(self):
        hlp = "Quit command to exit the program"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(hlp, op.getvalue().strip())

    def test_help_EOF(self):
        hlp = "EOF signal to exit the program"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(hlp, op.getvalue().strip())

    def test_help_create(self):
        hlp = ("Usage: create <class>"
               "\n        Create a new class instance and print its id")
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(hlp, op.getvalue().strip())

    def test_help_show(self):
        hlp = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
               "Print the string representation of a class instance of a "
               "given id")
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(hlp, op.getvalue().strip())

    def test_help_destroy(self):
        hlp = ("Usage: destroy <class> <id> or <class>.destroy(<id>)"
               "\n        Delete a class instance of a given id")
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(hlp, op.getvalue().strip())

    def test_help_all(self):
        hlp = ("Usage: all <class> or all or <class>.all()"
               "\n        Print all string representation of all instances"
               "\n        based or not on the class name")
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(hlp, op.getvalue().strip())

    def test_help_count(self):
        hlp = ("Usage: count <class> or <class>.count()"
               "\n        Retrieve the number of instances of  given class")
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(hlp, op.getvalue().strip())

    def test_help_update(self):
        hlp = ("Usage: update <class> <id> <attr_name> <attr_value> or"
               "\n        <class>.update(<id>, <attr_name>, <atrr_value>) or"
               "\n        <class>.update(<id>, <dictionary>)"
               "\n        Update an instance based on the class name and id"
               "\n        by adding or updating attribute")
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(hlp, op.getvalue().strip())

    def test_help(self):
        hlp = ("Documented commands (type help <topic>):\n"
               "========================================\n"
               "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(hlp, op.getvalue().strip())


class TestHBNBCommand_exit(unittest.TestCase):
    """Unittests for testing exiting from the HBNB command interpreter."""

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_create(unittest.TestCase):
    """Unittests for testing create from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_create_missing_class(self):
        ok = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_create_invalid_class(self):
        ok = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_create_invalid_syntax(self):
        ok = "** Unknown syntax: ['MyModel', 'create()']"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(ok, op.getvalue().strip())
        ok = "** Unknown syntax: ['BaseModel', 'create()']"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_create_object(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(op.getvalue().strip()))
            test_key = "BaseModel.{}".format(op.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(op.getvalue().strip()))
            test_key = "User.{}".format(op.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(op.getvalue().strip()))
            test_key = "State.{}".format(op.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(op.getvalue().strip()))
            test_key = "City.{}".format(op.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(op.getvalue().strip()))
            test_key = "Amenity.{}".format(op.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(op.getvalue().strip()))
            test_key = "Place.{}".format(op.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(op.getvalue().strip()))
            test_key = "Review.{}".format(op.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())


class TestHBNBCommand_show(unittest.TestCase):
    """Unittests for testing show from the HBNB command interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_show_missing_class(self):
        ok = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_show_invalid_class(self):
        ok = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_show_missing_id_space_notation(self):
        ok = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_show_missing_id_dot_notation(self):
        ok = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_show_no_instance_found_space_notation(self):
        ok = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_show_no_instance_found_dot_notation(self):
        ok = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            cmnd = "show BaseModel {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["User.{}".format(test_id)]
            cmnd = "show User {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["State.{}".format(test_id)]
            cmnd = "show State {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["Place.{}".format(test_id)]
            cmnd = "show Place {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["City.{}".format(test_id)]
            cmnd = "show City {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["Amenity.{}".format(test_id)]
            cmnd = "show Amenity {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["Review.{}".format(test_id)]
            cmnd = "show Review {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            cmnd = "BaseModel.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["User.{}".format(test_id)]
            cmnd = "User.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["State.{}".format(test_id)]
            cmnd = "State.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["Place.{}".format(test_id)]
            cmnd = "Place.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["City.{}".format(test_id)]
            cmnd = "City.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["Amenity.{}".format(test_id)]
            cmnd = "Amenity.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["Review.{}".format(test_id)]
            cmnd = "Review.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertEqual(obj.__str__(), op.getvalue().strip())


class TestHBNBCommand_destroy(unittest.TestCase):
    """Unittests for testing destroy from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        FileStorage.__objects = {}

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
        storage.reload()

    def test_destroy_missing_class(self):
        ok = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_destroy_invalid_class(self):
        ok = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_destroy_id_missing_space_notation(self):
        ok = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_destroy_id_missing_dot_notation(self):
        ok = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_destroy_invalid_id_space_notation(self):
        ok = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_destroy_invalid_id_dot_notation(self):
        ok = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_destroy_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            cmnd = "destroy BaseModel {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["User.{}".format(test_id)]
            cmnd = "show User {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["State.{}".format(test_id)]
            cmnd = "show State {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["Place.{}".format(test_id)]
            cmnd = "show Place {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["City.{}".format(test_id)]
            cmnd = "show City {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["Amenity.{}".format(test_id)]
            cmnd = "show Amenity {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["Review.{}".format(test_id)]
            cmnd = "show Review {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())

    def test_destroy_objects_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            cmnd = "BaseModel.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["User.{}".format(test_id)]
            cmnd = "User.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["State.{}".format(test_id)]
            cmnd = "State.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["Place.{}".format(test_id)]
            cmnd = "Place.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["City.{}".format(test_id)]
            cmnd = "City.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["Amenity.{}".format(test_id)]
            cmnd = "Amenity.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            obj = storage.all()["Review.{}".format(test_id)]
            cmnd = "Review.destory({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(cmnd))
            self.assertNotIn(obj, storage.all())


class TestHBNBCommand_all(unittest.TestCase):
    """Unittests for testing all of the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_all_invalid_class(self):
        ok = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_all_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", op.getvalue().strip())
            self.assertIn("User", op.getvalue().strip())
            self.assertIn("State", op.getvalue().strip())
            self.assertIn("Place", op.getvalue().strip())
            self.assertIn("City", op.getvalue().strip())
            self.assertIn("Amenity", op.getvalue().strip())
            self.assertIn("Review", op.getvalue().strip())

    def test_all_objects_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(".all()"))
            self.assertIn("BaseModel", op.getvalue().strip())
            self.assertIn("User", op.getvalue().strip())
            self.assertIn("State", op.getvalue().strip())
            self.assertIn("Place", op.getvalue().strip())
            self.assertIn("City", op.getvalue().strip())
            self.assertIn("Amenity", op.getvalue().strip())
            self.assertIn("Review", op.getvalue().strip())

    def test_all_single_object_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", op.getvalue().strip())
            self.assertNotIn("User", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", op.getvalue().strip())
            self.assertNotIn("BaseModel", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", op.getvalue().strip())
            self.assertNotIn("BaseModel", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", op.getvalue().strip())
            self.assertNotIn("BaseModel", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", op.getvalue().strip())
            self.assertNotIn("BaseModel", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", op.getvalue().strip())
            self.assertNotIn("BaseModel", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", op.getvalue().strip())
            self.assertNotIn("BaseModel", op.getvalue().strip())

    def test_all_single_object_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", op.getvalue().strip())
            self.assertNotIn("User", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", op.getvalue().strip())
            self.assertNotIn("BaseModel", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", op.getvalue().strip())
            self.assertNotIn("BaseModel", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", op.getvalue().strip())
            self.assertNotIn("BaseModel", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", op.getvalue().strip())
            self.assertNotIn("BaseModel", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", op.getvalue().strip())
            self.assertNotIn("BaseModel", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", op.getvalue().strip())
            self.assertNotIn("BaseModel", op.getvalue().strip())


class TestHBNBCommand_update(unittest.TestCase):
    """Unittests for testing update from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_update_missing_class(self):
        ok = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_update_invalid_class(self):
        ok = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_update_missing_id_space_notation(self):
        ok = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_update_missing_id_dot_notation(self):
        ok = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_update_invalid_id_space_notation(self):
        ok = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update User 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update State 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update City 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update Place 1"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("update Review 1"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_update_invalid_id_dot_notation(self):
        ok = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("User.update(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("State.update(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("City.update(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
            self.assertEqual(ok, op.getvalue().strip())

    def test_update_missing_attr_name_space_notation(self):
        ok = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = op.getvalue().strip()
            test_cmnd = "update BaseModel {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = op.getvalue().strip()
            test_cmnd = "update User {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = op.getvalue().strip()
            test_cmnd = "update State {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = op.getvalue().strip()
            test_cmnd = "update City {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = op.getvalue().strip()
            test_cmnd = "update Amenity {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = op.getvalue().strip()
            test_cmnd = "update Place {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())

    def test_update_missing_attr_name_dot_notation(self):
        ok = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = op.getvalue().strip()
            test_cmnd = "BaseModel.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = op.getvalue().strip()
            test_cmnd = "User.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = op.getvalue().strip()
            test_cmnd = "State.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = op.getvalue().strip()
            test_cmnd = "City.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = op.getvalue().strip()
            test_cmnd = "Amenity.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = op.getvalue().strip()
            test_cmnd = "Place.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())

    def test_update_missing_attr_value_space_notation(self):
        ok = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create BaseModel")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "update BaseModel {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create User")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "update User {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create State")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "update State {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create City")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "update City {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Amenity")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "update Amenity {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "update Place {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Review")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "update Review {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())

    def test_update_missing_attr_value_dot_notation(self):
        ok = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create BaseModel")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "BaseModel.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create User")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "User.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create State")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "State.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create City")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "City.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Amenity")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "Amenity.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "Place.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Review")
            test_id = op.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as op:
            test_cmnd = "Review.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(test_cmnd))
            self.assertEqual(ok, op.getvalue().strip())

    def test_update_valid_string_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create BaseModel")
            test_id = op.getvalue().strip()
        test_cmnd = "update BaseModel {} attr_name 'attr_value'".format(
            test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["BaseModel.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create User")
            test_id = op.getvalue().strip()
        test_cmnd = "update User {} attr_name 'attr_value'".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["User.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create State")
            test_id = op.getvalue().strip()
        test_cmnd = "update State {} attr_name 'attr_value'".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["State.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create City")
            test_id = op.getvalue().strip()
        test_cmnd = "update City {} attr_name 'attr_value'".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["City.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        test_cmnd = "update Place {} attr_name 'attr_value'".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Amenity")
            test_id = op.getvalue().strip()
        test_cmnd = "update Amenity {} attr_name 'attr_value'".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["Amenity.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Review")
            test_id = op.getvalue().strip()
        test_cmnd = "update Review {} attr_name 'attr_value'".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["Review.{}".format(test_id)].__dict__
        self.assertTrue("attr_value", test_dict["attr_name"])

    def test_update_valid_string_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create BaseModel")
            test_id = op.getvalue().strip()
        test_cmnd = "BaseModel.update({}, attr_name, 'attr_value')".format(
            test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["BaseModel.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create User")
            test_id = op.getvalue().strip()
        test_cmnd = "User.update({}, attr_name, 'attr_value')".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["User.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create State")
            test_id = op.getvalue().strip()
        test_cmnd = "State.update({}, attr_name, 'attr_value')".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["State.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create City")
            test_id = op.getvalue().strip()
        test_cmnd = "City.update({}, attr_name, 'attr_value')".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["City.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        test_cmnd = "Place.update({}, attr_name, 'attr_value')".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Amenity")
            test_id = op.getvalue().strip()
        test_cmnd = "Amenity.update({}, attr_name, 'attr_value')".format(
            test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["Amenity.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Review")
            test_id = op.getvalue().strip()
        test_cmnd = "Review.update({}, attr_name, 'attr_value')".format(
            test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["Review.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_int_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        test_cmnd = "update Place {} max_guest 98".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_int_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        test_cmnd = "Place.update({}, max_guest, 98)".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_float_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        test_cmnd = "update Place {} latitude 7.2".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_float_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        test_cmnd = "Place.update({}, latitude, 7.2)".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmnd))
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_dictionary_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create BaseModel")
            test_id = op.getvalue().strip()
        test_cmnd = "update BaseModel {} ".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["BaseModel.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create User")
            test_id = op.getvalue().strip()
        test_cmnd = "update User {} ".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["User.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create State")
            test_id = op.getvalue().strip()
        test_cmnd = "update State {} ".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["State.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create City")
            test_id = op.getvalue().strip()
        test_cmnd = "update City {} ".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["City.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        test_cmnd = "update Place {} ".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Amenity")
            test_id = op.getvalue().strip()
        test_cmnd = "update Amenity {} ".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["Amenity.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Review")
            test_id = op.getvalue().strip()
        test_cmnd = "update Review {} ".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["Review.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create BaseModel")
            test_id = op.getvalue().strip()
        test_cmnd = "BaseModel.update({}".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["BaseModel.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create User")
            test_id = op.getvalue().strip()
        test_cmnd = "User.update({}, ".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["User.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create State")
            test_id = op.getvalue().strip()
        test_cmnd = "State.update({}, ".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["State.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create City")
            test_id = op.getvalue().strip()
        test_cmnd = "City.update({}, ".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["City.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        test_cmnd = "Place.update({}, ".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Amenity")
            test_id = op.getvalue().strip()
        test_cmnd = "Amenity.update({}, ".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["Amenity.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Review")
            test_id = op.getvalue().strip()
        test_cmnd = "Review.update({}, ".format(test_id)
        test_cmnd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["Review.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_with_int_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        test_cmnd = "update Place {} ".format(test_id)
        test_cmnd += "{'max_guest': 98})"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_int_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        test_cmnd = "Place.update({}, ".format(test_id)
        test_cmnd += "{'max_guest': 98})"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_float_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        test_cmnd = "update Place {} ".format(test_id)
        test_cmnd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])

    def test_update_valid_dictionary_with_float_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as op:
            HBNBCommand().onecmd("create Place")
            test_id = op.getvalue().strip()
        test_cmnd = "Place.update({}, ".format(test_id)
        test_cmnd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(test_cmnd)
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])


class TestHBNBCommand_count(unittest.TestCase):
    """Unittests for testing count method of HBNB comand interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

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

    def test_count_invalid_class(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertEqual("0", op.getvalue().strip())

    def test_count_object(self):
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertEqual("1", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertEqual("1", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertEqual("1", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertEqual("1", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", op.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as op:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertEqual("1", op.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
