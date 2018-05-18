#!/usr/bin/python

import json 

from pprint import pprint

def upvNetToPCBmodE(upv_nets):
    """
    I think these might be airwires
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