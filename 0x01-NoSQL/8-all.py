#!/usr/bin/env python3
"""Defines list_all"""


def list_all(mongo_collection):
    """Lists all documents in a mongo collection"""

    docs = mongo_collection.find()

    return docs
