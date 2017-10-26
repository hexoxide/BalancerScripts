#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from decimal import Decimal
from DataGatherer.ReceivedTime import ReceivedTime, parseTimeLine
from DataGatherer.Globals import TOTAL, MIN_ID, MAX_ID
import re
import os
class SingleFailureResult(object):
    def __init__(self,date,ack,lost,perc,diffLost,diffPerc):
        self.__date = date
        self.__ack = ack
        self.__lost = lost
        self.__perc = perc
        self.__difflost = diffLost
        self.__diffPerc =diffPerc

    def getDate(self):
        return self.__date
    
    def getAcknowledgedTF(self):
        return self.__ack

    def getLostTF(self):
        return self.__lost
    
    def getLostPercentage(self):
        return self.__perc

    def getDifferenceLostTF(self):
        return self.__difflost

    def getDiffPercentageTF(self):
        return self.__diffPerc

class FailureResults(object):
    def __init__(self, resultList, averageAck, averageLost, averagePerc):
        self.__resultList = resultList
        self.__averageAck = averageAck
        self.__averageLost = averageLost
        self.__averagePerc = averagePerc

    def getResults(self):
        return self.__resultList

    def writeCSV(self, res):
        with open(res, "w") as res:
            res.write("date,Acknowledged_Timeframes,lost_TimeFrames,percentage_Lost,Lost_deviation,percentage_Deviation\n")
            for dat in self.__resultList:
                res.write("%s,%s,%s,%s%%,%s,%s\n" % (
                    dat.getDate(),
                    dat.getAcknowledgedTF(),
                    dat.getLostTF(),
                    dat.getLostPercentage(),
                    dat.getDifferenceLostTF(),
                    dat.getDiffPercentageTF()
                    )
                )


    @staticmethod
    def generateFailureResult(path):
        dateFinder = re.compile(r'Information_([0-9]+\-[0-9]+\-[0-9]+\_[0-9]+\-[0-9]+\-[0-9]+.[0-9]+).log')
        root = os.path.abspath(path)
        tmpRes = []

        for item in os.listdir(root):
            with open(os.path.join(root,item), "r") as fil:
                read_data = fil.read()
                results = parseTimeLine(read_data)

                perc = Decimal(
                            (TOTAL - len(results)) /
                            TOTAL * 100 
                )
                perc = round(perc,2)
                tmpRes.append((dateFinder.findall(item)[0], len(results), TOTAL - len(results), perc))

        #check stats
        averageLost = 0
        averageAck = 0
        averagePerc = 0
        for date, ack, lost, perc in tmpRes:
            averageLost += lost
            averageAck += ack
            averagePerc += perc

        averageLost = round(averageLost / len(tmpRes),2)
        averageAck = round(averageAck / len(tmpRes),2)
        averagePerc = round(averagePerc / len(tmpRes),2)
        print(averageLost)
        finalRes = []
        for date, ack, lost, perc in tmpRes:
            diffPerc = averagePerc - perc
            diffLost = lost - averageLost

            finalRes.append(
                SingleFailureResult(
                    date,
                    ack,
                    lost,
                    perc,
                    diffLost,
                    diffPerc
                )
            )
        return FailureResults(
            finalRes,
            averageLost,
            averageAck,
            averagePerc
        )