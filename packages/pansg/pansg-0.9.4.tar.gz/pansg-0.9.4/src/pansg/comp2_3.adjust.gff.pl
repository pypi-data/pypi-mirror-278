###################################################################
# File Name: extend60bp.pl
# Created Time: 2023年12月21日 星期四 23时21分30秒
#=============================================================
#!/usr/bin/perl -w
use strict;
use warnings;

my $gff=shift;##B73rag_C002.gff
my $holdgenepos=shift;#holdgene.pos.txt
open IN,"$holdgenepos";
my %hold;
while(<IN>){
chomp;
my @sp=split/\t/;
my @v=@sp[1,2];
$hold{$sp[0]}=\@v;
}
close IN;

my $fai=shift;
my %fai;
open IN,"$fai";
while(<IN>){
	chomp;
	my @sp=split/\t/;
	$fai{$sp[0]}=$sp[1];
}close IN;

my @arr;my @arrid;
sub getpos{
	my ($rr)=@_;
	my $idd=$arrid[$rr];
	my @shiftpos=@{$hold{$idd}};
	$shiftpos[0]=60-$shiftpos[0];
	return ($shiftpos[0],$shiftpos[1]);
}

open IN,"$gff";
my %stop;
while(<IN>){
	chomp;
	next if(/^#/);
	my @sp=split/\t/,$_;
	my $id;
	if($sp[8]=~/(\S+)=(\S+);Rank/){$id=$2;}
	if($sp[2] eq "stop_codon"){$stop{$id}="1";next;}
	else{next;}
}close IN;


open IN,"$gff";
my $row=-1;
my ($shst,$shed);
while(<IN>){
	chomp;
	next if(/^#/);
	my @sp=split/\t/,$_;
	my $id;
	if($sp[8]=~/(\S+)=(\S+);Rank/){$id=$2;}
	if($sp[2] eq "stop_codon"){next;}
	next unless(exists $hold{$id});
	$row++;
	$arrid[$row]=$id;

	foreach my $col (0..$#sp){
		$arr[$row][$col]=$sp[$col];
	}

	if($row == 1){ #process first cds of first mRNA
		my $up=$row-1;
		my ($upstr,$upend)=getpos($up);
		my ($str,$end)=getpos($row);
		
		if($arr[$up][2] eq "mRNA"){
			if($stop{$arrid[$up]}){
				$upend=$upend-3;
			}
			if($arr[$row][6] eq "+"){
				$arr[$up][3]=$arr[$up][3]-$upstr;
				$arr[$up][4]=$arr[$up][4]+$upend;
				$arr[$row][3]=$arr[$row][3]-$str;
			}else{
				$arr[$up][4]=$arr[$up][4]+$upstr;
				$arr[$up][3]=$arr[$up][3]-$upend;
				$arr[$row][4]=$arr[$row][4]+$str;
			}
		}
	}elsif($row>1){
		my $up=$row-1;
		my $lastcds=$row-2;

		my ($upstr,$upend)=getpos($up);
		my ($str,$end)=getpos($row);
		my ($lastr,$laend)=getpos($lastcds);

		if($arr[$up][2] eq "mRNA"){
			if($stop{$arrid[$up]}){$upend=$upend-3;}
			#process first cds of others mRNA && extend start_codon
			if($arr[$row][6] eq "+"){
				$arr[$up][3]=$arr[$up][3]-$upstr;
				$arr[$up][4]=$arr[$up][4]+$upend;
				$arr[$row][3]=$arr[$row][3]-$str;
			}else{
				$arr[$up][4]=$arr[$up][4]+$upstr;
				$arr[$up][3]=$arr[$up][3]-$upend;
				$arr[$row][4]=$arr[$row][4]+$str;
			}

			#process last cds of others mRNA && extend stop_codon
			if($arr[$lastcds][6] eq "+"){
				$arr[$lastcds][4]=$arr[$lastcds][4]+$laend;#end
			}else{
				$arr[$lastcds][3]=$arr[$lastcds][3]-$laend;#start
			}
		}
	}
}close IN;

my ($str,$end)=getpos($row);
##process last cds of last mRNA
if($arr[$row][6] eq "+"){
	$arr[$row][4]=$arr[$row][4]+$end;
}else{
	$arr[$row][3]=$arr[$row][3]-$end;
}


#print $arr[5][8]."\n";
#my $out=shift;#B73rag_C002.adjust.gff
#open OUT,">$out";
my %del;
#print OUT "##gff-version 3\n";
print "##gff-version 3\n";
for my $r (0..$row){
	my @rr=@{$arr[$r]};
	my $id;
	if($rr[8]=~/(\S+)=(\S+);Rank/){$id=$2;}
	if($rr[3]<0 || $rr[4]>$fai{$rr[0]}){$del{$id}="1";}
	next if(exists $del{$id});
	#print OUT join("\t",@rr)."\n";
	print join("\t",@rr)."\n";
}
#close OUT;
