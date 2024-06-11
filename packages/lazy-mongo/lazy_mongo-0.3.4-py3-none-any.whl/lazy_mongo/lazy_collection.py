from typing import Dict, NamedTuple, TYPE_CHECKING
from pymongo.collection import Collection
from pymongo.typings import _Pipeline
from pymongo.errors import DuplicateKeyError
from .update_response import UpdateResponse
from .insert_response import InsertResponse

if TYPE_CHECKING:
    from .lazy_database import LazyDatabase
    from .lazy_mongo import LazyMongo


class LazyCollection(NamedTuple):
    mongo: "LazyMongo"
    database: "LazyDatabase"
    collection: Collection

    def find_one(
        self,
        query: Dict = None,  # type: ignore
        project: Dict = None,  # type: ignore
    ):
        return self.collection.find_one(query, project)

    def find(
        self,
        query: Dict = None,  # type: ignore
        project: Dict = None,  # type: ignore
    ):
        return self.collection.find(query, project)

    def insert_one(
        self,
        document: Dict = None,  # type: ignore
    ):
        try:
            result = self.collection.insert_one(document)

            if self.mongo.log:
                print("[Mongo.Insert]", result.inserted_id)

            return InsertResponse(
                ok=True,
                result=result,
            )

        except DuplicateKeyError as e:
            if self.mongo.log:
                print("[Mongo.Duplicate]", e.code)

            return InsertResponse(
                ok=False,
                is_duplicate=True,
                error=e,
            )

        except Exception as e:
            if self.mongo.log:
                print("[Mongo.Error]", e)

            return InsertResponse(
                ok=False,
                error=e,
            )

    def update_one(
        self,
        filter: Dict = None,  # type: ignore
        update: Dict = None,  # type: ignore
        **kwargs,
    ):
        try:
            result = self.collection.update_one(
                filter=filter,
                update=update,
                **kwargs,
            )

            if self.mongo.log:
                print(
                    "[Mongo.Update]",
                    result.upserted_id or result.modified_count,
                )

            return UpdateResponse(
                ok=True,
                result=result,
            )

        except DuplicateKeyError as e:
            if self.mongo.log:
                print("[Mongo.Duplicate]", e)

            return UpdateResponse(
                ok=False,
                is_duplicate=True,
                error=e,
            )

        except Exception as e:
            if self.mongo.log:
                print("[Mongo.Error]", e)

            return UpdateResponse(
                ok=False,
                error=e,
            )

    def update_set_one(
        self,
        filter: Dict = None,  # type: ignore
        document: Dict = None,  # type: ignore
    ):
        """
        Shortcut for `$set`.

        Upsert = `False`
        """
        return self.update_one(
            filter,
            update={
                "$set": document,
            },
            upsert=False,
        )

    def count(
        self,
        query: Dict = None,  # type: ignore
    ):
        return self.collection.count_documents(query)

    def distinct(self, key: str):  # type: ignore
        return self.collection.distinct(key)

    def aggregate(self, pipeline: _Pipeline, **kwargs):
        return self.collection.aggregate(
            pipeline,
            **kwargs,
        )
