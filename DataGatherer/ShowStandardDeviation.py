#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ROOT import TCanvas, TGraph
from array import array
from DataGatherer.Utilities import getInput
from math import sqrt

def calculateStandardDeviation(failures):
    lst = failures.getResults()
    totalLost = []
    for i in range(0,len(lst)):
        totalLost.append(lst[i].getLostTF())

    mean = sum(totalLost) / len(lst)
    differences = [x - mean for x in totalLost]
    sq_differences = [d ** 2 for d in differences]
    ssd = sum(sq_differences)
    variance = ssd / (len(lst) - 1)
    sd = sqrt(variance)
    print('The mean of {} is {}.'.format(lst, mean))
    print('The differences are {}.'.format(differences))
    print('The sum of squared differences is {}.'.format(ssd))
    print('The variance is {}.'.format(variance))
    print('The standard deviation is {}.'.format(sd))
    print('--------------------------')
    return sd

def showStandardDeviation(resultsFailures):
    calculateStandardDeviation(resultsFailures)
    print("test")
    canvas = TCanvas("c1", "Standard deviation of lost time frames", 200, 10, 800, 500)
    canvas.SetGrid()
    n = len(resultsFailures.getResults())
    x,y = array('d'), array('d')
    for i in range(0,n):
        y.append(
            resultsFailures.getResults()[i].getDifferenceLostTF()
        )
    
    for i in range(0,n):
        x.append(i)

    graph = TGraph(n,x,y)
    graph.SetTitle("differences from the average Lost timeframes; Run; difference in lost timeframes;");
    graph.Draw("ACP")
    getInput("d")