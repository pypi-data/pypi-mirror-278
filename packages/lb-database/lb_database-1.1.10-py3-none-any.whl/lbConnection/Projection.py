# -*- coding: utf-8 -*-
__author__ = 'Lucas Barros'
__version__ = 1.0
__maintainer__ = 'Lucas Barros'
__email__ = 'lucasbarros2000@hotmail.com'
__status__ = 'Production'


class Projection:

    def __init__(self):
        self.__projection = {}

    def projection(self):
        return self.__projection

    def include(self, field):
        self.__projection[field] = 1

    def exclude(self, field):
        self.__projection[field] = 0
