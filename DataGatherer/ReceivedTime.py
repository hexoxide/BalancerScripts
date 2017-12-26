#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from DataGatherer.Globals import TOTAL, MIN_ID, MAX_ID, Snapshot


class ReceivedTime(object):
    def __init__(self, time, id, ip, latency):
        self.__time = time
        self.__id = id
        self.__ip = ip
        self.__latency = latency

    def getLatency(self):
        return self.__latency

    def __str__(self):
        return "%s,%i,%s,%i\n" % (self.__time, self.__id, self.__ip, self.__latency)


#[05:06:00][ERROR] Could not create a variable with name sampleSize and value 22
taintedFinder = re.compile(r'\[[0-9]+\:[0-9]+\:[0-9]+\]\s*\[ERROR\]\s*Could\s*not\s*create\s*a\s*variable\s*with\s*name\s*sampleSize\s*and\s*value\s*[0-9]*\s*')
finder = re.compile(r'\[([0-9]+\:[0-9]+\:[0-9]+)\]\[INFO\]\s+Timeframe\s+#([0-9]+)\s+received\s+from\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+acknowledged\safter\s([0-9]+)\sμs')
def parseTimeLine(lines):
    results = []
    tained = taintedFinder.search(lines)
    res = finder.findall(lines)
    snapshots = [
        Snapshot(2000,3000),
        Snapshot(3000,4000),
        Snapshot(4000,5000),
        Snapshot(5000,6000),
        Snapshot(6000,7000),
        Snapshot(7000,8000),
        Snapshot(8000,9000),
        Snapshot(9000,10000),
        Snapshot(10000, 11000),
        Snapshot(11000,12000),
        Snapshot(12000,13000),
        Snapshot(13000,14000)
    ]
    for i in res:
        id = int(i[1])
        for snapshot in snapshots:
            if(snapshot.idFits(id)):
                snapshot.addReceivedTf(ReceivedTime(
                    i[0], # time
                    id, #id
                    i[2], #target
                    int(i[3]) #latency 
                ))
                break



    for i in snapshots:
        results.append(i)
    
    return results, (not tained == None)
