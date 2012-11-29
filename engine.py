#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""copyright (c) 2012 - EsDevel"""

from ui.core import window
from ui import builder

class main:
    def __init__(self):
        self.__package__ = """glmplayer"""
        self.__version__ = """0.1"""
        self.__title__ = """GLMPlayer"""
        self.__ID__ = 1
        self.__parent__ = None
        self.__instance__ = None
    def run(self):
        p = self.__parent__
        t = self.__title__
        ID = self.__ID__
        self.__instance__ = window.Window(p,ID,t)
    def build(self):
        builder.startBuilding(self.__instance__)