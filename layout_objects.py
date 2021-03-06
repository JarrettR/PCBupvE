#!/usr/bin/python

import json 

from pprint import pprint

def upvLayoutObjects(upv_layout_objects, bounds):
    """
    Layout Objects
    So far only seen vias in this
    """
    count = 0
    
    vias = {}
    
    for layout_object in upv_layout_objects:
        count += 1
        
        #Error handling for future improvement
        #Only handling vias right now
        if layout_object['layer'] != 'via':
            raise ValueError('I haven\'t seen this layout_object layer before! Please report an issue!')
        if layout_object['attributes']['type'] != 'via':
            raise ValueError('I haven\'t seen this attribute type before! Please report an issue!')
        if layout_object['connection_indexes'] != None:
            raise ValueError('I haven\'t seen connection_indexes used before! Please report an issue!')
        if layout_object['flip'] != False:
            raise ValueError('I haven\'t seen vias flipped before! Please report an issue!')
        if layout_object['rotation'] != 0:
            raise ValueError('I haven\'t seen vias rotated before! Please report an issue!')
        if len(layout_object) != 7:
            raise ValueError('Unexpected number of layout_object elements! Please report an issue!')
        if len(layout_object['attributes']) != 10 and len(layout_object['attributes']) != 9:
            print(len(layout_object['attributes']))
            raise ValueError('Unexpected number of layout_object attributes! Please report an issue!')
            
        
        bounding_box_x = bounds['max_x'] - bounds['min_x']
        translate_x = bounds['min_x']
        translate_x += bounding_box_x / 2
        
        bounding_box_y = bounds['max_y'] - bounds['min_y']
        translate_y = bounds['min_y']
        translate_y += bounding_box_y / 2
        
        x = nmToMm(layout_object['x'] - translate_x)
        y = nmToMm(layout_object['y'] - translate_y)
        
        location = [ x, y ]
        footprint = createViaFootprint(layout_object['attributes'])
        
        via = {
            'assembly': { 'refdef': { 'show': False } },
            'footprint': footprint,
            'layer': 'bottom', #Todo: put some smarts in here
            'location': location,
            'rotate': 0,
            'silkscreen': { 'refdef': { 'show': False } }
        }
        
        vias[str(count)] = via
       

    
    print(count, "vias processed")
    return({ 'vias': vias })
    
def createViaFootprint(attributes):
    pins = { 'via': 0 }
    #todo: create footprint
    return 'via'
    
def nmToMm(nm):
    return (int(nm) / 1000000)