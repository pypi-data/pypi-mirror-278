###################################################################
# File Name: getsh.pl
# Created Time: 2024年01月03日 星期三 11时57分29秒
# filter by identity >0.9
#=============================================================
#!/usr/bin/perl -w
use strict;
use warnings;

my $config=shift;
my $rename=shift;
my $intresult=shift;
my $mini=shift;
my $bin=shift;
open IN,"$config";
while(<IN>){
	chomp;
	my @sp=split/\t/;
	my $sample=$sp[0];
	my $genebed="$rename/$sample.gene.bed";
	print "perl $bin/comp3_1.overlap.gene_miniprot.pl $sample $mini\|bedtools intersect -wao -a - -b $genebed\|gzip - >$intresult/$sample.overlap.miniprot_gene.bed.gz \&\& echo $sample.overlap.miniprot_gene.bed Done\n";
}close IN;
