#!/usr/bin/python

import json

def upvComponentInstances(upv_component_instances):
    """
    Component Instances
    Actual footprints placed on PCB, references upvComponent
    """
    count = 0
    used_count = 0

    component_instances = {}

    for component_instance in upv_component_instances:
        count += 1
        
        if ('footprint_pos' in component_instance) == True:
            used_count += 1
            name = component_instance['attributes']['refdes']
            
            location = [nmToMm(component_instance['footprint_pos']['x']), nmToMm(component_instance['footprint_pos']['y'])]

            silkscreen = {
                'refdef': {
                    'location': [0, 2],
                    'rotate': 0,
                    'show': True
                    }
                }
                
            data = {
                'footprint': component_instance['library_id'],
                'layer': component_instance['footprint_pos']['side'],
                'location': location,
                'rotate': component_instance['footprint_pos']['rotation'] * 180,
                'show': True,
                'silkscreen': silkscreen
                }

            component_instances[name] = data

    print(used_count, "component instances processed of", count)
    return(component_instances)

def nmToMm(nm):
    return (int(nm) / 1000000)