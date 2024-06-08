# -*- coding: utf-8 -*-
__author__ = 'Lucas Barros'
__version__ = 1.0
__maintainer__ = 'Lucas Barros'
__email__ = 'lucasbarros2000@hotmail.com'
__status__ = 'Production'


class Query:

    def __init__(self):
        self.__query = {}

    def query(self):
        return self.__query

    def where(self, field: str, value: any) -> None:
        self.__query[field] = value
