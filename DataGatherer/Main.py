#!/usr/bin/env python
# -*- coding: utf-8 -*-


from DataGatherer.FailureGenerator import FailureResults
from DataGatherer.VisualizeFailures import visualizeData

def main(arguments):
    res = FailureResults.generateFailureResult("./info")
    visualizeData(res)
    res.writeCSV("res.csv")
