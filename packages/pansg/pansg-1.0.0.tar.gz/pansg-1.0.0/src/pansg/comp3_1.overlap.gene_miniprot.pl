###################################################################
# File Name: getsh.pl
# Created Time: 2024年01月03日 星期三 11时57分29秒
# filter by identity >0.9
#=============================================================
#!/usr/bin/perl -w
use strict;
use warnings;

my $name=shift;
my $miniprot=shift;
my @file=`grep "_$name" $miniprot`;
#	my @file=`grep "_$name" test`;
	foreach my $mini (@file){
	chomp $mini;
	#print "$name\t$mini\n";
	open GFF,"$mini";
	my %ha;my %fail;
	my ($id,$identity,$target);
	while(<GFF>){
		chomp;
		next if(/^#/);
		my @sp=split/\t/;
		next if($sp[0]=~/_/);
		if($sp[2]=~/mRNA/){
			($id, $identity, $target) = $sp[8] =~ /ID=(\S+);\S+;Identity=(.*?);\S+;Target=(\S+)/;
			#print "$id\t$identity\t$target\n";
			if($identity<0.9){$fail{$id}="1";}
			#my $subid=$name."hhh".$sp[0]."_".$sp[3]."_".$sp[4];
			my $subid=$name."-".$sp[0].":".$sp[3]."..".$sp[4];
			my @tmp=($sp[0],$sp[3],$sp[4],$subid,$target,$sp[8],0);
			$ha{$target}=\@tmp;
		}elsif($sp[2]=~/CDS/){
			my $len=($sp[4]-$sp[3]+1)/3-1;##delet stop cond len of 1
			${$ha{$target}}[6]+=$len;
		}
	}
	close GFF;
	foreach my $ky (keys %ha){
		my @val=@{$ha{$ky}};
		my $id=(split/=|;/,$val[5])[1];
		next if(exists $fail{$id});
		print join("\t",@{$ha{$ky}})."\n";
	}
}
#close OUT;
