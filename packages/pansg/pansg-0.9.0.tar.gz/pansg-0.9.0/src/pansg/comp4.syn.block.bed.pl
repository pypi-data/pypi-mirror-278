###################################################################
# File Name: get.syn.pl
# Created Time: Tue 14 Nov 2023 09:45:54 AM CST
#=============================================================
#!/usr/bin/perl -w
use strict;
use warnings;

my $in=shift; #Ki3_Oh43.blastp.dag.nocontig.aligncoords
my $outdir=shift;
my $out=(split/\//,$in)[-1];
$out =~ s#\.dag\.aligncoords#\.syn\.block\.bed#;
my $paire =$out;
$paire =~ s#.syn.block.bed##;
#print "$paire\n";
my $que=(split/\_/,$paire)[0];
my $sub=(split/\_/,$paire)[1];

open IN,"$in";
open OUT,">$outdir/$out";
my @mar;
my $n=-1;
while(<IN>){
	chomp;
	$n++;
	my @sp=split/\t/;
	for my $i (0..$#sp){
		$mar[$n][$i]=$sp[$i];
	}
}close IN;
#print join("\t",@{$mar[1]})."\n";
#print $mar[1][1]."\n";
my ($firname,$secname);
#print $mar[1][0]."\n";
$firname=(split/\_/,$mar[1][0])[0];
$secname=(split/\_/,$mar[1][4])[0];

my $flag=0;
$flag=1 if($que eq $firname);
#print "$que\t$firname\n";

my @arr;
my $r=0;
my $i;
for $i (0..$n){
	my $up=$i-1;
	my $down=$i+1;
	if($mar[$i][0]=~/#/){
		if($i==0){
			if($flag){
			$arr[$r][0]=$mar[$down][0];
			$arr[$r][1]=$mar[$down][2];
			$arr[$r][3]=$mar[$down][4];
			$arr[$r][4]=$mar[$down][6];
			}else{
			$arr[$r][0]=$mar[$down][4];
			$arr[$r][1]=$mar[$down][6];
			$arr[$r][3]=$mar[$down][0];
			$arr[$r][4]=$mar[$down][2];
			}
	#		print join("\t",@{$arr[$r]})."\n";
		}else{
			if($flag){
			$arr[$r][2]=$mar[$up][3];
			$arr[$r][5]=$mar[$up][7];
			$r++;
			$arr[$r][0]=$mar[$down][0];
			$arr[$r][1]=$mar[$down][2];
			$arr[$r][3]=$mar[$down][4];
			$arr[$r][4]=$mar[$down][6];
			}else{
			$arr[$r][2]=$mar[$up][7];
			$arr[$r][5]=$mar[$up][3];
			$r++;
			$arr[$r][0]=$mar[$down][4];
			$arr[$r][1]=$mar[$down][6];
			$arr[$r][3]=$mar[$down][0];
			$arr[$r][4]=$mar[$down][2];
			}
		}
	}
	#print join("\t",@{$arr[$r]});
#	print "$i\n";
}
#print "@arr\n";
if($flag){
$arr[$r][2]=$mar[$n][3];
$arr[$r][5]=$mar[$n][7];
}else{
$arr[$r][2]=$mar[$n][7];
$arr[$r][5]=$mar[$n][3];
}
#print OUT "que\tqueS\tqueE\tsub\tsubS\tsubE\n";
for my $ii (0..$#arr){
	my @chr1=split/_/,$arr[$ii][0];
	my @chr2=split/_/,$arr[$ii][3];
	$chr1[1]=lc $chr1[1];
	$chr2[1]=lc $chr2[1];
	if($chr1[1] eq $chr2[1]){
#	print OUT "$chr1[1]\t$chr2[1]\n";
	#print OUT "$arr[$ii][0]\t$arr[$ii][3]\n";
		my $tmp1=$arr[$ii][2];
		my $tmp2=$arr[$ii][5];
		if($arr[$ii][1]>$tmp1){$arr[$ii][2]=$arr[$ii][1];$arr[$ii][1]=$tmp1;}
		if($arr[$ii][4]>$tmp2){$arr[$ii][5]=$arr[$ii][4];$arr[$ii][4]=$tmp2;}
	print OUT join("\t",@{$arr[$ii]})."\n";
	}
}

