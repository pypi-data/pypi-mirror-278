#!/usr/bin/perl
use strict;
use warnings;

my $name=shift;
my $workdir=shift;
my $rename=shift;
my $outdir=shift;

my $tandem="$workdir/$name/result/$name.tandem.pairs";
open IN,"$tandem";
my %graph;
while (<IN>) {
    chomp;
	next if(/^Dup/);
    my @nodes = split /\s+/;
	my @no1=split/\.|\_/,$nodes[0];
	my $n1="$name\_$no1[0]";
	my @no2=split/\.|\_/,$nodes[2];
	my $n2="$name\_$no2[0]";
	$graph{$n1}{$n2}=1;
	$graph{$n2}{$n1}=1;
}

my %visited;
my @clusters;

sub dfs {
    my ($node, $cluster) = @_;
    $visited{$node} = 1;
    push @$cluster, $node;

    for my $neighbor (sort {$graph{$a} <=> $graph{$b}} keys %{ $graph{$node} }) {
        dfs($neighbor, $cluster) unless $visited{$neighbor};
    }
}

for my $node (sort {$graph{$a} <=> $graph{$b}} keys %graph ) {
    next if $visited{$node};

    my @cluster;
    dfs($node, \@cluster);

    push @clusters, \@cluster;
}

my $gff="$rename/$name.gene.bed";
open FAI,"$gff";
my %len;
while(<FAI>){
	chomp;
	my @sp=split/\t/;
	$len{$sp[3]}=$sp[2]-$sp[1];
}close FAI;


my $max=0;
my $maxid;
open OUT,"|sort -k1,1V >$outdir/$name.tandem.duplicat.cluster";
foreach my $cluster (@clusters) {
	my @sorted_array = sort { lc($a) cmp lc($b) } @$cluster;
	foreach my $yy (@sorted_array){
		if($len{$yy} > $max){
			$max=$len{$yy};
			$maxid=$yy;
			#$maxid=$sp[0];
		}
	}
    print OUT "$maxid\t".join(",", @sorted_array), "\n";
	$max=0;
}
close OUT;

