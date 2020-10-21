#!/bin/bash
bindir=$(dirname $0)
tmpdir=/var/tmp/pictures.$$
mkdir $tmpdir
# count on exiftool already recursing for us
# but it can't seem to handle too large directories, so start down 2
for f in */*
do 
	if [ -d "$f" ]
	then
		echo "--- $f ---"
		exiftool -r "$f" | egrep "^(=====|File Type|Create Date)" | $bindir/parse_exiftool_out.pl >> $tmpdir/picture_manifest
	fi
done

# we want to collapse the lines above into a dir/file datestamp, cksum, filename
sort $tmpdir/picture_manifest > picture_manifest
rm -rf $tmpdir

# so, find all files with the same timestamp and compare, 
# emit one copy of each cksum, check that the rest are linked together?
