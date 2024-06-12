###################################################################
# File Name: get.shell.pl
# Created Time: 2024年01月16日 星期二 11时14分16秒
#=============================================================
#!/usr/bin/perl -w
use strict;
use warnings;

my $dir=shift;#"/public/home/s20223010040/zzq/01.pangene/06.filter.miniprot/work";
my $bin=shift;#"/public/home/s20223010040/zzq/01.pangene/06.filter.miniprot/bin";
my $config=shift;#config file
my $evebin=shift;#every paire sample script
my $miniprotlist=shift;##miniprot gff list

#open IN,"ref.list";
open IN,"$config";
my %ref;
my %refai;
open FAI,">$dir/all.genome.fai.list";
while(<IN>){
	chomp;my @sp=split/\t/;
	$ref{$sp[0]}=$sp[1];
	my $fai_file=$sp[1].".fai";
	if (!-e $fai_file) {
		print "FAI file $fai_file does not exist. Creating it using samtools faidx...\n";
		my $command = "samtools faidx $sp[1]";
		system($command);
		#system(samtools faidx $sp[1]);
		if ($? != 0) {die "Error running samtools faidx: $!\n";}#Check whether the command is executed successfully
	}else{
		print "FAI file $fai_file already exists.\n";  
	}
	$refai{$sp[0]}=$fai_file;
	print FAI "$sp[0]\t$fai_file\n";
	my $second=$sp[0];
	system(`mkdir -p $dir/$second/tmp`);
	open IN2,"$config";
	while(<IN2>){
		chomp;
		my @spp=split/\t/;
		my $first=$spp[0];
		next if($first eq $second);
		my $name=$first."_".$second;
		open OUT,">$evebin/filt.$name.sh";
		my $file=`grep "$name" $miniprotlist`;
		chomp $file;
		#print OUT "mkdir $dir/$second && cd $dir/$second && mkdir tmp\n";
		#print OUT "cd $dir/$second && mkdir tmp\n";
		print OUT "cd $dir/$second\n";
		print OUT "grep Frameshift $file".'|awk \'$3=="mRNA"\'|cut -f 9|cut -d ";" -f 1|cut -d "="'." -f 2 >tmp/$name.Frameshift.id\n";
		print OUT "perl $bin/comp2_1.extend60bp.pl $dir/all.genome.fai.list $file tmp/$name.extend60bp.gff\n";
		print OUT "gffread tmp/$name.extend60bp.gff -g $ref{$second} -w tmp/$name.extend60bp.cds.fa\n";
		print OUT "perl $bin/comp2_2.filt.codon_60bp.pl tmp/$name.extend60bp.cds.fa tmp/$name.Frameshift.id >tmp/$name.holdgene.pos.txt\n";
		print OUT "perl $bin/comp2_3.adjust.gff.pl $file tmp/$name.holdgene.pos.txt $refai{$second} >$name.adjust.gff\n";
	}
	close IN2;
	close OUT;
}close IN;
close FAI;
