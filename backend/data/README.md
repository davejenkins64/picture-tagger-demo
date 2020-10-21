# Picture Tagger Server Database
This directory contains the "database" for the picture tagger server.
As a lazy first cut, it just contains 2 files.

Future work could include using CSV files instead of this format, or sqllite
or even mysql.  But for now, there are two files, one with data on the pictures
and the other with data on the user-assigned tags.

## unique_pictures_sorted
Each line in this file is a data for a single picture.  

'''
0000:00:00 00:00:00 1397159242 "desktop/windows/Program Files/Jasc Software Inc/Paint Shop Photo Album/Samples/Scenery/Panorama004.jpg"
'''

1. The first "field" is the date and time, in the format YYYY:MM:DD HH:MM:SS.
2. The second "field" is the cksum of the jpeg file
3. The third "field" is the full path to the picture file, quote-delimited

## tags
Each line in the tag file has the unique identifier of a picture 
and the currently assigned tags for that picture.

'''
0000:00:00 00:00:00 1397159242 ""
'''

1. The first "field" is again the date/time, in the format YYYY:MM:DD HH:MM:SS.
2. The second "field" is a comma and space delimited set of tags assigned
to this picture.  Note, no tags are empty quotes, but any tags always end in a comma and a space.

# Tools
This suite pre-supposes that the unique_pictures_sorted file has been created
from all of the pictures on disk under the PICTURE_HOME directory.
I believe I used find to find all pictures and piped the output through
exiftool to capture the creation date and time.  
I then re-formatted this to the YYYY:MM:DD HH:MM:SS format.  The second
field is calculated with the cksum command.
Then, simply emit a "record" of these 3 fields into an unsorted data file.

We now have captured all pictures in a file. 
We can use sort to sort them, and another script to make the 
records in the file unique by the date/time/cksum key (below).  
This was needed because over time multiple copies
of some pictures where uploaded multiple times in different locations
but we don't want our user to have to tag the same picture multiple times.

## mk_picture_database.sh
Run this from the directory that is the root of where
the pictures are stored: WEBSERVER_PICTURE_ROOT.
Output file will be sorted but not unique.
This calls parse_exiftool_out.pl to get the meta data into our format.

## mk_unique.pl

Given a sorted picture file in the correct format, this script can emit only 
the first copy of any picture with the same date/time/cksum.

## parse_exiftool_out.pl
Convert exiftool meta data into our datestring format.

## fix_permissions

I configured my web server to treat my PICTURE_HOME as the document root, but
then ran into issues because the web server runs as nobody while the backup
directories are owned by the backup user.  This script will allow nobody to
read these files and directories by alloing ALL users to read them.
If that isn't desired, copy the files to the document root recursivly?



