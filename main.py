#!/usr/bin/python

import os
import json 
import argparse

from pcbmode.utils.json import dictFromJsonFile
from component_instances import upvComponentInstances
from components import upvComponents
from nets import upvNets
from paths import upvPaths
from layout_objects import upvLayoutObjects
from trace_segments import upvTraceSegments


#Old Upv JSON spec
#https://forum.upverter.com/uploads/default/86/5809bf9f391807c1.pdf

class upvToPme(object):
    def __init__(self):

        self.routes = {}
        # parse arguments
        args = self.argSetup()
        self.cmdline_args = args.parse_args()

        # input in Upverter OpenJSON format
        input_name = self.cmdline_args.filein[0]
        if self.cmdline_args.boards is not None:
            self.board_name = self.cmdline_args.boards[0]

        self.json_dict = dictFromJsonFile(input_name)

        #This project built on version 0.3.0
        print("Input file loaded, OpenJSON format version:", self.json_dict['version']['file_version'])
        
        self.convert()
        
    def argSetup(self):
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
                          help='Output will replace all files in specified board\'s directory')


        return args


    def process_category(self, category, data):
        print(category.ljust(22), ' - ', end='')
        
        if category == "component_instances":
            self.component_instances = upvComponentInstances(data, self.bounds)
        elif category == "components":
            self.components = upvComponents(data)
                
        elif category == "design_attributes":
            print("Not yet implemented")
        elif category == "layer_options":
            print("Not yet implemented")
        elif category == "layout_bodies":
            print("Not yet implemented")
        elif category == "layout_body_attributes":
            print("Not yet implemented")
        elif category == "layout_objects":
            self.routes.update(upvLayoutObjects(data, self.bounds))
        elif category == "module_instances":
            print("Not yet implemented")
        elif category == "modules":
            print("Not yet implemented")
        elif category == "named_regions":
            print("Not yet implemented")
        elif category == "nets":
            upvNets(data)
        elif category == "paths":
            self.outline, self.bounds = upvPaths(data)
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
            self.routes.update(upvTraceSegments(data, self.bounds))
        elif category == "version":
            print("Nothing to be done")
        else:
            print("Unknown")
        

    def saveJSON(self, filename, data):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)

    def mergeDefaults(self, filename):
        with open('defaults.json') as f:
            data = json.load(f)
            
        data['components'] = self.component_instances
        data['outline']['shape']['value'] = self.outline
        
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)

    def convert(self):
        print("")
        print("Processing categories...")
        print("")
        
        self.outline, self.bounds = upvPaths(self.json_dict['paths'])
        
        for category in self.json_dict:
            self.process_category(category, self.json_dict[category])
            
        #Outlines, component instances
        self.mergeDefaults('outputs/default.json')
        
        #Routes
        self.saveJSON('outputs/routes.json', self.routes)
        
        #Components
        for component in self.components:
            self.saveJSON('outputs/%s.json' % component, self.components[component])


        print("Done!")


if __name__ == "__main__":
    obj = upvToPme()
