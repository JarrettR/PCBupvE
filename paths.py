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

    for path in upv_paths:
        count += 1
        
        if path['layer'] == 'mechanical details':
            used_count += 1
            
            bounds = findLimits(path['points'])
            translated_path = translate(path['points'], -1 * bounds['min_x'], -1 * bounds['min_y'])
            svg = createSVG(translated_path)

    print(used_count, "paths processed of", count)
    return(svg, bounds)
    
def findLimits(path):
    max_x = 0
    max_y = 0
    min_x = None
    min_y = None
    
    for point in path:
        if max_x < point['x']:
            max_x = point['x']
        if max_y < point['y']:
            max_y = point['y']
            
        if not min_x:
            min_x = point['x']
        elif min_x > point['x']:
            min_x = point['x']
            
        if not min_y:
            min_y = point['y']
        elif min_y > point['y']:
            min_y = point['y']
        
    return { 'min_x': min_x, 'max_x': max_x, 'min_y': min_y, 'max_y': max_y }
    
def createSVG(path):
    initial = ''
    value = ''
    i = 0
    for point in path:
        if i == 0:
            initial = str(nmToMm(point['x'])) + ',' + str(-1 * nmToMm(point['y']))
            value += 'M ' + initial
        else:
            value += ' L ' + str(nmToMm(point['x'])) + ',' + str(-1 * nmToMm(point['y']))
            
        #Hack: to fix unclosed paths (https://github.com/boldport/pcbmode/issues/50)
        value += ' L ' + initial
        
        i += 1
    value += ' z'
    return value
    
def translate(path, x, y):
    translated_path = []
    for point in path:
        translated_path.append( { 'x': point['x'] + x, 'y': point['y'] + y } )
        
    return translated_path

def nmToMm(nm):
    return (int(nm) / 1000000)