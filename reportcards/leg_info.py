import pdb

import datetime
import json
import urllib.request
import sqlite3
from os import path

def get_since_fields( the_date ):
    mon = the_date.strftime( "%B" )
    day = the_date.strftime( "%-d" )
    year = the_date.strftime( "%Y" )
    suffix = 'th'
    if ( day == '1' or day == '21' or day == '31' ):
        suffix = 'st'
    elif ( day == '2' or day == '22' ):
        suffix = 'nd'
    elif ( day == '3' or day == '23' ):
        suffix = 'rd'
    return '{} {}{}, {}'.format( mon, day, suffix, year ), year

conn = sqlite3.connect( 'leg_info.db' )
cursor = conn.cursor()

legs_url = 'https://theunitedstates.io/congress-legislators/legislators-current.json'

legs = urllib.request.urlopen( legs_url ).read().decode()
obj = json.loads( legs )

govtrack_base = "https://govtrack.us/congress/members/"
wiki_base = "https://en.wikipedia.org/wiki/"

for leg in obj:
    # pdb.set_trace()
    id = leg['id']
    bioguide_id = id['bioguide']
    govtrack_id = id['govtrack']
    full_name = leg['name']['official_full']
    first_name = leg['name']['first']
    last_name = leg['name']['last']
    govtrack_url = '{}{}_{}/{}'.format( govtrack_base, first_name.lower(),
       last_name.lower(), govtrack_id )
    wikipedia_url = '{}{}'.format( wiki_base, id['wikipedia'].replace(' ','_'))
    terms = leg['terms']
    start_date = datetime.date.today()
    party = ''
    sen_rep = ''
    state = ''
    district = ''
    sen_class = ''
    official_url = ''
    for term in terms:
        if ( term['type'] != sen_rep ):
            # Will be true the first time through, and with change rep <--> sen
            sen_rep = term['type']
            start_date = datetime.datetime.strptime( term['start'], '%Y-%m-%d' )
            party = term['party']
            state = term['state']
            if ( sen_rep == 'rep' ):
                district = term['district']
            else:
                sen_class = term['class']
                district = ''
        else:
            this_date = datetime.datetime.strptime( term['start'], '%Y-%m-%d' )
            if ( this_date < start_date ):
                start_date = this_date
            elif ( party != term['party'] ):
                # They changed party after they became sen or rep
                party = term['party']
        try: official_url = term['url']
        except KeyError: pass
    ( since_date, since_year ) = get_since_fields( start_date )
    
    cursor.execute( 
        'insert into legislators ( cd_state, name, party, govtrack_id, ' \
           'bioguide_id, sen_class, since_date, since_year, ' \
           'official_url, govtrack_url, wikipedia_url ) ' \
           'values ( ?,?,?,?,?,?,?,?,?,?,? )',
           ( state + str( district ), full_name, party, govtrack_id, bioguide_id,
             sen_class, since_date, since_year, official_url, govtrack_url,
             wikipedia_url ))
    conn.commit()

