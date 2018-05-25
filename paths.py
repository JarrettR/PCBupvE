#!/usr/bin/python

import json

def upvPaths(upv_paths):
    """
    Paths
    Initially only bothering with outlines
    Assuming on mechanical layer
    Todo: finish for all paths
    """
    count = 0
    used_count = 0

    paths = {}
    value = ''

    for path in upv_paths:
        count += 1
        
        
        
        if path['layer'] == 'mechanical details':
            used_count += 1
            
            i = 0
            for point in path['points']:
                if i == 0:
                    value += 'M ' + str(nmToMm(point['x'])) + ',' + str(-1 * nmToMm(point['y']))
                else:
                    value += ' L ' + str(nmToMm(point['x'])) + ',' + str(-1 * nmToMm(point['y']))
                i += 1

    print(used_count, "paths processed of", count)
    return(value)
    
def findLimits(path):
    return 5,10
    
def translate(path, x, y):
    return path

def nmToMm(nm):
    return (int(nm) / 1000000)