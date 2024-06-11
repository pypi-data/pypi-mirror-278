from typing import Dict, NamedTuple, TYPE_CHECKING
from pymongo.database import Database
from .lazy_collection import LazyCollection
from pymongo.typings import _Pipeline

if TYPE_CHECKING:
    from .lazy_mongo import LazyMongo


class LazyDatabase(NamedTuple):
    mongo: "LazyMongo"
    database: Database
    default_collection_name: str = None  # type: ignore

    def __getitem__(self, key: str):
        return LazyCollection(
            mongo=self.mongo,
            database=self,
            collection=self.database[key],
        )

    def find_one(
        self,
        collection: str = None,  # type: ignore
        query: Dict = None,  # type: ignore
        project: Dict = None,  # type: ignore
    ):
        coll = self[collection or self.default_collection_name]

        return coll.find_one(query, project)

    def find(
        self,
        collection: str = None,  # type: ignore
        query: Dict = None,  # type: ignore
        project: Dict = None,  # type: ignore
    ):
        coll = self[collection or self.default_collection_name]

        return coll.find(query, project)

    def insert_one(
        self,
        collection: str = None,  # type: ignore
        document: Dict = None,  # type: ignore
    ):
        coll = self[collection or self.default_collection_name]

        return coll.insert_one(document)

    def update_one(
        self,
        collection: str = None,  # type: ignore
        filter: Dict = None,  # type: ignore
        update: Dict = None,  # type: ignore
        **kwargs,
    ):
        coll = self[collection or self.default_collection_name]

        return coll.update_one(filter, update, **kwargs)

    def update_set_one(
        self,
        collection: str = None,  # type: ignore
        filter: Dict = None,  # type: ignore
        document: Dict = None,  # type: ignore
    ):
        coll = self[collection or self.default_collection_name]

        return coll.update_set_one(filter, document)

    def count(
        self,
        collection: str = None,  # type: ignore
        query: Dict = None,  # type: ignore
    ):
        coll = self[collection or self.default_collection_name]

        return coll.count(query)

    def distinct(
        self,
        key: str,
        collection: str = None,  # type: ignore
    ):
        coll = self[collection or self.default_collection_name]

        return coll.distinct(key)

    def aggregate(
        self,
        pipeline: _Pipeline,
        collection: str = None,  # type: ignore
        **kwargs,
    ):
        coll = self[collection or self.default_collection_name]

        return coll.aggregate(pipeline, **kwargs)
