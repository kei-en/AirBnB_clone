#!/usr/bin/python3
"""This is the Review.
Has the Review class that inherits from BaseModel.
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """This defines a Review.
    Attributes:
        place_id (str)
        user_id (str)
    """

    place_id = ""
    user_id = ""
    text = ""
