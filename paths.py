#!/usr/bin/python

import json
import math
import numpy as np

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
    svg = ''

    for path in upv_paths:
        count += 1
        print("apth ", count)
        
        if path['layer'] == 'mechanical details':
            used_count += 1
            
            bounds = findLimits(path['points'])
            translated_path = iter(translate(path['points'], -1 * bounds['min_x'], -1 * bounds['min_y']))
            #if svg == '':
            svg += createSVG(translated_path, path['shape_types'])

    print(svg)
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
    
def createSVG(path, shape_types):
    initial = ''
    value = ''
    arc_run = False
    i = 0
    for point in path:
        print('-> ', nmToMm(point['x']), ' ', nmToMm(point['y']), shape_types[i])
        if i == 0:
            initial = str(nmToMm(point['x'])) + ',' + str(-1 * nmToMm(point['y']))
            value += 'M ' + initial
        #elif arc_run == False and shape_types[i] != 'arc':
        elif arc_run:
            arc_run = False
            nadir = point
            value += createArc(start, end, nadir)
        elif shape_types[i] == 'arc':
            value += ' L ' + str(nmToMm(point['x'])) + ',' + str(-1 * nmToMm(point['y']))
            start = point
            point = next(path)
            print('-> ', nmToMm(point['x']), ' ', nmToMm(point['y'])) #, ' ', shape_types[i])
            end = point
            arc_run = True
        else:
            value += ' L ' + str(nmToMm(point['x'])) + ',' + str(-1 * nmToMm(point['y']))
            
        i += 1
                
    #Hack: to fix unclosed paths (https://github.com/boldport/pcbmode/issues/50)
    value += ' L ' + initial
    
    value += ' z '
    return value
    
def createArc(start, end, nadir):
    a = nmToMm(distance(start, nadir))
    b = nmToMm(distance(nadir, end))
    c = nmToMm(distance(end, start))
    r = c / 2
    
    #angle = sidesToAngle(a, b, c)
    angle = np.arctan((start['y'] - end['y']) / (start['x'] - end['x']))
    
    centre = {'x': (r * np.cos(angle)), 'y': (r * np.sin(angle))}
    centre['x'] = nmToMm(start['x']) - centre['x']
    centre['y'] = nmToMm(start['y']) - centre['y']
    
    print('start: ', nmToMm(start['x']), nmToMm(start['y']))
    print('end: ', nmToMm(end['x']), nmToMm(end['y']))
    print('nadir: ', nmToMm(nadir['x']), nmToMm(nadir['y']))
    print('angle: ', angle)
    print('a: ', a)
    print('b: ', b)
    print('c: ', c)
    print('centre: ', centre['x'], centre['y'])
    
    if angle > (math.pi / 2):
        large_arc = 1
    else:
        large_arc = 0
        
    sweep = 0
    
    #A rx ry rotation large_arc sweep x y
    svg = " A {:f} {:f} {:f} {} {} {:f} {:f}".format(r, r, angle, large_arc, sweep, centre['x'], centre['y'])
        
    return svg
    
def translate(path, x, y):
    translated_path = []
    for point in path:
        translated_path.append( { 'x': point['x'] + x, 'y': point['y'] + y } )
        
    return translated_path
    
def distance(a, b):
    '''Straight-line distance between two points'''

    d = math.sqrt((b['x'] - a['x'])**2 + (b['y'] - a['y'])**2)

    return d
    
def sidesToAngle(a, b, c):
    '''Cosine law: Given sides a, b, and c, this will return angle C'''

    #return 5
    if a + b <= c:
        raise ValueError('Cosine Lawbreaker! a + b must be greater than c')
    else:

        C = np.arccos((a * a + b * b - c * c)/(2.0 * a * b))

        return C

def nmToMm(nm):
    return (int(nm) / 1000000)