# -*- coding: utf-8 -*-
__author__ = 'Lucas Barros'
__version__ = 1.0
__maintainer__ = 'Lucas Barros'
__email__ = 'lucasbarros2000@hotmail.com'
__status__ = 'Production'


from enum import Enum


class EnumCollections(str, Enum):

    CNAES: str = "cnaes"
    COMPANIES: str = "companies"
    USERS: str = "users"
