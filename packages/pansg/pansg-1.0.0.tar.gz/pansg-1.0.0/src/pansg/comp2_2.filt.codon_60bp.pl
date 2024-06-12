#!/bin/perl -w
use strict;
use warnings;

my $f=shift;##mik.transcripts.fa
my $s="ATG";
my $e1="TAA";
my $e2="TAG";
my $e3="TGA";
my %seq;
open IN,"$f";
my $name;
while(<IN>){
	chomp;
	if(/^>(\S+)/){
		$name=$1;
		$seq{$name}="";
	}else{
		$seq{$name}.=$_;
	}
}
close IN;

my $framshift=shift;##Frameshift.id.ingff
open IN,"$framshift";
my %frams;
while(<IN>){
	chomp;
	$frams{$_}=1;
}close IN;

#open OUT1,">holdgene.txt";
#open OUT2,">holdgene.pos.txt";

foreach my $key (keys %seq){
	my $allseq=$seq{$key};
	$allseq = uc($allseq);
	next if(length($allseq)<=150);
	my $ss=substr($allseq,0,63);
	my $ee=substr($allseq,-63);
	#print "$key\t$ss\t$ee\n";
	my $sflag=0;my $eflag=0;
#	for (my $i=0;$i < length($ss)-2; $i+=3){
#		my $st=substr($ss,$i,3);
#		if($st eq $s){$sflag=1;}
#	}
	my $stri=0;my $endi=0;
	for(my $i=60;$i>=0;$i-=3){
		my $st=substr($ss,$i,3);
		if($st eq $s){
			$sflag=1;
			$stri=$i;
		}
	}

	for (my $ii=0;$ii<length($ee)-2; $ii+=3){
		my $en=substr($ee,$ii,3);
		if(($en eq $e1)||($en eq $e2)||($en eq $e3)){
			$eflag=1;
			$endi=$ii;
		}
	}

	if($sflag==1 && $eflag==1){
		next if(exists $frams{$key});
#		print OUT1 "$key\n";
		#print OUT2 "$key\t$stri\t$endi\n";
		print "$key\t$stri\t$endi\n";
	}
}
#close OUT1;
#close OUT2;
