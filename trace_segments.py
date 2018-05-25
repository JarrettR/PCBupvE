#!/usr/bin/python

import json 

def upvTraceSegments(upv_trace_segments, bounds):
    """
    Routes
    """
    bottom = {}
    top = {}
    count = 0
    
    for trace_segment in upv_trace_segments:
        count += 1
        
        #Error handling for future improvement
        #All of these will probably get triggered as soon as someone uses curved lines
        if trace_segment['trace_type'] != 'straight':
            raise ValueError('I haven\'t seen this trace type before! Please report an issue!')
        if len(trace_segment['control_points']) > 0:
            raise ValueError('I haven\'t seen trace_segment control points used before! Please report an issue!')
        if len(trace_segment) != 6:
            raise ValueError('Wrong number of trace_segment children! Please report an issue!')
            
        translate_x = bounds['max_x'] - bounds['min_x']
        translate_x += translate_x / 2
        
        translate_y = bounds['max_y'] - bounds['min_y']
        #translate_y += translate_y / 2
            
        
        value = 'M ' + \
            str(nmToMm(trace_segment['p1']['x'] - translate_x)) + ',' + \
            str(-1 * nmToMm(trace_segment['p1']['y'] - translate_y)) + ' ' + \
            str(nmToMm(trace_segment['p2']['x'] - translate_x)) + ',' + \
            str(-1 * nmToMm(trace_segment['p2']['y'] - translate_y))
        line = {
            #In px
            'stroke-width': nmToMm(trace_segment['width']),
            'style': 'stroke',
            'type': 'path',
            'value': value
        }
        if trace_segment['layer'] == 'top copper':
            top[str(count)] = line           
        elif trace_segment['layer'] == 'bottom copper':
            bottom[str(count)] = line           
        else:
            raise ValueError('I haven\'t seen this trace type before! Please report an issue!')

    routes = {
        'routes': {'top': top, 'bottom': bottom}
    }
    
    print(count, "trace_segments processed")
    return(routes)
    
def nmToMm(nm):
    return (int(nm) / 1000000)