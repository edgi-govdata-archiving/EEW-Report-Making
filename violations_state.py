#!/usr/bin/python

import pathlib, fnmatch, re, csv
import glob
import sys, argparse
from shutil import copy
import pdb

def main( argv ):
    parser = argparse.ArgumentParser( prog='violations_per.py', description=\
       'Consolidate all violationsper1000_pg4 files into violationsper1000_all.csv' )
    parser.parse_args( argv )

    state_pat = re.compile( '[A-Z][A-Z]0?$' )
    
    base_filename = 'violationsper1000_All_pg4'
    
    currentDir = pathlib.Path('.')

    for file_obj in currentDir.iterdir():
        c_dir = str( file_obj )
        if ( state_pat.match( c_dir )):
            state = c_dir
            viol_filename = base_filename + '_' + state + '-[0-9]*.csv'
            file1 = glob.glob( state + '/' + viol_filename )[0]
            for file_obj2 in currentDir.iterdir():
                c_dir2 = str( file_obj2 )
                if state != c_dir2 and state in c_dir2:
                    copy( file1, c_dir2 )
                    
if __name__ == "__main__":
    main( sys.argv[1:] )
