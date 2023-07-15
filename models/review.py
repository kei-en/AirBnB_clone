#!/usr/bin/python3
"""This is the Review class.
Has the Review class that inherits from BaseModel.
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """This class defines a Review.
    Attributes:
        place_id (str)
        user_id (str)
    """

    place_id = ""
    user_id = ""
    text = ""
