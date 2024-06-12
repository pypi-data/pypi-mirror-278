###################################################################
# File Name: cmp1_1.get.miniprot.index.pl
# Created Time: 2024年06月04日 星期二 17时00分45秒
#=============================================================
#!/usr/bin/perl -w
use strict;
use warnings;
my $file=shift;##config
my $outdir=shift;
my $out=shift;
open IN,"$file";
open OUT,">$out";
while(<IN>){
	chomp;
	my @sp=split/\t/;
	print OUT "miniprot -t 32 -d $outdir/$sp[0].fa.mpi $sp[1]\n";
}close IN;
close OUT;

