#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DataGatherer.FailureGenerator import FailureResults

def main(arguments):
    number = str(int(arguments[1]))
    res = FailureResults.generateFailureResult("./resblacklist/info/"+ number +  "/172.20.22.17/root/info")
    res.writeCSV(number)
