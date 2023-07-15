#!/usr/bin/python3
"""Class that
represent
the user"""

from models.base_model import BaseModel


class User(BaseModel):
    """user class
    instance
    of basemodel class"""

    email = ''
    password = ''
    first_name = ''
    last_name = ''
