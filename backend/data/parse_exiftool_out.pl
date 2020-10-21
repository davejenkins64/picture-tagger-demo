#!/usr/bin/perl -w

use strict;
use FileHandle;

sub process_one($$$) {
	my ($filename, $type, $ts) = @_;
	if ((defined($filename))
	&& (defined($type))
	&& ('JPEG' eq $type)
	&& (defined($ts))) {
		my $fh = FileHandle->new("cksum \"$filename\" |") 
			|| die "failed to cksum $filename\n";
		my $line = $fh->getline();
		my ($sum, $size, $rest) = split(/ /, $line, 3);
		$fh->close();
		print "$ts $sum \"$filename\"\n";
	}
}

my $filename;
my $type;
my $ts;
while (my $line = <>) {
	chomp($line);
	if ($line =~ m/======== (.*)/) {
		my $newfilename = $1;
		process_one($filename, $type, $ts);
		$filename = $newfilename;
		undef $type;
		undef $ts;
	}
	elsif ($line =~ m/Create Date *: (.*)/) {
		$ts = $1;
	}
	elsif ($line =~ m/File Type *: (.*)/) {
		$type = $1;
	}
}
process_one($filename, $type, $ts);

