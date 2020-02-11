#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 13:07:03 2020

@author: murzik
"""

import requests
from collections import defaultdict
import statistics 
import matplotlib.pyplot as plt

response = requests.get("https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20200101]&count=receivedate")
response1 = requests.get("https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20200101]+AND+patient.drug.drugindication:DIABETES&count=receivedate")
response2 = requests.get("https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20200101]+AND+patient.drug.drugindication:DIABETES+AND+patient.drug.medicinalproduct:AVANDIA+AND+occurcountry:'US'&count=receivedate")
responsearray = [response, response1, response2]

for aresponse in responsearray:
        
    monthly = defaultdict(int)
    #country = ['US']
    results = aresponse.json().get('results')
    for record in results:
        count = record.get('count')
        date = record.get('time')
        monthKey = ''.join(date[0:4])+'-'+''.join(date[4:6])
        monthly[monthKey] += int(count)
    
    Window = 24
    NewMonthly = {}
    counter = 0
    for key in monthly:
        NewMonthly[counter] = [key,monthly[key]]
        counter += 1
    
    for counter1 in range(len(NewMonthly)):
        AverageArray = []
        if counter1 < Window:
            NewMonthly[counter1].append(0)
        else:   
            Sum = 0
            for valuerange in range((counter1 - (Window-1)),(counter1)):
                SumSet = NewMonthly[valuerange]
                SumVal = SumSet[1]
                AverageArray.append(SumVal)
            Average = statistics.mean(AverageArray)
            Stdev = statistics.stdev(AverageArray)
            NewMonthly[counter1].append(Average)
            NewMonthly[counter1].append(Stdev)
    x = []
    y = []
    y1 = []
    for key in NewMonthly:
        ValArray = NewMonthly[key]
        x.append(ValArray[0])
        y.append(ValArray[1])
        y1.append(ValArray[2])
    plt.figure()
    plt.plot(x,y)
    plt.plot(x, y1)
    plt.show

