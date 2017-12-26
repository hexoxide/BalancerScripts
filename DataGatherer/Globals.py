#!/usr/bin/env python
# -*- coding: utf-8 -*-

MIN_ID = 2000
MAX_ID = 14000

class Snapshot(object):
    def __init__(self, min,max):
        self.__min = min
        self.__max = max
        self.__data = []

    def addReceivedTf(self, TF ):
        self.__data.append(TF)

    def getTFs(self):
        return self.__data

    def getAverageLatency(self):
        res = 0
        for i in self.__data:
            res += i.getLatency()

        return res / len(self.__data)

    def idFits(self, id):
        return (id > self.getMin() and id < self.getMax())

    def getTotal(self):
        return self.__max - self.__min

    def getMin(self):
        return self.__min
    
    def getMax(self):
        return self.__max



TOTAL = MAX_ID - MIN_ID