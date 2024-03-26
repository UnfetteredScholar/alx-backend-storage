#!/usr/bin/env python3
""" 8-main """
from pymongo import MongoClient

list_all = __import__("8-all").list_all

if __name__ == "__main__":
    client = MongoClient("mongodb://mongo_user:mongo_pwd@localhost:27017")
    school_collection = client.my_db.school
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {}".format(school.get("_id"), school.get("name")))
