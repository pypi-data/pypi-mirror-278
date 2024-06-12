###################################################################
# File Name: comp0.rename.pl
# Created Time: 2024年06月07日 星期五 04时04分01秒
#=============================================================
#!/usr/bin/perl -w
use strict;
use warnings;

my $config=shift;
my $pwd=shift;
my $out=shift;

open IN,"$config";
while(<IN>){
	chomp;
	my @sp=split/\t/;
	my $name=$sp[0];
	my $genome=$sp[1];
	my $gff="$pwd/$name/$name.gff";
	my @spp=split/\//,$genome;
	$spp[-1]="$name.pro_fasta";
	my $pep=join("/",@spp);
#	print "$name\t$gff\t$pep\n";
	
	##rename pep
	open PEP,"$pep";
	open PEPOUT,">$out/$name.pep.fa";
	my %holdpep;
	while(<PEP>){
		chomp;
		if(/^>(\S+)/){
			my $pepid=$1;
			$holdpep{$pepid}="1";
			my $pepidd=(split/>|\.|\_/,$pepid)[0];
			print PEPOUT ">$name\_$pepidd\n";
		}else{
			print PEPOUT "$_\n";
		}
	}close PEPOUT;
	
	##rename gene bed
	open GFF,"$gff";
	open OUT,">$out/$name.gene.bed";
	while(<GFF>){
		chomp;
		my @gf=split/\t/;
		my @gfp=split/\.|\_/,$gf[1];
		if(exists $holdpep{$gf[1]}){
			print OUT "$gf[0]\t$gf[2]\t$gf[3]\t$name\_$gfp[0]\n";
		}
	}close OUT;

}close IN;

