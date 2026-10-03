#!/bin/sh
# Read RLPM's local file records: Shelly has no CLI file-owner query yet.
exec /usr/bin/perl - <<'PERL'
use strict;
use warnings;
use File::Find qw(find);

my $basedir = '/usr/lib/perl5';
my $dbdir = '/var/lib/shelly/local';
my $perlver = sprintf '%vd', $^V;
$perlver =~ s/\.\d+$//;
exit 0 unless -d $basedir;

opendir(my $dirs, $basedir) or die "Cannot read $basedir: $!\n";
my @old_dirs = sort grep { /^\d+\.\d+$/ && $_ ne $perlver && -d "$basedir/$_" } readdir $dirs;
closedir $dirs;
exit 0 unless @old_dirs;

# Index package names and their file lists once, without invoking a package
# transaction from inside a transaction hook. These paths are inside its root.
my %owners;
my $ownership_available = -d $dbdir;
if ($ownership_available) {
    opendir(my $records, $dbdir) or die "Cannot read $dbdir: $!\n";
    for my $record (sort grep { !/^\./ && -d "$dbdir/$_" } readdir $records) {
        open(my $desc, '<', "$dbdir/$record/desc") or die "Cannot read $record/desc: $!\n";
        my $name;
        while (my $line = <$desc>) {
            if ($line eq "%NAME%\n") { $name = <$desc>; last; }
        }
        close $desc;
        die "Missing package name in $record/desc\n" unless defined $name;
        chomp $name;
        open(my $files, '<', "$dbdir/$record/files") or die "Cannot read $record/files: $!\n";
        my $in_files = 0;
        while (my $line = <$files>) {
            chomp $line;
            if ($line =~ /^%/) { $in_files = $line eq '%FILES%'; next; }
            next unless $in_files && length $line;
            $line =~ s{/$}{};
            next unless index("/$line", "$basedir/") == 0;
            $owners{"/$line"}{$name} = 1;
        }
        close $files;
    }
    closedir $records;
}

for my $version (@old_dirs) {
    my $dir = "$basedir/$version";
    my @files;
    find({ no_chdir => 1, wanted => sub { push @files, $File::Find::name if -f $_ || -l $_ } }, $dir);
    next unless @files;
    print "WARNING: '$dir' contains modules which will NOT be used by the installed perl interpreter.\n";
    unless ($ownership_available) {
        print " -> Shelly package database unavailable at $dbdir; ownership could not be checked.\n";
        next;
    }
    my %packages;
    for my $path (keys %owners) {
        next unless $path eq $dir || index($path, "$dir/") == 0;
        $packages{$_} = 1 for keys %{$owners{$path}};
    }
    if (%packages) {
        print " -> Rebuild the affected packages: ", join(' ', sort keys %packages), "\n";
    }
    my @unowned = sort grep { !exists $owners{$_} } @files;
    if (@unowned) {
        print " -> Files not tracked by Shelly (rebuild their CPAN or locally installed modules):\n";
        print "    $_\n" for @unowned;
    }
}
PERL
