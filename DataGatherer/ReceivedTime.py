#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from DataGatherer.Globals import TOTAL, MIN_ID, MAX_ID


class ReceivedTime(object):
    def __init__(self, time, id, ip, latency):
        self.__time = time
        self.__id = id
        self.__ip = ip
        self.__latency = latency

    def __str__(self):
        return "%s,%i,%s,%i\n" % (self.__time, self.__id, self.__ip, self.__latency)




finder = re.compile(r'\[([0-9]+\:[0-9]+\:[0-9]+)\]\[INFO\]\s+Timeframe\s+#([0-9]+)\s+received\s+from\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+acknowledged\safter\s([0-9]+)\sμs')
def parseTimeLine(lines):
    results = []
    res = finder.findall(lines)
    for i in res:
        
        #print("%s received : %i from %s duration: %i" % (i[0], int(i[1]), i[2], int(i[3])))
        id = int(i[1])
        if(id > MIN_ID and id < MAX_ID):
            results.append(ReceivedTime(
                i[0], # time
                id, #id
                i[2], #target
                int(i[3]) #latency 
            ))
    return results
