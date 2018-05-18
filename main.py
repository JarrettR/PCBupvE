#!/usr/bin/python

import os
import json 
import argparse


try:
    from os import getcwdu as getcwd
except:
    from os import getcwd as getcwd

from pcbmode.utils.json import dictFromJsonFile
    
    
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


def process_category(category):
    print(category, ' - ', end='')
    
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
        print("Not yet implemented")
    elif category == "module_instances":
        print("Not yet implemented")
    elif category == "modules":
        print("Not yet implemented")
    elif category == "named_regions":
        print("Not yet implemented")
    elif category == "nets":
        print("Not yet implemented")
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
        print("Not yet implemented")
    elif category == "version":
        print("Not yet implemented")
    else:
        print("Unknown")

def convert():

    # parse arguments
    args = argSetup()
    cmdline_args = args.parse_args()

    # input in Upverter OpenJSON format
    input_name = cmdline_args.filein[0]
    if cmdline_args.boards is not None:
        board_name = cmdline_args.boards[0]

    json_dict = dictFromJsonFile(input_name)
    
    print("Input file loaded, OpenJSON format version:", json_dict['version']['file_version'])
    
    print("")
    print("Processing categories...")
    print("")
    for category in json_dict:
        process_category(category)
    #json.dumps(json_dict)


    print("Done!")



if __name__ == "__main__":
    convert()