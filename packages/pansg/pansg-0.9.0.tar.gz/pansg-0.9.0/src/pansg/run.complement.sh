#!/bin/sh
#SBATCH -p Cnode3
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --time=24:00:00
##usage bash run.complement.sh pansg.config 
##pansg.config:
##sample1	/data/sample1.genome.fa	/data/sample1.gff3
##sample2	/data/sample2.genome.fa	/data/sample2.gff3
config=$1
tmppansg=$2
bin=$(pip show pansg|grep Location|awk '{print $NF"/pansg"}')
#bin="/public/home/s20223010040/zzq/01.pangene/00.pipline/02.test_cao/bin"
pwd=(`pwd`)
outpre="complement.pansg"
out=$pwd/$outpre
mkdir -p $out  && echo build $out success|| echo build $out error

#00.rename gene id
rename="$out/00.rename"
mkdir $rename && echo build $rename success|| echo build $raname error
perl $bin/comp0.rename.pl $config $pwd $rename

#<<COMMENT
#01.minimap
mini="$out/01.miniprot"
#1.1 build index for genomes
indexdir="$out/01.miniprot/index"
mkdir -p $indexdir && echo build $indexdir success|| echo build $indexdir error
perl $bin/comp1_1.get.miniprot.index.pl $pwd/$config $indexdir $indexdir/mini.index.sh
sh $indexdir/mini.index.sh

#01.2 run miniprot
alig="$mini/alignment"
mkdir $alig && echo build $alig success|| echo build $alig error
ls $rename/*pep.fa|awk -F "/" '{a=$0;split($NF,b,"\.");print a"\t"b[1]}'>$mini/pep.list
ls $indexdir/*mpi|awk -F "/" '{a=$0;split($NF,b,"\.");print a"\t"b[1]}'>$mini/mpi.list
perl $bin/comp1.get.mpi_sh.pl $mini/pep.list $mini/mpi.list $alig $mini/commend ##>>thread需要指定吗？


#####
#02.filter miniprot results
filter="$out/02.filter.miniprot"
evebin="$filter/every.script"
mkdir -p $filter && echo build $filter success|| echo build $filter error
mkdir -p $evebin && echo build $evebin success|| echo build $evebin error
ls $alig/*gff >$filter/miniprot.gff.list
perl $bin/comp2.get.filter.sh.pl $filter $bin $config $evebin $filter/miniprot.gff.list
ls $evebin|awk '{print "sh "$1}'
ls $evebin/*sh|awk -F "/" '{a=$0;gsub("filt.","",$NF);gsub(".sh","",$NF);print "sh "a" && echo filter miniprot of "$NF" DONE"}' >$filter/all.filter.sh
parallel  --jobs 32 <$filter/all.filter.sh

####
#03.ovelap gene to miniprot result
int="$out/03.overlap.gene.miniprot"
genebed="$int/genebed"
intresult="$int/intresult"
mkdir -p $intresult && echo build $intresult success|| echo build $intresult error
ls $filter/*/*gff >$int/miniprot.adjust.list
perl $bin/comp3.get.overlapsh.pl $config $rename $intresult $int/miniprot.adjust.list $bin >>$int/all.overlap.gene_minipro.sh
sh $int/all.overlap.gene_minipro.sh
####
#04.get.syn.block
dag="$out/04.syn.block"
dagout="$dag/DAGchainer.block.bed"
mkdir -p $dagout && echo build $dagout success|| echo build $dagout error
ls $pwd/*_*/*aligncoords >$dag/DAGchainer.file.list
for i in `cat $dag/DAGchainer.file.list`
do
	perl $bin/comp4.syn.block.bed.pl $i $dagout
done
ls $dagout/*bed|awk -F "/" '{a=$0;gsub(".syn.block.bed","",$NF);print $NF"\t"a}' >$dag/DAGchainer.synbed.list

#05.cluster.tandem duplication genes
dup="$out/05.cluster.tandem"
mkdir -p $dup && echo build $dup success|| echo build $dup error
for i in `cut -f 1 $config`
do
perl $bin/comp5.cluster.tandem.pl $i $pwd $rename $dup
done

####
#05.complement tmp Pan-sg
comp="$out/06.complement"
tmppan="$pwd/$tmppansg"
mini="$out/01.miniprot"
samplenumber=$(wc -l $config |cut -d " " -f 1)

mkdir -p $comp && echo build $comp success|| echo build $comp error

perl $bin/comp6_1.format.tmp_pansg_add.dup.pl $config $rename $dup $tmppan $samplenumber $comp/Format.pansg_add.dup.txt && echo "Done for format tmp.Pansg"
perl $bin/comp6_2.complement.pansg.pl $intresult $dagout $rename $dup $comp/Format.pansg_add.dup.txt $comp && echo "Done for complement pipline"

