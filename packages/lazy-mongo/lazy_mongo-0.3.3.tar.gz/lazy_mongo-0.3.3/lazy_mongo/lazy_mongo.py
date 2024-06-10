from typing import Dict
from pymongo import MongoClient
from .lazy_database import LazyDatabase
from pymongo.typings import _Pipeline


class LazyMongo:
    def __init__(self):
        self.mongo: MongoClient = None  # type: ignore
        self.default_database: str = None  # type: ignore
        self.default_collection: str = None  # type: ignore
        self.log: bool = True

    def connect(self, uri: str):
        try:
            self.mongo = MongoClient(uri)
        except:
            pass

        return self

    def __getitem__(self, key: str):
        return LazyDatabase(
            mongo=self,
            database=self.mongo[key or self.default_database],
            default_collection_name=self.default_collection,
        )

    def find_one(
        self,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        query: Dict = None,  # type: ignore
        project: Dict = None,  # type: ignore
    ):
        db = self[database or self.default_database]

        return db.find_one(collection, query, project)

    def find(
        self,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        query: Dict = None,  # type: ignore
        project: Dict = None,  # type: ignore
    ):
        db = self[database or self.default_database]

        return db.find(collection, query, project)

    def insert_one(
        self,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        document: Dict = None,  # type: ignore
    ):
        db = self[database or self.default_database]

        return db.insert_one(collection, document)

    def update_one(
        self,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        filter: Dict = None,  # type: ignore
        update: Dict = None,  # type: ignore
        **kwargs,
    ):
        db = self[database or self.default_database]

        return db.update_set_one(
            collection,
            filter,
            update,
            **kwargs,
        )

    def update_set_one(
        self,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        filter: Dict = None,  # type: ignore
        document: Dict = None,  # type: ignore
    ):
        db = self[database or self.default_database]

        return db.update_set_one(
            collection,
            filter,
            document,
        )

    def count(
        self,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        query: Dict = None,  # type: ignore
    ):
        db = self[database or self.default_database]

        return db.count(collection, query)

    def distinct(
        self,
        key: str,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
    ):
        db = self[database or self.default_database]

        return db.distinct(key, collection)

    def aggregate(
        self,
        pipeline: _Pipeline,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        **kwargs,
    ):
        db = self[database or self.default_database]

        return db.aggregate(pipeline, collection, **kwargs)
