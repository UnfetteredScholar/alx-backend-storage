#!/usr/bin/env python3
"""
Python function that returns the list of school having
a specific topic:
"""


def schools_by_topic(mongo_collection, topic):
    """Returns the list of school having a specific topic"""

    # docs = mongo_collection.find({"topics": {"$elemMatch": {"$eq": topic}}})
    docs = mongo_collection.find({"topics": topic})

    return docs
