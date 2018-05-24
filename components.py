#!/usr/bin/python

import json, pickle, hashlib, math

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
    name = []

    for component in upv_components:
        count += 1

        if len(upv_components[component]['footprints']) > 0:
            used_count += 1

            #todo: investigate multiple footprints
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
        else:
            data = {
                'pins': {},
                'layout': {},
                'pads': {},
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

        #todo: determine if this even matters
        if pin['attributes']['type'] == 'padstack':
            pass
        elif pin['attributes']['type'] == 'plated through hole':
            #todo: flesh out
            drills = { 'diameter': nmToMm(pin['attributes']['internal_diameter']) }
        elif pin['attributes']['type'] == 'center cross':
            break
        else:
            raise ValueError("I haven\'t seen pin %s type before! Please report an issue!" % pin['attributes']['type'])
            
        rotate = pin['rotation'] * 180
        x = nmToMm(pin['x'])
        y = -1 * nmToMm(pin['y'])
        #todo: attrib-layers, flip

        print(rotate, math.cos(math.radians(rotate)))
        if ('width' in pin['attributes']) == True:
            shapes['width'] = nmToMm(pin['attributes']['width'])
            x += (shapes['width'] / 2) * math.cos(math.radians(rotate))
            y += (shapes['width'] / 2) * math.sin(math.radians(rotate))
        if ('height' in pin['attributes']) == True:
            shapes['height'] = nmToMm(pin['attributes']['height'])
            #y += shapes['height'] / 2
            x -= (shapes['height'] / 2) * math.sin(math.radians(rotate))
            y += (shapes['height'] / 2) * math.cos(math.radians(rotate))
            

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
            if ('hole_shape' in pin['attributes']) == True:
                shapes['type'] = 'circle'
                shapes['diameter'] = nmToMm(pin['attributes']['plating_diameter'])
        elif pin['attributes']['shape'] == 'rectangle':
            shapes['type'] = 'rect'
        elif pin['attributes']['shape'] == 'rounded rectangle':
            #todo: design this
            #"radii": {"tl": 0.33, "tr": 0.33, "bl": 0.33, "br": 0.33}
            shapes['type'] = 'rect'
        else:
            raise ValueError("I haven\'t seen component %s before! Please report an issue!" % pin['attributes']['shape'])
            
        if ('drills' in locals()) == True:
            name = genName([shapes, drills])
            pads[name] = { 'shapes': [shapes], 'drills': [drills] }
        else:
            name = genName([shapes])
            pads[name] = { 'shapes': [shapes] }
        
        
        pins[len(pins)] = { 'layout': { 'pad': name, 'rotate': rotate, 'location': [x, y] } }

    return pads, pins

def genName(entropy):
    #Unique name
    m = hashlib.md5()
    m.update(pickle.dumps(entropy))
    name = m.hexdigest()
    return name


def nmToMm(nm):
    return (int(nm) / 1000000)