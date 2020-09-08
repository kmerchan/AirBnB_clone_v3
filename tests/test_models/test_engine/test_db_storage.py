#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
from models import storage, storage_t
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import MySQLdb
import os
import pep8
from unittest import TestCase
from unittest import skipIf
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(TestCase):
    """Test the FileStorage class"""
    @skipIf(storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)


class test_dbStorage(TestCase):
    """ Class to test the database storage method """
    @skipIf(storage_t != 'db', "not testing db storage")
    def test_new(self):
        """ New object is correctly added to database """
        db = MySQLdb.connect(host="localhost", user="hbnb_test",
                             passwd="hbnb_test_pwd", db="hbnb_test_db")
        cur = db.cursor()
        cur.execute("""SELECT COUNT(*) FROM states""")
        count1 = cur.fetchall()
        new = State()
        new.save()
        cur.execute("""SELECT COUNT(*) FROM states""")
        count2 = cur.fetchall()
        self.assertEqual(count1 + 1, count2)
        cur.close()
        db.close()

    @skipIf(storage_t != 'db', "not testing db storage")
    def test_all(self):
        """ __objects is properly returned """
        # tests that storage.all() returns dictionary of objects
        new = BaseModel()
        new.save()
        temp = storage.all()
        self.assertIsInstance(temp, dict)
        dict_key = "{}.{}".format("BaseModel", new.id)
        self.assertIn(dict_key, temp)

        # tests storage.all() with cls argument, with no cls instances
        all_states = storage.all(State)
        db = MySQLdb.connect(host="localhost", user="hbnb_test",
                             passwd="hbnb_test_pd", db="hbnb_test_db")
        cur = db.cursor()
        cur.execute("""SELECT COUNT(*) FROM states""")
        count = cur.fetchall()
        self.assertEqual(len(all_states.keys()), count)
        # creates cls instance and retests storage.all() with cls
        new_state = State()
        new_state.name = "California"
        new_state.save()
        all_states = storage.all(State)
        self.assertEqual(len(all_states.keys()), count + 1)
        for k, v in all_states.items():
            self.assertEqual("California", v.name)
        cur.execute("""SELECT COUNT(*) FROM states""")
        count2 = cur.fetchall()
        self.assertEqual(count + 1, count2)
        # tests delete method
        storage.delete(new_state)
        all_states = storage.all(State)
        self.assertEqual(len(all_states.keys()), count)
        cur.close()
        db.close()

    @skipIf(storage_t != 'db', "not testing db storage")
    def test_empty(self):
        """ Data is saved to database """
        new = State()
        new.name = "California"
        new.save()
        C_id = new.id
        db = MySQLdb.connect(host="localhost", user="hbnb_test",
                             passwd="hbnb_test_pd", db="hbnb_test_db")
        cur = db.cursor()
        cur.execute("""SELECT COUNT(*) FROM states""")
        count = cur.fetchall()
        self.assertNotEqual(count, 0)
        cur.close()
        db.close()

    @skipIf(storage_t != 'db', "not testing db storage")
    def test_reload(self):
        """ Storage database is successfully loaded to __objects """
        new = State()
        new.name = "testing"
        new.save()
        storage.reload()
        self.assertIn("testing", storage.all(State).values())

    @skipIf(storage_t != 'db', "not testing db storage")
    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    @skipIf(storage_t != 'db', "not testing db storage")
    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        new.save()
        _id = new.id
        for key in storage.all().keys():
            temp = key
            if _id in key:
                self.assertEqual(temp, 'BaseModel' + '.' + _id)

    @skipIf(storage_t != 'db', "not testing db storage")
    def test_storage_var_created(self):
        """ DBStorage object storage created """
        from models.engine.db_storage import DBStorage
        print(type(storage))
        self.assertEqual(type(storage), DBStorage)
