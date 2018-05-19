#!/usr/bin/python

import json 

from pprint import pprint

def upvLayoutObjects(upv_layout_objects):
    """
    Layout Objects
    So far only seen vias in this
    """
    '''
    "12d213e32": {
      "assembly": {
        "refdef": {
          "show": false
        }
      },
      "footprint": "via",
      "layer": "bottom",
      "location": [
        9.876513,
        7.307817
      ],
      "rotate": 0,
      "silkscreen": {
        "refdef": {
          "show": false
        }
      }
    },
    '''
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
            
        
        location = [ nmToPx(layout_object['x']), nmToPx(layout_object['y']) ]
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
    
def nmToPx(nm):
    #Better use Inkscape 0.92 or later
    return (96 * (nm * 0.0000000393701))