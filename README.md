# EEW-Report-Making
Scripts and process for moving from the Jupyter notebook to the R-based CD and State report cards

The AllPrograms Jupyter notebook in the ECHO-Cross-Program repository can be used to generate CSV data files for one, a few or many
congressional districts or states.  The process and programs in this repository use that data and gather additional
information such as maps and legislator material to enable the generation of report cards using an R Markdown template.

### Getting data from the AllPrograms notebook
The all_cds.csv file in this repository contains a list of all congressional districts and states.  The two pieces of information
per line are the two-letter state abbreviation and a congressional district number.  States simply use a 0 in the congressional
district field.

The AllPrograms notebook can take a CSV file such as all_cds.csv as input and will work its way through all of the congressional districts 
and states.  In practice the number of entries in all_cds.csv may exhaust the memory capabilities of the computer the notebook is run on,
since all data is compiled and stored in memory before being processed.  For that reason it is preferrable to break the all_cds.csv
file up into chunks of 75-100 lines and process those separately.

AllPrograms will write its results into an Output subdirectory.  Each CD will be written into a sub-directory of Output made up of the state and CD, such as AL1 for Alabama's first district.  This sub-directory will contain all of the file results for the district.  For a state there is no CD in the directory's name.  Alabama's statewide data is in directory AL, for example.

### Consolidate violation data from all CDs

The report card's dotplot of violations per 100 facilities needs the violationsper1000__<State>-<district>-<datestamp>.csv for every congressional district to be consolidated into a single report.  Running the violations_per.py script will accomplish this. The following steps should be followed:
  
1.  Run violations_per.py from the parent directory of all the CD/State directories.  If CD_Dirs is the parent directory containing directories AL, AL1, etc., run the script from CD_Dirs.  Make sure all directories that you want to be included are present.
2.  Run the script twice--once for CDs and once for states:
    violations_per.py --region cds
    violations_per.py --region states
3.  The files produced will be violationsper1000_CWA_all_cds.csv and violationsper1000_CWA_all_states.csv.  These need to be combined into a single file, violationsper1000_CWA_all_cds.csv, which needs to be placed in the nationalstats directory of CD-report.

All CD directories need to have their state's violationsper1000_All file copied in from the state directory.  This can be done with the violations_state.py script.  Run this script from the same directory as before--i.e, the CD_Dirs directory.

### Maps for districts

This is a link to a zip file containing maps of all districts: https://drive.google.com/file/d/1TitM460QfU7nWeigApwhvSN6cQEBmGtt/view?usp=sharing 

Maps can be generated with the RegionMaps notebook in the ECHO-Cross-Programs repository.  The notebook now sizes and bounds the maps so they will be an appropriate size and won't need hand editing as they did in the past.  The notebook needs to be run on a system with a headless Chrome installed, and with a web server.  The HTML maps from the notebook run on the ECHO data for the district are put into a directory known by the web server and opened automatically by Chrome.  The Selenium package can then take a screen shot to produce the needed .png file.  (The ECHO data often has facilities outside of the district which have distorted the bounds of the map.  Such facilities are discarded in the current version of the RegionMaps notebook.)

### Legislator information

#### Legislator photo

The image for each legislator is obtained with a script (get_leg_image.py) that retrieves the image from their page at govtrack.us, using a govtrack_id that is published in the legislators-current.csv file from https://theunitedstates.io/congress-legislators/legislators-current.csv.  The images are saved in a CD_images directory in a format like AK0_rep.jpeg, AL1_rep.jpeg for representatives, and AK_sen2.jpeg for senators.  The digit following "sen" in the senator's file name refers to a field called "senate_class" in legislators-current.csv.  This needs to be used to distinguish between the two senators in a state.  The "senate_class" field will need to be added to the nationalstats/housememberinfo.csv that is used by R to generate the report card.

#### Committee membership


