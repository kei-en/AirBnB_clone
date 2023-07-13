#!/usr/bin/python3
"""Defines the command interpreter"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


def parse(args):
    cbraces = re.search(r"\{(.*?)\}", args)
    brackets = re.search(r"\[(.*?)\]", args)
    if cbraces is None:
        if brackets is None:
            return [i.strip(",") for i in split(args)]

        lex = split(args[:brackets.span()[0]])
        rtnl = [i.strip(",") for i in lex]
        rtnl.append(brackets.group())
        return rtnl

    lex = split(args[:cbraces.span()[0]])
    rtnl = [i.strip(",") for i in lex]
    rtnl.append(cbraces.group())
    return rtnl


class HBNBCommand(cmd.Cmd):
    """Defines the entry point of the command interpreter

    Atrributes:
        prompt (str): Custom command prompt
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing after getting an empty line"""
        pass

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, args):
        """EOF signal to exit the program (Ctrl-d)"""
        print("")
        return True

    def default(self, args):
        """Default behaviour for cmd module when input is invalid"""
        argsdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", args)
        if match is not None:
            arg = [args[:match.span()[0]], args[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg[1])
            if match is not None:
                cmnd = [arg[1][:match.span()[0]], match.group()[1:-1]]
                if cmnd[0] in argsdict.keys():
                    call = "{} {}".format(arg[0], cmnd[1])
                    return argsdict[cmnd[0]](call)
        print("** Uknown syntax: {}".format(arg))
        return False

    def do_create(self, args):
        """Usage: create <class>
        Create a new class instance and print its id
        """
        arg = parse(args)
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg[0])().id)
            storage.save()

    def do_show(self, args):
        """Usage: show <class> <id> or <class>.show(<id>)
        Print the string representation of a class instance of a given id
        """
        arg = parse(args)
        objdict = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg[0], arg[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(arg[0], arg[1])])

    def do_destroy(self, args):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id
        """
        arg = parse(args)
        objdict = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg[0], arg[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(arg[0], arg[1])]
            storage.save()

    def do_all(self, args):
        """Usage: all <class> or all or <class>.all()
        Print all string representation of all instances
        based or not on the class name
        """
        arg = parse(args)
        if len(arg) > 0 and arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objlist = []
            for obj in storage.all().values():
                if len(arg) > 0 and arg[0] == obj.__class__.__name__:
                    objlist.append(obj.__str__())
                elif len(arg) == 0:
                    objlist.append(obj.__str__())
            print(objlist)

    def do_count(self, args):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of  given class
        """
        arg = parse(args)
        count = 0
        for obj in storage.all().values():
            if arg[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, args):
        """Usage: update <class> <id> <attr_name> <attr_value> or
        <class>.update(<id>, <attr_name>, <atrr_value>) or
        <class>.update(<id>, <dictionary>)
        Update an instance based on the class name and id
        by adding or updating attribute
        """
        arg = parse(args)
        objdict = storage.all()

        if len(arg) == 0:
            print("** class name missing **")
            return False
        if arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg[0], arg[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(arg) == 2:
            print("** attribute name missing **")
            return False
        if len(arg) == 3:
            try:
                type(eval(arg[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg) == 4:
            obj = objdict["{}.{}".format(arg[0], arg[1])]
            if arg[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arg[2]])
                obj.__dict__[arg[2]] = valtype(arg[3])
            else:
                obj.__dict__[arg[2]] = arg[3]
        elif type(eval(arg[2])) == dict:
            obj = objdict["{}.{}".format(arg[0], arg[1])]
            for k, v in eval(arg[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
