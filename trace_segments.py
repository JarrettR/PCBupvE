#!/usr/bin/python

import json 

def upvTraceSegments(upv_trace_segments):
    """
    Routes
    """
    routes = []
    bottom = []
    top = []
    count = 0
    
    for trace_segment in upv_trace_segments:
        count += 1
        
        #Error handling for future improvement
        if trace_segment['trace_type'] != 'straight':
            raise ValueError('I haven\'t seen this trace type before! Please report an issue!')
            
        print(trace_segment['layer'])
        line = {
            #In px
            'stroke-width': nmToPx(trace_segment['width']),
            'style': 'stroke',
            'type': 'path'
        }
        if trace_segment['layer'] == 'top copper':
            top.append(line)            
        elif trace_segment['layer'] == 'bottom copper':
            bottom.append(line)
        else:
            raise ValueError('I haven\'t seen this trace type before! Please report an issue!')

    print(count, "trace_segments processed")
    print(top)
    
def nmToPx(nm):
    #Better use Inkscape 0.92 or later
    return (96 * (nm * 0.0000000393701))