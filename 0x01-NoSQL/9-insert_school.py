#!/usr/bin/env python3
"""Defines the function insert_school"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a document into a collection"""

    id = mongo_collection.insert_one(kwargs).inserted_id

    return id
