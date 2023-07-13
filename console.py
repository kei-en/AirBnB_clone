#!/usr/bin/python3
"""Defines the command interpreter"""
import cmd
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Defines the entry point of the command interpreter

    Atrributes:
        prompt (str): Custom command prompt
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel"
    }

    def emptyline(self):
        """Do nothing after getting an empty line"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program (Ctrl-d)"""
        print("")
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()