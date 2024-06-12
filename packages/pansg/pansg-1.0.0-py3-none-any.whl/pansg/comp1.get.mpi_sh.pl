###################################################################
# File Name: get.sh.pl
# Created Time: 2024年01月02日 星期二 22时56分02秒
#=============================================================
#!/usr/bin/perl -w
use strict;
use warnings;

my $pep=shift;
my $genome=shift;
my $outdir=shift;
my $outcommend=shift;

open IN,"$pep";
open OUT,">$outcommend";
my $dir="$outdir";
while(<IN>){
chomp;
my @sp=split/\t/;

open REF,"$genome";
while(<REF>){
chomp;
my @spp=split/\t/;
next if ($sp[1] eq $spp[1]);
my $name=$sp[1]."_".$spp[1];
print OUT "miniprot --outn=1 -Iut8 --gff $spp[0] $sp[0] >$dir/".$name.".gff && echo $name miniprotone\n";
}
close REF;

}close IN;
close OUT;
