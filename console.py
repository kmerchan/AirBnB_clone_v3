#!/usr/bin/python3
""" console """

import cmd
from datetime import datetime
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import shlex  # for splitting the line along spaces except in double quotes

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """ Create an object of any class"""
        # split arguments by space to get class name
        args = arg.split()
        # check if class name is missing or not in list of available classes
        if args == []:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        else:
            cls = args[0]
        # if class does exist, create new instance
        new_instance = classes[cls]()
        # if more arguments, resets args without class name
        if len(args) >= 1:
            args = args[1:]
        else:
            # save before returning, in case using FileStorage
            new_instance.save()
            print(new_instance.id)
            return
        # loops through each argument, splitting into key/value pairs
        for argument in args:
            sa = argument.split("=")
            # print("Here is sa: {}".format(sa))
            key = sa[0]
            value = sa[1]
            # if there are underscores in value, changed to spaces
            for i in range(len(value)):
                if value[i] == "_":
                    value = value[:i] + " " + value[i+1:]
            # if there are quotes around key or value, trimmed to remove
            if (key[0] == "'" and key[-1] == "'") or (
                    key[0] == "\"" and key[-1] == "\""):
                key = key[1:-1]
            if (value[0] == "'" and value[-1] == "'") or (
                    value[0] == "\"" and value[-1] == "\""):
                value = value[1:-1]
            # atrribute is set to that key in the dictionary of objects
            setattr(new_instance, key, value)
        # new object is saved after setting non-nullable attributes
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in storage.all():
                    print(storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in storage.all():
                    storage.all().pop(key)
                    storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints string representations of instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = storage.all()
        elif args[0] in classes:
            obj_dict = storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value"""
        args = shlex.split(arg)
        integers = ["number_rooms", "number_bathrooms", "max_guest",
                    "price_by_night"]
        floats = ["latitude", "longitude"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] == "Place":
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except:
                                        args[3] = 0.0
                            setattr(storage.all()[k], args[2], args[3])
                            storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_count(self, args=None):
        """Count current number of class instances"""
        if args in classes:
            print(storage.count(classes[args]))
        else:
            print(storage.count(None))

    def help_count(self):
        """ Provides more direction for how to use count method """
        print("Usage: count <class_name>")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
