#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ROOT import TCanvas, TGraph,TH1F
from array import array
from DataGatherer.Utilities import getInput
from math import sqrt
import sys

def visualizeData(resultsFailures):
    canvas = TCanvas("c1", "Standard deviation of lost time frames", 200, 10, 800, 500)
    #canvas.SetGrid()
    canvas.Divide(2,1)
    canvas.cd(1)
    n = len(resultsFailures.getResults())
    print(n)
    x,y = array('d'), array('d')
    lowest = float('inf')
    highest = float('-inf')
    for i in range(0,n):
        lostTF = resultsFailures.getResults()[i].getDifferenceLostTF()
        if lostTF > highest:
            highest = lostTF
        if lostTF < lowest:
            lowest = lostTF

        y.append(
           lostTF
        )
        x.append(i)


    lowest += 5
    highest+= 5

    graph = TGraph(n,x,y)
    graph.SetTitle("Differences from the average Lost timeframes; Run; difference in lost timeframes;");
    graph.Draw("ACP")
    #getInput("press any key")
    his = TH1F("Lost TF", "Histogram lost Time frames", 100, lowest, highest)
    his.GetXaxis().SetTitle("Deviation #sigma")
    his.GetYaxis().SetTitle("Amount")
    for i in range(0, n):
        his.Fill(resultsFailures.getResults()[i].getDifferenceLostTF())

    canvas.cd(2)
    his.Draw()
    getInput("press any key")
    

