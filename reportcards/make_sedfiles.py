from csv import reader
import sys, argparse
import pdb

def main( argv ):
    parser = argparse.ArgumentParser( prog='make_sedfiles.py', 
       description=\
       'Make a sedfile for each of the CDs/States in the input CSV,' \
       ' and a make_reports.sh that will call the sedfiles' )
    parser.add_argument( '-c', '--cds_file', required=True,
        help='The CDs to work with' )
    parser.add_argument( '-s', '--states_file', required=True,
        help='The state names' )
    my_args = parser.parse_args()

    # pdb.set_trace()
    cds_todo_file = my_args.cds_file
    states_file = my_args.states_file

    template_filename = "NY14_template.Rmd"
    template_state_cd = "New York's 14th" 
    template_cd = "14th"
    template_st = "NY"
    template_data_date = "102320"
    data_date = "102320"
    bash_name = "make_reports.sh"
    
    with open( cds_todo_file, 'r' ) as read_obj:
        csv_reader = reader( read_obj )
        state_cds = list( map( tuple, csv_reader ))
    with open( states_file, 'r' ) as read_obj:
        csv_reader = reader( read_obj )
        state_name_list = list( map( tuple, csv_reader ))
    state_names = {}
    for state_abbr, state_name in state_name_list:
        state_names[ state_abbr ] = state_name
    with open( bash_name, "w" ) as bash_obj:
        for state, cd in state_cds:
            target_file = "New/{}{}_2020.Rmd".format( state, cd )
            cd = int( cd )
            sed_name = "SEDs/sedfile_{}{}.txt".format( state, cd )
            with open( sed_name, "w" ) as write_obj:
                suff = "th"
                if ( cd == 1 or cd == 21 or cd == 31 or cd == 41 or cd == 51 ):
                    suff = "st"
                elif ( cd == 2 or cd == 22 or cd == 32 or cd == 42 or cd == 52 ):
                    suff = "nd"
                elif ( cd == 3 or cd == 23 or cd == 33 or cd == 43 or cd == 53 ):
                    suff = "rd"
                str = "s/{}/{} {}{}/g\n".format( template_state_cd, state_names[state],
                       cd, suff )
                write_obj.write( str )
                str = "s/NY 14/{} {}/g\n".format( state, cd )
                write_obj.write( str )
                str = "s/_NY-14/_{}-{}/g\n".format( state, cd )
                write_obj.write( str )
                str = "s/NY14/{}{}/g\n".format( state, cd )
                write_obj.write( str )
                str = "s/_NY-/_{}-/g\n".format( state )
                write_obj.write( str )
                if ( template_data_date != data_date ):
                    str = "s/{}/{}\n".format( template_data_date, data_date )
                    write_obj.write( str )
            str = "sed -f {} {} > {}\n".format( sed_name, template_filename,
                                                target_file )
            bash_obj.write( str ) 

if __name__ == "__main__":
    main( sys.argv[1:] )


