#!/usr/bin/perl -w
#
use strict;

my $saw_key = '';
while (my $line = <>) {
    my ($date, $time, $cksum, $file) = split(/ /, $line, 4);
    my $key = "$date $time $cksum";
    if ($saw_key ne $key) {
        print($line);
        $saw_key = $key;
    }
}
