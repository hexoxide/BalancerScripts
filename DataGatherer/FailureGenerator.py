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
    def __init__(self, resultList, averageAck, averageLost, averagePerc, layers):
        self.__resultList = resultList
        self.__averageAck = averageAck
        self.__averageLost = averageLost
        self.__averagePerc = averagePerc
        self.__layers = layers


    def getResults(self):
        return self.__resultList

    def writeCSV(self, res):
        with open(res + "layered.csv", "w") as data:
            data.write("epnsLeft,averageLost,averageLatency\n")
            for epnsLeft, averageLost, averageLatency in self.__layers:
                data.write("%i,%i,%i\n" % (epnsLeft, averageLost, averageLatency))

        with open(res + "total.csv", "w") as data:
            data.write("date,Acknowledged_Timeframes,lost_TimeFrames,percentage_Lost,Lost_deviation,percentage_Deviation\n")
            for dat in self.__resultList:
                data.write("%s,%s,%s,%s%%,%s,%s\n" % (
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
        failures = 0
        layers = []

        for item in os.listdir(root):
            with open(os.path.join(root,item), "r") as fil:
                read_data = fil.read()
                results, failure = parseTimeLine(read_data)
                if(failure):
                    failures += 1
                else:
                    j = 0
                    totalTFs = 0
                    for i in results:
                        totalTFs += len(i.getTFs())
                        inList = False
               
                        for t in layers:
                            nr, lostTfs, latency = t
                            if nr == j:
                                inList = True
                                #print(lostTfs)
                                layers[j] = nr, lostTfs + len(i.getTFs()), i.getAverageLatency()

                        if not inList:
                            tmp = j, len(i.getTFs()), i.getAverageLatency()  
                            layers.append(tmp)
                        j += 1

                    #print(totalTFs)

                    perc = Decimal(
                        (TOTAL - totalTFs) / TOTAL * 100 
                    )
                    perc = round(perc,2)
                    tmpRes.append((dateFinder.findall(item)[0], totalTFs, TOTAL - totalTFs, perc))
       
        layerResult  = []
        for nr, totallost , latency in layers:
            tmp = nr, totallost / len(os.listdir(root)) , latency / len(os.listdir(root))
            layerResult.append(tmp)

        print("Total failed to initialize %i" % failures)
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
            averagePerc,
            layerResult
        )