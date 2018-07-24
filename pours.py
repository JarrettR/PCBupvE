#!/usr/bin/python

import json

def upvPours(upv_pours):
    """
    Pours
    """
    count = 0

    pours = {}
    pour_instances = {}

    for pour in upv_pours:
        
        pours[str(count)] = {'layout': {'pours': {'shapes': [genPour(pour)] } } }
    
        #layer
        if pour['layer'][0:3] == 'top':
            layer = 'top'
        elif pour['layer'][0:6] == 'bottom':
            layer = 'bottom'
        else:
            raise ValueError("I haven\'t seen pour layer %s before! Please report an issue!" % pour['layer'])
            
        pour_instances['pour' + str(count)] = {
                'footprint': str(count),
                'layer': layer,
                'location': [0, 0],
                'rotate': 180,
                'show': True
            }
        
        
        count += 1

    print(count, "pours processed")
    return(pours, pour_instances)

def genPour(data):
    count = 0
            
    #todo: find more than first one
    points = data['polygons']['polygons'][0]['outline']['points']
    value = ''

    for point in points:
        
        if count == 0:
            value = 'M ' + str(nmToMm(point['x'])) + ',' + str(nmToMm(point['y']))
        else:
            value += 'L' + str(nmToMm(point['x'])) + ',' + str(nmToMm(point['y']))
            
        count += 1
        
    value += ' z'
    pour = {
        'style': 'fill',
        'type': 'path',
        'value': value
    }   

    return(pour)
    
def nmToMm(nm):
    return(int(nm) / 1000000)