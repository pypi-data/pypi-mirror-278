import logging

import gffutils
import pathlib

from pansg._logging import set_logging_level
from Bio import SeqIO, Seq, SeqRecord


# 创建或加载GFF数据库
def create_gff_db(gff, db):
    if pathlib.Path(db).is_file():
        return gffutils.FeatureDB(db, keep_order=True)
    else:
        logging.info("build your gff.db now")
        return gffutils.create_db(gff, dbfn=db, force=True, keep_order=True, merge_strategy='merge',
                                  sort_attribute_values=True)


# 获取转录本的序列
def get_transcript_sequence(transcript, genome_seq, gff_db):
    cds_seqs = []
    for cds in gff_db.children(transcript, featuretype='CDS', order_by='start'):
        cds_seq = genome_seq[cds.chrom].seq[cds.start - 1:cds.end]
        cds_seqs.append(cds_seq)
    transcript_seq = Seq.Seq('').join(cds_seqs)
    if transcript.strand == '-':
        transcript_seq = transcript_seq.reverse_complement()
    return transcript_seq


def main(config: str, verbose: str):
    set_logging_level(verbose)
    for line in open(config).read().rstrip().split('\n'):
        sample, fasta, gff = line.split('\t')
        nuc_seq = SeqIO.to_dict(SeqIO.parse(fasta, 'fasta'))
        gff_db = create_gff_db(gff, f'{pathlib.Path(gff).parent}/{pathlib.Path(gff).stem}.db')

        longest_transcripts = {}

        for gene in gff_db.features_of_type('gene'):
            transcripts = list(gff_db.children(gene, featuretype='mRNA'))
            if not transcripts:
                continue

            # 计算每个转录本的外显子长度之和，并找到最长的转录本
            longest_transcript = max(transcripts, key=lambda t: sum(
                exon.end - exon.start + 1 for exon in gff_db.children(t, featuretype='exon')))
            # 获取转录本的序列
            transcript_seq = get_transcript_sequence(longest_transcript, nuc_seq, gff_db)

            # 翻译为氨基酸序列
            pro_seq = transcript_seq.translate(to_stop=True, stop_symbol='')
            header = longest_transcript.id
            record = SeqRecord.SeqRecord(pro_seq, id=header, description='')
            longest_transcripts[header] = record

        SeqIO.write(longest_transcripts.values(), f"{pathlib.Path(fasta).parent}/{sample}.pro_fasta",
                    "fasta")


if __name__ == '__main__':
    main('data/pansg.config')
