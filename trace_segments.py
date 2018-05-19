#!/usr/bin/python

import json 

def upvTraceSegments(upv_trace_segments):
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
            
        
        value = 'm ' + \
            str(nmToPx(trace_segment['p1']['x'])) + ',' + \
            str(nmToPx(trace_segment['p1']['y'])) + ' c ' + \
            str(nmToPx(trace_segment['p2']['x'])) + ',' + \
            str(nmToPx(trace_segment['p2']['y']))
        line = {
            #In px
            'stroke-width': nmToPx(trace_segment['width']),
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
    
def nmToPx(nm):
    #Better use Inkscape 0.92 or later
    return (96 * (nm * 0.0000000393701))