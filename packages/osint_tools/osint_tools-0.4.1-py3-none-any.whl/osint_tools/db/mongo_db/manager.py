from typing import Any, Callable
from pydantic import BaseModel, AnyUrl
from motor.core import AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ( 
    InsertOne,
    ReplaceOne
)

class MongoCrud(object):

    def __init__(self, uri: AnyUrl, db_name: str) -> None:
        """Motor provides a single client class, MotorClient. 
        Unlike PyMongos MongoClient, Motors client class does not begin connecting in the background when it is instantiated. 
        Instead it connects on demand, when you first attempt an operation.

        https://motor.readthedocs.io/en/stable/differences.html#connecting-to-mongodb
        Args:
            uri (AnyUrl): _description_
            db_name (str): _description_
        """
        client = AsyncIOMotorClient(uri, uuidRepresentation="standard")
        self.db = client[db_name]

    def get_mongo_db(self) -> AgnosticDatabase:
        """async Motor db connection

        Returns:
            AsyncIOMotorDatabase: _description_

        Yields:
            Iterator[AsyncIOMotorDatabase]: _description_
        """
        '''this throws TypeError: 'AsyncIOMotorDatabase' object is not iterable'''
        return self.db

    @property
    def get_db_name(self) -> str:
        return self.db.name

    @property
    async def get_build_info(self) -> dict:
        return await self.db.command("buildinfo")

    @property
    async def get_collection_names(self) -> list[str]:
        non_system = {"name": {"$regex": r"^(?!system\.)"}}
        return await self.db.list_collection_names(filter=non_system)

    async def create_unique_idx(self, db, field: str) -> Any:
        """a missing property will be added to the index as if it the value of that property were null.

        Args:
            db (_type_): _description_
            field (str): _description_

        Returns:
            Any:
        """
        res = await db.create_index(field, unique=True)
        return res

    async def drop_collection(
        self, 
        db: AgnosticDatabase, 
        collection_name: str
    ):
        dropped = await db.drop_collection(collection_name)
        return dropped

    async def get_distinct(
        self, 
        db: AgnosticDatabase, 
        field: str
    ):
        """
        - Distinct values for a given key

        https://www.mongodb.com/docs/manual/core/transactions/#distinct-operation

        Args:
            db (AsyncIOMotorDatabase): _description_
            field (str): _description_

        Raises:
            Exception: Any

        Returns:
            Any: List of unique values
        """
        try:
            cur = await db.distinct(field)
            return cur
        except Exception as err:
            # logger.info(f'{err}')
            raise Exception(f'{err}')

    async def delete_all(
        self, 
        db: AgnosticDatabase,
        obj: dict
    ):
        try:
            return await db.delete_many(obj)
        except Exception as e:
            return e

    async def insert_many_documents(
        self, 
        db: AgnosticDatabase, 
        collection_name: str, 
        results: list, 
        is_testing: bool = False
    ):
        '''
        https://pymongo.readthedocs.io/en/stable/examples/bulk.html#ordered-bulk-write-operations
        '''
        if is_testing:
            try:
                await db.drop_collection(collection_name)
            except Exception as e:
                raise

        await db[collection_name].insert_many((i for i in results))
        # count = await self.count_docs(db[collection_name])
        # logger.info({'Total Document Count': count})
        return 'insert many success'

    async def _insert_docs_test(
        self,
        db: AgnosticDatabase,
        collection_name: str,
        results: list,
    ):
        result = await db[collection_name].insert_many(({'x': i} for i in range(2)))
        r = result.inserted_ids
        return r

    async def find_all(
        self, 
        db: AgnosticDatabase, 
        model = None,
        _filter = None, 
        _projection = None, 
        as_dict: bool = False,
        skip: int = 0, 
        limit: int = 0
    ) -> list:
        query = db.find(_filter, _projection, skip=0, limit=0)
        if model:
            if as_dict:
                return [model(**raw).dict() async for raw in query]
            return [model(**raw) async for raw in query]
        return [raw async for raw in query]


    async def insert_or_update_many(
        self, 
        db_from: AgnosticDatabase, 
        db_to: AgnosticDatabase, 
        model: Callable, 
        _filter: dict = {}
    ):
        assert issubclass(model, BaseModel)
        try:
            query = db_from.find(filter=_filter)
            requests = [
                ReplaceOne(
                    {'_id': raw['_id']},
                    model(**raw).dict(),
                    upsert=True
                ) async for raw in query
            ]
            result = await db_to.bulk_write(requests)
            res_str = f'''New:\n-{result.upserted_ids}\nModified:\n-{result.modified_count}'''
            # logger.info(res_str)
            return res_str
        except Exception as e:
            raise


    async def bulk_insert_one(
        self, 
        db_from: AgnosticDatabase, 
        db_to: AgnosticDatabase, 
        model: Callable, 
        _filter: dict = None
    ):
        try:
            query = db_from.find(filter=_filter)
            requests = [
                InsertOne(
                    # model(**raw).dict()
                    model(**raw)
                ) async for raw in query
            ]
            result = await db_to.bulk_write(requests)
            res_str = f'''New:\n-{result.upserted_ids}\nModified:\n-{result.modified_count}'''
            return res_str
        except Exception as e:
            raise


    async def aggregation(
        self, 
        db: AgnosticDatabase, 
        pipe_line: list, 
        model: Callable = None
    ) -> list:
        try:
            cur = db.aggregate(pipe_line, allowDiskUse=True)
            if model:
                return [model(**i).dict() async for i in cur]
            return [i async for i in cur]
        except Exception as err:
            raise Exception(f'{err}')


    async def create(
        self, 
        db: AgnosticDatabase,
        obj: dict
    ):
        try:
            result = await db.insert_one(obj)
            return result
        except Exception as e:
            return e

    async def update(
        self, 
        db: AgnosticDatabase,
        query_by: dict,
        update_by: dict, 
    ):
        # p. 207
        try:
            return await db.update_one(query_by, update_by)
        except Exception as e:
            return e

    async def delete(
        self, 
        obj: dict, 
        db: AgnosticDatabase
    ):
        # p. 208
        try:
            return await db.delete_one(obj)
        except Exception as e:
            return e


