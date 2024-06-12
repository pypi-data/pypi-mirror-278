import logging
import re

import gffutils

from pansg._logging import set_logging_level
from pathlib import Path


def cluster_tandem(tandem_pwd):
    fi = open(tandem_pwd, 'rt')
    sample_name = tandem_pwd.split('/')[-3]
    fi.readline()
    tandem_dic = {}
    last_key = ""
    lines = fi.readline()
    while lines:
        line = lines.rstrip().split('\t')
        target = sample_name + "_" + re.split(r'\.|\_|\-|\:', line[0])[0]
        repeat = sample_name + "_" + re.split(r'\.|\_|\-|\:', line[2])[0]
        if tandem_dic.get(target) == 1:
            tandem_dic[last_key] = tandem_dic[last_key] + "," + repeat
        else:
            tandem_dic[target] = repeat
            last_key = target
        tandem_dic[repeat] = 1
        lines = fi.readline()

    return tandem_dic


def sg2syn_dic(right: str, left: str, synpair: dict) -> dict:
    insyn = open(f"{right}_{left}/{right}_{left}.dag.aligncoords", 'rt')
    for lines in insyn:
        # 共线性块信息没有用
        if lines.startswith('#'):
            pass
        else:
            _, QG, _, _, _, RG, _, _, _, _ = lines.rstrip().split('\t')

            QG = right + "_" + re.split(r'\.|\_|\-|\:', QG)[0]
            RG = left + "_" + re.split(r'\.|\_|\-|\:', RG)[0]
            if len(re.split(r'\.|\_|\-|\:', QG)) > 2:
                logging.info("Only allow ., _, -, or : as separators between gene IDs and transcripts.")
            # 只保留最佳共线性对
            if QG in synpair.keys() or RG in synpair.keys():
                pass
            else:
                synpair[QG] = RG
                synpair[RG] = QG
    insyn.close()

    return synpair


def merge_gene2sg(QG: str, sg: dict, sg_rev: dict, synpair: dict) -> (dict, dict):
    sg_gene = synpair[QG]
    del sg[sg_rev[QG]]
    sg_id = sg_rev[sg_gene]
    sg[sg_id] = f"{sg[sg_id]},{QG}"
    sg_rev[QG] = sg_id
    return sg, sg_rev


def main(config, output, verbose):
    set_logging_level(verbose)
    fo = open(output, 'wt')

    td_pwd_list = []
    sample_list = []
    gff_dic = {}
    all_td_dic = {}

    sg = {}
    sg_rev = {}
    sg_order = 0
    scaffold_keywords = ["scaf", "scaffold", "contig", "SK", "unplaced", "UN"]
    for line in open(config, 'rt').read().rstrip().split('\n'):
        sample, _, gff = line.split('\t')
        td_pwd_list.append(f"{sample}/result/{sample}.tandem.pairs")
        sample_list.append(sample)
        gff_dic[sample] = gff
    # 所有的串联重复关系，将value 还原为 key
    for pwd in td_pwd_list:
        all_td_dic |= cluster_tandem(pwd)

    # 读取每个材料的所有基因，提供初始编号
    for sample, gff in gff_dic.items():
        db = gffutils.FeatureDB(str(Path(gff).with_suffix('.db')))
        for feature in db.features_of_type('gene'):
            if not any(keyword in feature.chrom for keyword in scaffold_keywords):
                gene = sample + "_" + feature.id
                if all_td_dic.get(gene) == 1:
                    # 去除串联重复基因
                    pass
                else:
                    # 初始化
                    sg[sg_order] = gene
                    sg_rev[gene] = sg_order
                    sg_order += 1

    for i in range(1, len(sample_list)):
        right = sample_list[i]
        unsyn = []
        for j in range(0, i):
            left = sample_list[j]
            logging.info(f"Current comparison: {right} vs {left}... \n")
            # 读取Mo17 和 B73的所有共线性对
            # 处理Oh7B的时候会先读Mo17后读B73
            synpair = sg2syn_dic(right, left, {})
            synpair = sg2syn_dic(left, right, synpair)

            # 读取Mo17的所有基因
            if j == 0:
                Rgff = gffutils.FeatureDB(str(Path(gff_dic[right]).with_suffix('.db')))
                for feature in Rgff.features_of_type('gene'):
                    if not any(keyword in feature.chrom for keyword in scaffold_keywords):
                        QG = right + "_" + feature.id
                        if not synpair.get(QG):
                            # 和Mo17不共线的等待后续处理
                            unsyn.append(QG)
                        else:
                            sg, sg_rev = merge_gene2sg(QG, sg, sg_rev, synpair)

                logging.info(f"Non-syntenic-to-Ref Gene Number:{len(unsyn)}!!!\n")
                logging.info("Compare to Non-Ref genomes...\n===============\n")

            else:
                # 现在处理 B73 和 Mo17 不共线的基因
                # 当i=2的时候则是处理 Oh7B 和 Mo17 不共线的基因
                unsyn_tmp = []
                logging.info(f"**Current Non-Ref Comparison: {right} vs {left}... \n==============\n")
                for private_gene in unsyn:
                    if synpair.get(private_gene):

                        if j == 1:
                            sg, sg_rev = merge_gene2sg(private_gene, sg, sg_rev, synpair)
                        else:
                            private_id = sg_rev[private_gene]
                            mediate_sg_id = sg_rev[synpair[private_gene]]
                            if private_id == mediate_sg_id:
                                pass
                            else:
                                if sg[private_id] == private_gene:
                                    sg, sg_rev = merge_gene2sg(private_gene, sg, sg_rev, synpair)
                                else:
                                    sg[private_id] = f"{sg[private_id]},{sg[mediate_sg_id]}"
                                    for gene in sg[mediate_sg_id].split(","):
                                        sg_rev[gene] = private_id
                                    del sg[mediate_sg_id]
                    else:
                        unsyn_tmp.append(private_gene)
                unsyn = unsyn_tmp

    for i, (_, v) in enumerate(sorted(sg.items(), key=lambda kv: (kv[1], kv[0]))):
        for gene in v.split(","):
            if all_td_dic.get(gene, 1) != 1:
                # 解压串联重复基因
                v = v.replace(gene, gene + "," + all_td_dic[gene])
        idx = f"SG{i + 1:07d}"
        fo.write(f'{idx}\t{v}\n')
    fo.close()


if __name__ == '__main__':
    main("data/pansg.config",
         'SG_test', 'INFO')
