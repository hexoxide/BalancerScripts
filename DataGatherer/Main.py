#!/usr/bin/env python
# -*- coding: utf-8 -*-


from DataGatherer.FailureGenerator import FailureResults
from DataGatherer.ShowStandardDeviation import showStandardDeviation

def main(arguments):
    res = FailureResults.generateFailureResult("./info")
    showStandardDeviation(res)
    res.writeCSV("res.csv")
