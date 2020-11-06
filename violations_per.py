#!/usr/bin/python

import pathlib, fnmatch, re, csv
import sys, argparse
import pdb

def main( argv ):
    parser = argparse.ArgumentParser( prog='violations_per.py', description=\
       'Consolidate all violationsper1000_pg4 files into violationsper1000_all.csv' )
    parser.add_argument( '--region', choices=['states', 'cds'], required=True )
    parser.parse_args( argv )

    region = argv[1]
    if ( region == 'states' ):
        region_pat = re.compile( '[A-Z][A-Z]0?$' )
        out_filename = 'violationsper1000_CWA_all_states.csv'
    else:
        region_pat = re.compile( '[A-Z][A-Z][0-9]' )
        out_filename = 'violationsper1000_CWA_all_cds.csv'
    
    base_filename = 'violationsper1000_All_pg4'
    
    currentDir = pathlib.Path('.')
    cd_data = {}
   
    # A CD might have two files that match the base_filename pattern:
    # violationsper1000_All_pg4_AL_2-102320.csv and
    # violationsper1000_All_pg4_AL-102320.csv if it has been moved into
    # the CD's directory from the state's.  The Rmd needs both of these.
    # For this consolidation, we only want to include the CD's data when
    # region == 'cd'.

    col_names = ['CD/State', 'Num per 1000', 'Region']
    region_name = 'State' if region == 'states' else 'Congressional District'
    with open( out_filename, 'w' ) as csvfile:
        writeCSV = csv.writer( csvfile, delimiter=',' )
        writeCSV.writerow( col_names )
        for file_obj in currentDir.iterdir():
            c_file = str( file_obj )
            if ( region_pat.match( c_file )):
                viol_filename = base_filename
                if ( region == 'cds' ):
                    # The current directory name will be like AL1, TX22, AL, AL0
                    # We need to put a '-' between the state and cd to match the
                    # filename.
                    viol_filename += '_' + c_file[:2]
                    # States with the digit 0 are those with only 1 district.
                    if ( c_file[2] != '0' ):
                        viol_filename += '-' + c_file[2:]
                file_pat = re.compile( viol_filename )
                # pdb.set_trace()
                for data_file in file_obj.iterdir():
                    viol_file = str( data_file )
                    if ( file_pat.search( viol_file )):
                        # pdb.set_trace()
                        with open( viol_file ) as csvfile:
                            readCSV = csv.reader( csvfile, delimiter=',' )
                            next( readCSV, None )  # skip the header row
                            for row in readCSV:
                                if ( row[0] == 'CWA' ):
                                    if ( region == 'states' and len(c_file) > 2 ):
                                        writeCSV.writerow( [c_file[:2], row[1], region_name ])
                                    else:
                                        writeCSV.writerow( [c_file, row[1], region_name ])
if __name__ == "__main__":
    main( sys.argv[1:] )
