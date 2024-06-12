###################################################################
# File Name: format.pl
# Created Time: 2024年01月18日 星期四 09时13分30秒
#=============================================================
#!/usr/bin/perl -w
use strict;
use warnings;

my $config=shift;
my $renamedir=shift;
open IN,"$config";
my %cdslen;
while(my $row=<IN>){
        chomp $row;
		my @sp=split/\t/,$row;
		my $name=$sp[0];
		my $gff="$renamedir/$name.gene.bed";
		open GFF,"$gff";
		while(<GFF>){
			chomp;my @spp=split/\t/;
			$cdslen{$spp[3]}=$spp[2]-$spp[1];
		}close GFF;
}close IN;
close OUT;

my $in=shift;#SG_144.pan
my $nu=shift; #144
my $out=shift;
my $end=$nu+2;

open IN,"$in";
#my $out=$in;
#$out=~s/\.pan/\_format\.pan/g;
open OUT,">$out";
my $n=0;
while(my $row=<IN>){
	$n++;
	chomp $row;
	my @sp=split/\t/,$row;
	if($sp[1] eq "sample_number"){
		print OUT "SG_id\trepresent_gene\ttrepresent_gene.length\tsample_number\t".join("\t",@sp[3..$#sp])."\n";
		next;
	}
	my $id;my $max=0;my $nu=0;
	for my $i (3..$end){
	if($sp[$i]){
		if($sp[$i]=~/,/){
			$nu++;
			my @spp=split/,/,$sp[$i];
			foreach my $pp (@spp){
				my $len=$cdslen{$pp};
				if($len>$max){$max=$len;$id=$pp;}
			}
		}else{
			my $pp=$sp[$i];
			if(exists $cdslen{$pp}){
				$nu++;
				my $len=$cdslen{$pp};
				if($len>$max){$max=$len;$id=$sp[$i];}
			}else{
			if($sp[$i]){print "$sp[$i]\tERROR";}
			}
		}
	}
	else{$sp[$i]="None";}
	}
	my @pre=("sg".$n,$id,$max,$nu);
	print OUT join("\t",@pre)."\t".join("\t",@sp[3..$#sp])."\n";
}close IN;
close OUT;
