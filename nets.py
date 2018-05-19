#!/usr/bin/python

import json 

def upvNets(upv_nets):
    """
    Schematic nets
    """
    routes = []
    count = 0
    
    for net in upv_nets:
        #print(net['net_id'])
        count += 1
        
        #Error handling for future improvement
        if net['net_type'] != "nets":
            raise ValueError('I haven\'t seen this net type before! Please report an issue!')
            
        

    print(count, "nets unprocessed, still todo")