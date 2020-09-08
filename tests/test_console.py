#!/usr/bin/python3
"""
Contains the class TestConsoleDocs
"""

import console
from console import HBNBCommand
import inspect
import pep8
from unittest import TestCase
from unittest.mock import patch
from io import StringIO
from models import storage
import os


class TestConsoleDocs(TestCase):
    """Class for testing documentation of the console"""
    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")


class TestHBNBCommandClass(TestCase):
    """ Tests HBNBCommand class """

    def test_do_create(self):
        """ Tests create method """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count State")
            state_count = int(f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count Place")
            place_count = int(f.getvalue())
        # checks error message if no class argument given
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual(f.getvalue(), "** class name missing **\n")
        # checks error message if no class argument is invalid
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BadClassName")
            self.assertEqual(f.getvalue(), "** class doesn't exist **\n")
        # tests obj created successfully when first object
        HBNBCommand().onecmd("create State name=\"California\"")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count State")
            self.assertEqual(f.getvalue(), "{}\n".format(state_count + 1))
        # tests obj created successfully when not first
        HBNBCommand().onecmd("create State name=\"Nevada\"")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count State")
            self.assertEqual(f.getvalue(), "{}\n".format(state_count + 2))
        # tests obj created with different class, saves id
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                "create Place name=\"My_little_house\" number_rooms=4")
            p_id = f.getvalue()
            p_id = p_id[:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count Place")
            self.assertEqual(f.getvalue(), "{}\n".format(place_count + 1))
        # checks that after do_create, obj exists in dictionary
        dict_key = "Place." + p_id
        __objects = storage.all()
        self.assertTrue(dict_key in __objects.keys())
        # tests that underscores in value were changed to spaces
        self.assertEqual(__objects[dict_key].name, "My little house")
