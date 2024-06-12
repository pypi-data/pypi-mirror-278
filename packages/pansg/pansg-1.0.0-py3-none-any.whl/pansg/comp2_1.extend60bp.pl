###################################################################
# File Name: extend60bp.pl
# Created Time: 2023年12月21日 星期四 23时21分30秒
#=============================================================
#!/usr/bin/perl -w
use strict;
use warnings;
use File::Basename;

my $fai=shift;
#open IN,"/public/home/s20223010040/zzq/01.pangene/06.filter.miniprot/bin/refai.list";
open IN,"$fai";
my %refai;
while(<IN>){
	chomp;my @sp=split/\t/;
	$refai{$sp[0]}=$sp[1];
}close IN;


my $gff=shift;##B73rag_C002.gff
#exit if($gff=~/C7_2/);
my @suffixlist = qw(.gff3 .gff);
my $gffname=basename($gff,@suffixlist);
print "$gffname\n";
my $name=(split/\_/,$gffname)[-1];
$name=~s/\.gff//g;
print "$name\n";
my %fai;
open IN,$refai{$name};
while(<IN>){
	chomp;
	my @sp=split/\t/;
	$fai{$sp[0]}=$sp[1];
}close IN;

open IN,"$gff";
my @arr;
my $row=-1;
while(<IN>){
	chomp;
	next if(/^#/);
	my @sp=split/\t/,$_;
	next if($sp[2] eq "stop_codon");
	$row++;

	foreach my $col (0..$#sp){
		$arr[$row][$col]=$sp[$col];
	}

	if($row == 1){ #process first cds of first mRNA
		my $up=$row-1;
		if($arr[$up][2] eq "mRNA"){
			#$arr[$up][3]=$arr[$up][3]-60;
			#$arr[$up][4]=$arr[$up][4]+60;
			if($arr[$up][3]-60 >0){$arr[$up][3]=$arr[$up][3]-60;}
			if($fai{$arr[$up][0]}>=($arr[$up][4]+60)){$arr[$up][4]=$arr[$up][4]+60;}
			if($arr[$row][6] eq "+"){
				#$arr[$row][3]=$arr[$row][3]-60;
				if($arr[$row][3]-60 >0){$arr[$row][3]=$arr[$row][3]-60;}
			}else{
				#$arr[$row][4]=$arr[$row][4]+60;
				if($fai{$arr[$row][0]}>=($arr[$row][4]+60)){$arr[$row][4]=$arr[$row][4]+60;}
			}
		}
	}elsif($row>1){
		my $up=$row-1;
		my $lastcds=$row-2;
		if($arr[$up][2] eq "mRNA"){
			#$arr[$up][3]=$arr[$up][3]-60;
			if($arr[$up][3]-60 >0){$arr[$up][3]=$arr[$up][3]-60;}
			#$arr[$up][4]=$arr[$up][4]+60;
			if($fai{$arr[$up][0]}>=($arr[$up][4]+60)){$arr[$up][4]=$arr[$up][4]+60;}
			#process first cds of others mRNA && extend start_codon
			if($arr[$row][6] eq "+"){
				#$arr[$row][3]=$arr[$row][3]-60;
				if($arr[$row][3]-60>0){$arr[$row][3]=$arr[$row][3]-60;}
			}else{
				#$arr[$row][4]=$arr[$row][4]+60;
				if($fai{$arr[$row][0]}>=($arr[$row][4]+60)){$arr[$row][4]=$arr[$row][4]+60;}
			}

			#process last cds of others mRNA && extend stop_codon
			if($arr[$lastcds][6] eq "+"){
				#$arr[$lastcds][4]=$arr[$lastcds][4]+60;
				if($fai{$arr[$lastcds][0]}>=($arr[$lastcds][4]+60)){$arr[$lastcds][4]=$arr[$lastcds][4]+60;}
			}else{
				#$arr[$lastcds][3]=$arr[$lastcds][3]-60;
				if($arr[$lastcds][3]-60>0){$arr[$lastcds][3]=$arr[$lastcds][3]-60;}
			}
		}
	}
}close IN;

##process last cds of last mRNA
if($arr[$row][6] eq "+"){
	#$arr[$row][4]=$arr[$row][4]+60;
	if($fai{$arr[$row][0]}>=($arr[$row][4]+60)){$arr[$row][4]=$arr[$row][4]+60;}
}else{
	#$arr[$row][3]=$arr[$row][3]-60;
	if($arr[$row][3]-60 >0){$arr[$row][3]=$arr[$row][3]-60;}
}


#print $arr[5][8]."\n";
my $out=shift;#B73rag_C002.extend60bp.gff
open OUT,">$out";
print OUT "##gff-version 3\n";
for my $r (0..$row){
	my @rr=@{$arr[$r]};
	print OUT join("\t",@rr)."\n";
}
close OUT;
