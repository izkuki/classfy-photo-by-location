# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 18:39:46 2019

@author: izkuk
"""


import json


def findlocation(alldata,lati,longi):
    item1 = {}
    dist1 = 0
    
    #遍历寻找最小值
    for item in alldata:
        latix1 = item['lati']
        longix1 = item['longi']
        dist = ((lati-latix1)**2 + (longi-longix1)**2)**0.5
        if item1 == {}:
            item1 = item
            dist1 = dist
            continue
        
        if dist1 > dist:
            dist1 = dist
            item1 = item
        
        continue
    
    return item1

        
        


with open('map_data_new.json', 'r', encoding='utf8') as fp:
    json_str = json.load(fp)
    print(type(json_str))

#测试    
print(findlocation(json_str,33.39476,112.1924))
