#!/usr/bin/python

import os
import json 
import argparse

from pcbmode.utils.json import dictFromJsonFile
from nets import upvNets
from layout_objects import upvLayoutObjects
from trace_segments import upvTraceSegments


#Old Upv JSON spec
#https://forum.upverter.com/uploads/default/86/5809bf9f391807c1.pdf
    
def argSetup():
    """
    Setup args
    """

    args = argparse.ArgumentParser(description="Upverter Importer",
                      add_help=True)

    args.add_argument('-f', '--filein', required=True,
                      dest='filein', nargs=1,
                      help='Input file name')
                      
    args.add_argument('-b', '--board-name',
                      dest='boards', required=False, nargs=1,
                      help='Output will replace all files in specelified board\'s directory')


    return args


def process_category(category, data):
    print(category.ljust(22), ' - ', end='')
    
    if category == "component_instances":
        print("Not yet implemented")
    elif category == "components":
        print("Not yet implemented")
    elif category == "design_attributes":
        print("Not yet implemented")
    elif category == "layer_options":
        print("Not yet implemented")
    elif category == "layout_bodies":
        print("Not yet implemented")
    elif category == "layout_body_attributes":
        print("Not yet implemented")
    elif category == "layout_objects":
        vias = upvLayoutObjects(data)
    elif category == "module_instances":
        print("Not yet implemented")
    elif category == "modules":
        print("Not yet implemented")
    elif category == "named_regions":
        print("Not yet implemented")
    elif category == "nets":
        upvNets(data)
    elif category == "paths":
        print("Not yet implemented")
    elif category == "pcb_text":
        print("Not yet implemented")
    elif category == "pins":
        print("Not yet implemented")
    elif category == "pours":
        print("Not yet implemented")
    elif category == "rulers":
        print("Not yet implemented")
    elif category == "shape_poses":
        print("Not yet implemented")
    elif category == "shapes":
        print("Not yet implemented")
    elif category == "trace_segments":
        out = upvTraceSegments(data)
        saveJSON('routes.json', out)
    elif category == "version":
        print("Nothing to be done")
    else:
        print("Unknown")

def saveJSON(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)


def convert():

    # parse arguments
    args = argSetup()
    cmdline_args = args.parse_args()

    # input in Upverter OpenJSON format
    input_name = cmdline_args.filein[0]
    if cmdline_args.boards is not None:
        board_name = cmdline_args.boards[0]

    json_dict = dictFromJsonFile(input_name)
    
    #This project built on version 0.3.0
    print("Input file loaded, OpenJSON format version:", json_dict['version']['file_version'])
    
    print("")
    print("Processing categories...")
    print("")
    for category in json_dict:
        process_category(category, json_dict[category])


    print("Done!")



if __name__ == "__main__":
    convert()