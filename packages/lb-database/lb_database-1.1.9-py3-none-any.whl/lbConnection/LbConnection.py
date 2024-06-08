# -*- coding: utf-8 -*-
__author__ = 'Lucas Barros'
__version__ = 1.0
__maintainer__ = 'Lucas Barros'
__email__ = 'lucasbarros2000@hotmail.com'
__status__ = 'Production'


import os
import pymongo
from lbConnection.Query import Query
from lbConnection.Projection import Projection
from lbLogger.LbLogger import LbLogger
from pymongo import results
from typing import Any
from typing import List


class LbConnection:

    def __init__(self):
        self.__lb_logger: LbLogger = LbLogger()

        url_database: str = self.check_and_read_environment_variables(variable="db_con")
        name_database: str = self.check_and_read_environment_variables(variable="db_name")

        my_connection = pymongo.MongoClient(url_database)
        self.__my_database = my_connection[name_database]

    def find_one(self, query: Query, class_model: Any, collection: str, projection: Projection = None) -> Any:
        """
        Function for find one document by query
        :param query: Query to use in search database
        :param class_model: Data model to apply return document
        :param projection: Fields for return search
        :param collection: Collection for get data
        :return: Data model (class model) with documents founded in database
        """

        self.__lb_logger.info(f"Starting find one by query {query.query()}")

        database_document: List = []
        if projection is None:
            database_document = list(self.__my_database[collection].find(query.query()))
        else:
            database_document = list(self.__my_database[collection].find(query.query(), projection.projection()))

        self.__lb_logger.info(f"Founded {len(database_document)} documents by query")

        if len(database_document) > 0:
            return class_model(**database_document[0])
        return {}

    def list(self, query: Query, class_model: Any, collection: str, projection: Projection = None):
        """
        Function for list documents by query
        :param query: Query to use in search database
        :param class_model: Data model to apply return documents
        :param projection: Fields for return search
        :param collection: Collection for get data
        :return: List with data model (class model) with documents founded in database
        """

        self.__lb_logger.info(f"Starting list by query {query.query()}")

        database_document: List
        if projection is None:
            database_document = list(self.__my_database[collection].find(query.query()))
        else:
            database_document = list(self.__my_database[collection].find(query.query(), projection.projection()))

        self.__lb_logger.info(f"Founded {len(database_document)} documents by query")

        if len(database_document) > 0:
            return [class_model(**document) for document in database_document]
        else:
            return []

    def count(self, query: Query, collection: str) -> int:
        """
        Function for count documents by query
        :param query: Query for search and count documents
        :param collection: Collection for get data
        :return: Number documents founded by query
        """

        self.__lb_logger.info(f"Starting count by query {query.query()}")

        return self.__my_database[collection].count(query.query())

    def distinct(self, query: Query, key_distinct: str, collection: str) -> List[Any]:
        """
        Function for get distinct values field by query
        :param query: Query for distinct field
        :param key_distinct: Field for distinct values
        :param collection: Collection for get data
        :return: List with distinct values by field
        """

        self.__lb_logger.info(f"Starting distinct by query {query.query()}")

        return self.__my_database[collection].distinct(key=key_distinct, query=query.query())

    def update_one(self, query: Query, update: Query, collection: str) -> None:
        """
        Function for update one document by query
        :param query: Query for update one document
        :param update: Fields and values for update
        :param collection: Collection for get data
        :return: None
        """

        self.__lb_logger.info(f"Starting update one by query {query.query()}")

        self.__my_database[collection].update_one(query.query(), {"$set": update.query()})

    def update_one_unset(self, query: Query, update: Query, collection: str) -> None:
        """
        Function for update one unset document by query
        :param query: Query for update one document
        :param update: Fields and values for update
        :param collection: Collection for get data
        :return: None
        """

        self.__lb_logger.info(f"Starting update one by query {query.query()}")

        self.__my_database[collection].update_one(query.query(), {"$unset": update.query()})

    def update_many(self, query: Query, update: Query, collection: str) -> None:
        """
        Function for update many document by query
        :param query: Query for update many document
        :param update: Fields and values for update
        :param collection: Collection for get data
        :return: None
        """

        self.__lb_logger.info(f"Starting update many by query {query.query()}")

        self.__my_database[collection].update_many(query.query(), {"$set": update.query()})

    def insert_one(self, document: dict, collection: str) -> results:
        """
        Function for insert one document at mongo database
        :param document: Document for insert
        :param collection: Collection for get data
        :return: Result insert mongo databse
        """

        self.__lb_logger.info(f"Starting insert one document at mongo database")

        return self.__my_database[collection].insert_one(document=document)

    def check_and_read_environment_variables(self, variable: Any) -> Any:
        """
        Function for check and read environment variable
        :param variable: Variable for check
        :return: Environment variable
        """

        self.__lb_logger.info(message=f"Checking variable {variable}")

        environment_variable: Any = os.environ.get(variable, None)

        if environment_variable is None:
            raise EnvironmentError(f"Environment variable {variable} is required")

        return environment_variable
