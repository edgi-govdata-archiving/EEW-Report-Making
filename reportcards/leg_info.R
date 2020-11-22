library(RSQLite)
library(rlist)
cd_state = 'TX22'
conn <- dbConnect( RSQLite::SQLite(), "leg_info.db")
legislator = dbGetQuery( conn, "select * from legislators where cd_state=?",
                         params=c( cd_state ))
leg_info <- list( name=legislator$name, party=legislator$party, sen_class=legislator$sen_class,
                  since_date=legislator$since_date, since_year=legislator$since_year,
                  official_url=legislator$official_url, govtrack_url=legislator$govtrack_url,
                  wikipedia_url=legislator$wikipedia_url, twitter=legislator$twitter,
                  facebook=legislator$facebook )
committee_membership = dbGetQuery( conn,
                        "select * from committee_members where bioguide_id = ?",
                        params=c(legislator$bioguide_id))
committees <- list()
subcommittees <- list()
for ( row in 1:nrow( committee_membership )) {
  committee_id <- committee_membership[ row, "committee_id" ]
  subcommittee_id <- committee_membership[ row, "subcommittee_id" ]
  if ( nchar( subcommittee_id ) == 0 ) {
    committee <- dbGetQuery( conn,
                        "select * from committees where committee_id = ?",
                        params=c(committee_id))
    # print( committee )
    committees[[committee_id]] <- list( committee=committee )
  } else {
    subcommittee <- dbGetQuery( conn,
                                "select *,? as rank from sub_committees where committee_id=? and subcommittee_id=?",
                                params=c(committee_membership[row,"rank"],committee_id,subcommittee_id))
    # print( subcommittee )
    subcommittees[[subcommittee_id]] <- subcommittee
    committees[[committee_id]] <- list.append( committees[[committee_id]], subcommittee )
  }
}
# print( leg_info )
dbDisconnect( conn )

# length(committees$HSIF)
# committees$HSIF[[1]]$name
# committees$HSIF[[4]]$name
# committees[[1]]$committee$jurisdiction
# committees$HSIF$committee$jurisdiction

print( sprintf( "Name: %s", leg_info$name ))
print( sprintf( "Party: %s", leg_info$party ))
if ( leg_info$sen_class == '' ) {
  print( "Representative" )
} else {
  print( "Senator")
}
print( sprintf( "In this office since %s", leg_info$since_date ))
print( sprintf( "In this office since %s", leg_info$since_year ))
print( sprintf( "<a href=%s>Official web page</a>", leg_info$official_url))
print( sprintf( "<a href=%s>Govtrack web page</a>", leg_info$official_url))
print( sprintf( "<a href=%s>Wikipedia web page</a>", leg_info$official_url))
print( sprintf( "Twitter: %s", leg_info$twitter ))
print( sprintf( "Facebook: %s", leg_info$facebook ))

for ( committee in committees ) {
  # print( committee[[1]]$name )
  print( sprintf( "Committee Name: %s", committee[[1]]$name ))
  print( sprintf( "Jurisdiction: %s", committee[[1]]$jurisdiction ))
  print( sprintf( "<a href='%s'>Committee web page</a>", committee[[1]]$url ))
  for ( i in 2:length(committee) ) {
    print( sprintf( "Subcommittee: %s, Rank: %s",
                    committee[[i]]$name, committee[[i]]$rank ))
  }
}

