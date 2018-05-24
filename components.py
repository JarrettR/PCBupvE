#!/usr/bin/python

import json, pickle, hashlib

from pprint import pprint

# Pad "type" eg. mounting hole, smd pad, through-hole
pads = {}
# Instance of type pad
pins = {}

def upvComponents(upv_components):
    """
    Components
    Only really care about footprints.
    Even generic passives will be unique if they have different V/C/R/Whatever, so there's
    a lot of footprint duplication here.
    """
    count = 0
    used_count = 0

    components = {}

    for component in upv_components:
        count += 1

        if len(upv_components[component]['footprints']) > 0:
            used_count += 1

            pads, pins = genComponents(upv_components[component]['footprints'][0]['gen_objs'])
            
            #todo
            layout = upv_components[component]['footprints'][0]

            data = {
                'pins': pins,
                'layout': {},
                'pads': pads,
                'meta': upv_components[component]['name']
                }

            components[component] = data

    print(used_count, "components processed of", count)
    return(components)

def genComponents(data):
    pins = {}
    pads = {}
    count = 0

    for pin in data:
        name = ''
        shapes = {}
        drills = {}

        #todo: determine if this even matters
        if pin['attributes']['type'] == 'padstack':
            pass
        elif pin['attributes']['type'] == 'plated through hole':
            #todo: flesh out
            drills = {'diameter': nmToMm(pin['attributes']['internal_diameter'])}
        elif pin['attributes']['type'] == 'center cross':
            break
        else:
            raise ValueError("I haven\'t seen pin %s type before! Please report an issue!" % pin['attributes']['type'])

        if ('width' in pin['attributes']) == True:
            shapes['width'] = nmToMm(pin['attributes']['width'])
        if ('height' in pin['attributes']) == True:
            shapes['height'] = nmToMm(pin['attributes']['height'])
            
        rotate = pin['rotation']
        x = nmToMm(pin['x'])
        y = -1 * nmToMm(pin['y'])
        #todo: attrib-layers, flip

        #layer
        if pin['layer'] == 'top copper':
            shapes['layers'] = ['top']
        elif pin['layer'] == 'top component':
            shapes['layers'] = ['top']
        elif pin['layer'] == 'bottom copper':
            shapes['layers'] = ['bottom']
        else:
            raise ValueError("I haven\'t seen component layer %s before! Please report an issue!" % pin['layer'])

        #shape
        #todo: circle, path
        if ('shape' in pin['attributes']) == False:
            #whoops
            pass
            #print('')
        elif pin['attributes']['shape'] == 'rectangle':
            shapes['type'] = 'rect'
        elif pin['attributes']['shape'] == 'rounded rectangle':
            #todo: design this
            #"radii": {"tl": 0.33, "tr": 0.33, "bl": 0.33, "br": 0.33}
            shapes['type'] = 'rect'
        else:
            raise ValueError("I haven\'t seen component %s before! Please report an issue!" % pin['attributes']['shape'])
            
        #Unique name
        m = hashlib.md5()
        m.update(pickle.dumps(shapes) + pickle.dumps(drills))
        name = m.hexdigest()
        pads[name] = { 'shapes': [shapes], 'drills': drills }
        
        pins[len(pins)] = { 'layout': { 'pad': name, 'rotate': rotate, 'location': [x, y] } }

    return pads, pins


def nmToMm(nm):
    return (int(nm) / 1000000)