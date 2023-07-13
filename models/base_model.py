#!/usr/bin/python3
"""Type module of BaseModel"""

import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents the BaseModel of HBnB project."""

    def __init__(self, *args, **kwargs):
        """Type initialize"""
        tformat = "%Y-%m-%dT%H:%M:%S.%f"
        if len(kwargs) != 0:
            for key, val in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(val, tformat))
                elif key != '__class__':
                    setattr(self, key, val)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.today()
            self.updated_at = datetime.today()
            models.storage.new(self)

    def save(self):
        """Type method save"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Type to_dict"""
        rtn_dict = self.__dict__.copy()
        rtn_dict["created_at"] = self.created_at.isoformat()
        rtn_dict["updated_at"] = self.updated_at.isoformat()
        rtn_dict["__class__"] = self.__class__.__name__
        return rtn_dict

    def __str__(self):
        """Return the print/str rep ofBaseModel instance"""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
