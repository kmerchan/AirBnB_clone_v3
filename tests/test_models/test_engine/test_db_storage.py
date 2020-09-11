#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
from models import storage, storage_t
from models.engine.db_storage import DBStorage, __doc__ as db_storage_doc
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
from unittest import TestCase, skipIf
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
        self.assertIsNot(db_storage_doc, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage_doc) >= 1,
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
        self.assertIs(type(storage.all()), dict)

    @skipIf(storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @skipIf(storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @skipIf(storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


class test_dbStorage(TestCase):
    """ Class to test the database storage method """
    @skipIf(storage_t != 'db', "not testing db storage")
    def test_new(self):
        """ New object is correctly added to database """
        db = MySQLdb.connect(host="localhost", user="hbnb_test",
                             passwd="hbnb_test_pwd", db="hbnb_test_db")
        cur = db.cursor()
        cur.execute("""SELECT * FROM states""")
        count1 = cur.fetchall()
        new = State()
        new.name = "New York"
        new.save()
        cur.close()
        db.close()
        db = MySQLdb.connect(host="localhost", user="hbnb_test",
                             passwd="hbnb_test_pwd", db="hbnb_test_db")
        cur = db.cursor()
        cur.execute("""SELECT * FROM states""")
        count2 = cur.fetchall()
        self.assertEqual(len(count1) + 1, len(count2))
        cur.close()
        db.close()

    @skipIf(storage_t != 'db', "not testing db storage")
    def test_all(self):
        # tests storage.all() with cls argument, with no cls instances
        all_states = storage.all(State)
        db = MySQLdb.connect(host="localhost", user="hbnb_test",
                             passwd="hbnb_test_pwd", db="hbnb_test_db")
        cur = db.cursor()
        cur.execute("""SELECT * FROM states""")
        count = cur.fetchall()
        self.assertEqual(len(all_states.keys()), len(count))
        # creates cls instance and retests storage.all() with cls
        new_state = State()
        new_state.name = "California"
        new_state.save()
        all_states = storage.all(State)
        # tests that storage.all returns dictionary of objects and key
        self.assertIsInstance(storage.all(), dict)
        dict_key = "{}.{}".format("State", new_state.id)
        self.assertIn(dict_key, storage.all())
        self.assertEqual(len(all_states.keys()), len(count) + 1)
        self.assertEqual("California",
                         all_states.get("State.{}".format(new_state.id)).name)
        cur.close()
        db.close()
        db = MySQLdb.connect(host="localhost", user="hbnb_test",
                             passwd="hbnb_test_pwd", db="hbnb_test_db")
        cur = db.cursor()
        cur.execute("""SELECT * FROM states""")
        count2 = cur.fetchall()
        self.assertEqual(len(count) + 1, len(count2))
        # tests delete method
        storage.delete(new_state)
        all_states = storage.all(State)
        self.assertEqual(len(all_states.keys()), len(count))
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
                             passwd="hbnb_test_pwd", db="hbnb_test_db")
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
        self.assertIn("State.{}".format(new.id), storage.all(State).keys())
        self.assertEqual(storage.all().get("State.{}".
                                           format(new.id)).name, "testing")

    @skipIf(storage_t != 'db', "not testing db storage")
    def test_key_format(self):
        """ Key is properly formatted """
        new = State()
        new.name = "Maine"
        new.save()
        for key in storage.all().keys():
            if new.id in key:
                self.assertEqual(key, 'State' + '.' + new.id)

    @skipIf(storage_t != 'db', "not testing db storage")
    def test_storage_var_created(self):
        """ DBStorage object storage created """
        self.assertEqual(type(storage), DBStorage)

    def test_storage_count_method(self):
        """tests FileStorage count method"""
        # gets initial counts of all objects and all State objects in storage
        count = storage.count()
        count_state = storage.count(State)
        # creates new instance of State and saves to database
        new = State()
        new.name = "Idaho"
        new.save()
        # tests if count increased for both all and State objects
        self.assertEqual(storage.count(), count + 1)
        self.assertEqual(storage.count(State), count_state + 1)

    def test_storage_get_method(self):
        """tests FileStorage get method to retrieve one object"""
        # tests get method when id is not found
        self.assertIs(storage.get(State, -89), None)
        # creates new instance of State and saves to database
        new = State()
        new.name = "Oklahoma"
        new.save()
        # tests get method with valid class name and id
        got_obj = storage.get(State, new.id)
        self.assertIs(type(got_obj), State)
        self.assertEqual(got_obj.id, new.id)
