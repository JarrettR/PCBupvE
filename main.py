#!/usr/bin/python

import os
import json
import argparse


try:
    from os import getcwdu as getcwd
except:
    from os import getcwd as getcwd


def argSetup():
    """
    Setup args
    """

    args = argparse.ArgumentParser(description="Upverter Importer",
                      add_help=True)


    return args


def convert():

    # parse arguments
    args = argSetup()
    

    print("Done!")



if __name__ == "__main__":
    convert()