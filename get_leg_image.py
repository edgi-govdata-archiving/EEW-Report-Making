import csv, requests
import urllib
import wget
import pdb

url = "https://govtrack.us/static/legislator-photos/{}-200px.jpeg"

with open( 'legislators-current.csv', 'r' ) as csvfile:
    # pdb.set_trace()
    csv_reader = csv.DictReader( csvfile, delimiter=',' )
    for row in csv_reader:
        print( row['full_name'] )
        govtrack_id = row['govtrack_id']
        leg_url = url.format( govtrack_id )
        if ( row['type'] == 'sen' ):
            filename = '{}_sen{}.jpeg'.format( row['state'],
                   row['senate_class'] )
        elif ( row['type'] == 'rep' ):
            filename = '{}{}_rep.jpeg'.format( row['state'],
                   row['district'] )
        try:
            wget.download( leg_url, 'CD_images/{}'.format( filename ))
        except urllib.error.HTTPError:
            print( "Photo not available." )
