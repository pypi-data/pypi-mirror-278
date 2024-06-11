###################################################################
# File Name: complement.pl
# Created Time: 2024年01月02日 星期二 16时25分28秒
# v3 add represent gene hold -hom.shift,old is gene.shift
#=============================================================
#!/usr/bin/perl -w
use strict;
use warnings;
use File::Basename;

my $intminidir=shift;
my @minilist=`ls $intminidir/*gz`;
my %int;
foreach my $mini (@minilist){
	chomp $mini;
	my $sample=basename($mini,".overlap.miniprot_gene.bed.gz");
	#print "$sample\t$mini\n";
	$int{$sample}=$mini;
}


#open IN,"DAGchainer.5gene.block.bed.file.list";
my $dagblockdir=shift;
my @dagblock=`ls $dagblockdir/*bed`;
my %syn;
foreach my $file (@dagblock){
#while(<IN>){
    chomp $file;
	my $name=basename($file,".syn.block.bed");
#    my ($name,$file)=split/\t/;
    open SYN,$file;
    while(my $row=<SYN>){
        chomp $row;
        my ($block1, $start1, $end1, $block2, $start2, $end2) = split/\t/,$row;  
        # push @{$syn{$name}{$block1}}, [$block1,$start1, $end1, $block2, $start2, $end2]; 
        push @{$syn{$name}{$block1}},$row;
		#print "$name\n";
    }close SYN;
}close IN;

#open IN,"../../gene.bed.list";
my $renamedir=shift;
my @genebedlist=`ls $renamedir/*bed`;
my %genebed;
my %allgenepos;
my %pep;
#while(my $row=<IN>){
	#next unless($_=~/^chr/);##only panning for chr genes
	#chomp $row;	my @sp=split/\t/,$row;
    #$genebed{$sp[0]}=$sp[1];
    #open POS,"$sp[1]";
foreach my $genefile (@genebedlist){
	chomp $genefile;
	#print $genefile;
	my $name=basename($genefile,".gene.bed");
	$genebed{$name}=$genefile;
    open POS,"$genefile";
    while(<POS>){
        chomp;
        my ($c,$s,$e,$g)=split/\t/;
		$c=$name."_".$c;
        push @{$allgenepos{$g}},($c,$s,$e);
		$pep{$g}=$e-$s+1;
    }close POS;
}close IN;

#my $peplen=shift;
#open IN,"../../pep.len.list";
#open IN,"$peplen";
#my %peplenfile;
#while(my $row=<IN>){
#	chomp $row;	my @sp=split/\t/,$row;$peplenfile{$sp[1]}=$sp[0];
#}close IN;

my $dupdir=shift;
my %dupfile;
my @duplist=`ls $dupdir/*cluster`;
#open IN,"../../dupgene.list";
#while(my $row=<IN>){
foreach my $dup (@duplist){
	chomp $dup;
	my $name=basename($dup,".tandem.duplicat.cluster");
	$dupfile{$name}=$dup;
	#print "$name\t$dup\n";
}close IN;


my $in=shift;#test.SG.133_3sample
open IN,"$in";
my @arr;
my @arrrow;
my @arrrowev;
my $row=-1;
my %holdgene;
my $head=<IN>;
while(<IN>){
        chomp;
        $row++;
        my @sp=split/\t/;
        for(my $c=0;$c<=3;$c++){
            $arr[$c][$row]=$sp[$c];
            $arrrow[$row][$c]=$sp[$c];
        }
        $arrrow[$row][3]=0;
        for(my $c=4;$c<=$#sp;$c++){
#			my $ct=$c-1;
            $arr[$c][$row]=$sp[$c];
            $arrrow[$row][$c]=$sp[$c];
			if($sp[$c]=~/\,/){
				my @tmp=split/\,/,$sp[$c];
				push @{$arrrowev[$row]},@tmp;
				foreach my $tmphold (@tmp){
					$holdgene{$tmphold}="1";
				}
			}else{
				push @{$arrrowev[$row]},$sp[$c];
					$holdgene{$sp[$c]}="1";
			}
        }
}close IN;

my $flag=$row;
my $sg=$row+1;
#my %pep;
my %minlen;
# my %holdpos;

###
chomp $head;
my @sp=split/\t/,$head;
for (my $cc=4;$cc<=$#sp;$cc++){
	#my $name=(split/hhh/,$sp[$cc])[0];
	my $name=$sp[$cc];
	##hold tandem duplication genes
	my $dupf=$dupfile{$name};
#	print "$dupf\n";
	open DUP,"$dupf";
	my %dup;my %duprep;
	while(<DUP>){
		chomp;
		my @sp=split/\t/,$_;
		my @tmp=split/\,/,$sp[1];
		foreach my $d (@tmp){
			$dup{$d}=\@tmp;
			$duprep{$d}=$sp[0];
		}
	}close DUP;

	my $intfile=$int{$name};
	###Relationship between target gene and subject genome location and gene
	open INTT,"gunzip -dc $intfile|";
	my %gene;
	while(<INTT>){
		chomp;my @spp=split/\t/;
		#my $sppname=(split/hhh/,$spp[4])[0];
		#next if($name eq $sppname);
		$minlen{$spp[3]}=$spp[6];
		if(exists $gene{$spp[4]}){
			my @tmpmi=@{$gene{$spp[4]}};
			if($#tmpmi>10){
				my @tmpsub=($tmpmi[-2],$spp[-2]);
				$gene{$spp[4]}=\@tmpsub;
			}else{
				push @{$gene{$spp[4]}},$spp[-2];
			}
		}else{
			$gene{$spp[4]}=\@spp;
		}
	}close INTT;

	###get the every row infomation of one sample/column
	my @col=@{$arr[$cc]};
	#my %holdgene;
	for my $rr (0..$#col){
		if($col[$rr] ne "None"){
			# $col[$rr]=~s/-hom//g;
			$col[$rr]=~s/-syn//g;
			if($col[$rr]=~/\,/){
				my @tmpsp=split/\,/,$col[$rr];
				foreach my $evid (@tmpsp){
					# if($evid=~/evm/){$holdgene{$evid}="1"}
					$holdgene{$evid}="1";
				}
			}else{
				# if($col[$rr]=~/evm/){$holdgene{$col[$rr]}="1";}
				$holdgene{$col[$rr]}="1";
			}
			next;
		}
		##complement homology gene by others genes in other all samples 
		my @none;
		for my $eve (0..$#{$arrrowev[$rr]}){ ##bian li does every sample have hom gene in subject genome
			my $tmpgene=$arrrowev[$rr][$eve];
			# my $tmpgene=$arrrow[$rr][1];
			# next if($tmpgene=~/hom/);
			$tmpgene=~s/-syn//g;
			if(exists $gene{$tmpgene}){
				my @minp=@{$gene{$tmpgene}};
				if($minp[0]=~/_/){##one target gene map to >1 evm gene
					foreach my $ggg (@minp){
						next if(exists $holdgene{$ggg});
						if(exists $dup{$ggg}){
							my @spdup=@{$dup{$ggg}};
							foreach my $dgene (@spdup){
								#$holdgene{$dgene}="1";
								#$dgene.="-hom";
								# push @none,$dgene;
								my $endgene=syngene($tmpgene,$dgene);
								#print "dgene1\t$dgene\n";
								if($endgene ne "None"){
									my $tmp=$endgene; $tmp=~s/-syn//g;
									$holdgene{$tmp}="1";
									push @none,$endgene;
								}
							}
						}else{
							#$holdgene{$ggg}="1";
							# $ggg.="-hom";
							# push @none,$ggg;
							my $endgene=syngene($tmpgene,$ggg);
							#print "ggg1\t$ggg\n";
							if($endgene ne "None"){
								my $tmp=$endgene; $tmp=~s/-syn//g;
								$holdgene{$tmp}="1";
								push @none,$endgene;
							}
						}
					}
				}else{#one target gene map to <=1 evm gene
					#if($minp[-2]=~/hhh/){
					if($minp[-2]=~/\_/){
						my $ggg=$minp[-2];
						next if(exists $holdgene{$ggg});
						if(exists $dup{$ggg}){
							my @spdup=@{$dup{$ggg}};
							foreach my $dgene (@spdup){
								#$holdgene{$dgene}="1";
								# $dgene.="-hom";
								# push @none,$dgene;
								my $endgene=syngene($tmpgene,$dgene);
								#print "dgene2\t$dgene\n";
								if($endgene ne "None"){
									my $tmp=$endgene; $tmp=~s/-syn//g;
									$holdgene{$tmp}="1";
									push @none,$endgene;
								}
							}
						}else{
							#$holdgene{$ggg}="1";
							# $ggg.="-hom";
							# push @none,$ggg;
							my $endgene=syngene($tmpgene,$ggg);
							#print "ggg2\t$ggg";
							if($endgene ne "None"){
								my $tmp=$endgene; $tmp=~s/-syn//g;
								$holdgene{$tmp}="1";
								push @none,$endgene;
							}
						}
					}else{
						next if(exists $holdgene{$minp[3]});
						#$holdpos{$minp[3]}="1";
						# $minp[3]=$minp[3]."-hom";
						# push @none,$minp[3];
						my $endgene=syngene($tmpgene,$minp[3]);
						#print "minp\t$minp[3]\n";
						if($endgene ne "None"){
							my $tmp=$endgene; $tmp=~s/-syn//g;
							$holdgene{$tmp}="1";
							push @none,$endgene;
						}
					}
				}
			}
		}
		
		my $noneid=join(",",@none);
		if($noneid){$arrrow[$rr][$cc]=$noneid;}
		#else{$arrrow[$rr][$cc]="None";}##None cell have not hom gene in other samples;
	}

}

my $outdir=shift;
$pep{"None"}=0;
my $out1="$outdir/01.Pansg.complement_dup.txt";
open OUT,">$out1";
print OUT "$head\n";
#whether synteny genes are preferred as representative genes
foreach my $rr (0..$row){
		my $id;my $max=0;my %nameha;
		for my $ll (4..$#{$arrrow[$rr]}){
			my $idd=$arrrow[$rr][$ll];
			if($idd!~/None/){ ##stat sample number for one synteny gene
				my $namee=(split/\_/,$idd)[0];
				$nameha{$namee}=1;##state hom gene sample;
			}
		}
		my $number=0;
		foreach my $namek (keys %nameha){$number+=$nameha{$namek};}
		$arrrow[$rr][3]=$number;
		print OUT join("\t",@{$arrrow[$rr]})."\n";
#	}
}close OUT;

my $out2="$outdir/02.Pansg.complement.represent.txt";
open OUTREPS,">$out2";
print OUTREPS "$head\n";
#whether synteny genes are preferred as representative genes
foreach my $rr (0..$row){
		my @newarr;
		@{$newarr[$rr]}=@{$arrrow[$rr]}[0..3];
		$newarr[$rr][0]=~s/\#//;
		for my $ll (4..$#{$arrrow[$rr]}){
			my $idd=$arrrow[$rr][$ll];
			if($idd=~/\,/){
				my @spid=split/\,/,$idd;
				##get every cell longest pep;
				my $maxcelllen=0;my $maxcellid;
				my (@comevm,@comevmsyn,@comevmhom,@comminisyn,@comminihom);
				foreach my $ele (@spid){
					if($ele=~/_/ && $ele!~/hom/ && $ele!~/syn/){push @comevm,$ele;}
					elsif($ele=~/_/ && $ele =~/syn/){$ele=~s/-syn//g;push @comevmsyn,$ele;}
					elsif($ele=~/_/ && $ele =~/hom/){$ele=~s/-hom//g;push @comevmhom,$ele;}
					elsif($ele!~/_/ && $ele=~/syn/){$ele=~s/-syn//g;push @comminisyn,$ele;}
					elsif($ele!~/_/ && $ele =~/hom/){$ele=~s/-hom//g;push @comminihom,$ele;}
					else{print "$idd\terror.for.hold.other.element\n";}
				}

				if(@comevm){
					($maxcellid,$maxcelllen)=extract_max_element(\@comevm,\%pep);
				}elsif(@comevmsyn){
					($maxcellid,$maxcelllen)=extract_max_element(\@comevmsyn,\%pep);$maxcellid.="-syn";
				}elsif(@comevmhom){
					($maxcellid,$maxcelllen)=extract_max_element(\@comevmhom,\%pep);$maxcellid.="-hom";
				}elsif(@comminisyn){
					($maxcellid,$maxcelllen)=extract_max_element(\@comminisyn,\%minlen);$maxcellid.="-syn";
				}elsif(@comminihom){
					($maxcellid,$maxcelllen)=extract_max_element(\@comminihom,\%minlen);$maxcellid.="-hom";
				}else{print "$idd\terror\n";}

				push @{$newarr[$rr]},$maxcellid;
			}else{
				push @{$newarr[$rr]},$idd;
			}
		}
		print OUTREPS join("\t",@{$newarr[$rr]})."\n";
}
close OUTREPS;

sub extract_max_element {  
    my ($arr, $len_hash) = @_;  
    my $max_value;  
    my $max_element;  

    foreach my $element (@$arr) {  
        my $value = $len_hash->{$element} // 0; # 默认值为0，以防元素不在哈希中  
        if (!defined $max_value || $value > $max_value) {  
            $max_value = $value;  
            $max_element = $element;  
        }  
    }  
    return ($max_element,$max_value);  
}

sub syngene {
	my ($que,$sub)=@_;
	#$que=~s/-hom//;	
	$que=~s/-syn//;
	#$sub=~s/-hom//;	
	$sub=~s/-syn//;

	my @qpos=@{$allgenepos{$que}};
	#my $qname=(split/hhh/,$que)[0];
	my $qname=(split/_/,$que)[0];
	#if($sub=~/evm/){
	#print "$que\t";
	if($sub=~/\_/){
	#	print "$sub\n";
		my @spos=@{$allgenepos{$sub}};
		#my $sname=(split/hhh/,$sub)[0];
		my $sname=(split/_/,$sub)[0];
		my $schr=$sname."_".$spos[0];

		my $paire=$qname."_".$sname;
		# print "$paire\tevm\n";
		my @synpos=@{$syn{$paire}{$qpos[0]}};
		my $flag=0;
		foreach my $sypos (@synpos){
			my @spsyn=split/\t/,$sypos;
			if($qpos[1]>$spsyn[1] && $qpos[1]<$spsyn[2] && $schr eq $spsyn[3] && $spos[1]>$spsyn[4] && $spos[1]<$spsyn[5]){
				#print "$que".join("\t",@qpos)."|".$sub.join("\t",@spos)."\n";
				#print join("\t",@spsyn)."\n";
				$flag++;
				next;
			}
		}
		if($flag){return $sub."-syn";}
		else{return "None";}
#		else{return $sub."-hom";}
	}else{
		# my @spos=@{$allgenepos{$sub}};
		#my ($sname,$c,$s,$e)=(split/_/,$sub);
		my ($sname,$c,$s,$e)=(split/\-|\:|\.\./,$sub);
		my @spos=($c,$s,$e);
		my $schr=$sname."_".$c;

		my $paire=$qname."_".$sname;
		#print "$paire\tminiprot\t$que\n";
		my @synpos=@{$syn{$paire}{$qpos[0]}};
		my $flag=0;
		foreach my $sypos (@synpos){
			my @spsyn=split/\t/,$sypos;
			if($qpos[1]>$spsyn[1] && $qpos[1]<$spsyn[2] && $schr eq $spsyn[3] && $spos[1]>$spsyn[4] && $spos[1]<$spsyn[5]){
				#print "$que".join("\t",@qpos)."|".$sub.join("\t",@spos)."\n";
				#print join("\t",@spsyn)."\n";
				$flag++;
				next;
			}
		}
		if($flag){return $sub."-syn";}
		else{return "None";}
		# else{return $sub."-hom";}
	}
}

