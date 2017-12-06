#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ROOT import TCanvas, TGraph,TH1F
from array import array
import csv
import os
import re
from math import sqrt

def calculateStandardDeviation(failures):		
    totalLost = []		
    for lost  in failures:
        totalLost.append(float(lost))		
 		
    mean = sum(totalLost) / len(failures)		
    differences = [x - mean for x in totalLost]		
    sq_differences = [d ** 2 for d in differences]		
    ssd = sum(sq_differences)		
    variance = ssd / (len(failures) - 1)		
    sd = sqrt(variance)		
    return sd, mean


def showMeanDeviationRelation(dat):
    x,y = array('d'), array('d')
    highestSD = float('-inf')
    for tick, av, allLost in dat:
        sd, mean = calculateStandardDeviation(allLost)
        y.append(sd)
        x.append(mean)
        if sd > highestSD:
            highestSD = float(sd)

        print("%i,%i" % (tick,av))
    graph = TGraph(len(dat),x,y)

    graph.GetYaxis().SetRangeUser(0,highestSD)
    graph.SetTitle("mean standard deviation relation; mean ; standard deviation;")
    graph.Draw("ACP")
    raw_input("press a key to continue")


finder = re.compile(r'\s*([0-9]+).csv')

def getLost(file):
    res = finder.findall(file.replace("total", ""))
    with open(file) as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        totallost = 0
        totalAm = 0
        allLost = []
        next(reader, None)
        for date,Ack,lost,pl,Ld,pd  in reader:
            totallost += int(lost) 
            totalAm += 1
            allLost.append(lost)
        return (int(res[0]), (totallost / totalAm), allLost) 

dat = []
for file in os.listdir("./"):
    if file.endswith("csv"):
        if "total" in file:
            number, averagetotal, allLost = getLost(file)
            dat.append((number, averagetotal, allLost))

dat.sort(key=lambda tup: tup[0])

#showMeanDeviationRelation(dat)



canvas = TCanvas("c1", "Standard deviation of lost time frames", 200, 10, 800, 500)



x,y = array('d'), array('d')
for tick, ave, allLost in dat:
    x.append(tick)
    y.append(ave)

graph = TGraph(len(dat),x,y)
graph.SetTitle("Average data loss re-initialization algorithm by ticktime; ticktime (in milliseconds); lost time frames;")
graph.Draw("ACP")
raw_input("press a key to continue")




for tick, ave, allLost in dat:
    #his = TH1F("Lost TF", "Histogram lost Time frames", 100, lowest, highest)
    lowest= float('inf')
    highest= float('-inf')
    for i in allLost:
        if i > highest:
            highest = float(i)
        if i < lowest:
            lowest = float(i)
    
    lowest += 5
    highest+= 5
    his = TH1F("Lost TF %i"  % tick, "Histogram lost Time frames from re-initialization algorithm with ticktime %i" % tick, 100, lowest, highest)
    his.GetXaxis().SetTitle("lost")
    his.GetYaxis().SetTitle("Amount")
    for i in range(0, len(allLost)):
        his.Fill(float(allLost[i]))
    print("ticktime histgram shown: %i" % tick)
    his.Draw()
    raw_input("press a key")
