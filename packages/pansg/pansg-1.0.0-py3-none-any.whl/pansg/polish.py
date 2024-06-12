import logging
import gffutils

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from pathlib import Path
from pansg._logging import set_logging_level


def process_genes(row, gene_lengths):
    genes = row['gene'].split(',')
    if row['gene_number'] > row['sample_number']:
        # 按材料分组
        materials = {}
        for gene in genes:
            material, gene_id = gene.split('_', 1)
            if material not in materials:
                materials[material] = []
            materials[material].append(gene_id)

        # 保留每种材料长度最接近中位数的基因
        selected_genes = []
        for material, gene_ids in materials.items():
            lengths = [gene_lengths[f'{material}_{gene_id}'] for gene_id in gene_ids]
            median_length = np.median(lengths)
            closest_gene = min(gene_ids, key=lambda gene_id: abs(gene_lengths[f'{material}_{gene_id}'] - median_length))
            selected_genes.append(f'{material}_{closest_gene}')
        row['gene'] = ','.join(selected_genes)
    return row


def gene_length_from_gff(sample_name, gff_pwd) -> dict:
    len_dic = {}
    db_path = str(Path(gff_pwd).with_suffix('.db'))

    # 读取GFF数据库
    db = gffutils.FeatureDB(db_path)

    for gene in db.features_of_type('gene'):
        transcripts = list(db.children(gene, featuretype='mRNA'))
        if not transcripts:
            continue

        # 计算每个转录本的外显子长度之和，并找到最长的转录本
        longest_transcript_length = max(
            sum(exon.end - exon.start + 1 for exon in db.children(transcript, featuretype='exon'))
            for transcript in transcripts
        )

        # 将结果存储在字典中
        len_dic[sample_name + "_" + gene.id] = longest_transcript_length

    return len_dic


def polish_pan_matrix(pan_matrix_path: str, name_list: list, gene_len_dic: dict):
    order_list = ['SG', 'sample_number', 'gene_number'] + name_list
    df = pd.read_csv(pan_matrix_path, sep='\t', names=['SG', 'gene'])
    df['gene_number'] = df['gene'].apply(lambda x: x.count(',') + 1)
    df['sample_number'] = df['gene'].apply(lambda x: len(set(g.split('_')[0] for g in x.split(','))))

    raw_df = df.apply(process_genes, axis=1, gene_lengths=gene_len_dic)
    for name in name_list:
        raw_df[name] = raw_df['gene'].apply(
            lambda x: next((g for g in x.split(',') if g.startswith(name + '_')), ''))

    polished_df = raw_df[order_list]
    return polished_df


def draw(polished_df, name_list):
    plt.figure(figsize=(8, 12))
    sns.set(style="white")
    palette = sns.color_palette("viridis", len(name_list))

    data = polished_df['sample_number'].value_counts().reset_index()
    data.columns = ['sample_number', 'count']
    data = data.sort_values(by='sample_number')

    barplot = sns.barplot(x='sample_number', y='count', data=data, palette=palette)

    # 设置标题和标签
    barplot.set_xlabel('Shared_Genomes', fontsize=14)
    barplot.set_ylabel('SOG_Number', fontsize=14)

    return barplot


def main(config, pan_matrix, verbose):
    set_logging_level(verbose)
    gene_len_dic = {}
    name_list = []
    for line in open(config, 'rt').read().rstrip().split('\n'):
        sample, _, gff = line.split('\t')
        name_list.append(sample)
        gene_len_dic |= gene_length_from_gff(sample, gff)

    df = polish_pan_matrix(pan_matrix, name_list, gene_len_dic)
    df.to_csv(pan_matrix + '.pan', sep='\t', index=False)
    plot = draw(df, name_list)

    outplot = pan_matrix + '.png'
    plot.get_figure().savefig(outplot, format='png', dpi=300)
    data = pd.DataFrame(df['sample_number'].value_counts()).sort_values(by='sample_number').reset_index()
    with open(pan_matrix + '.stat', 'wt') as fo:
        logging.log('-----------------------------------')
        logging.log('Shared_Genomes\tSOG_Number')
        for index, row in data.iterrows():
            logging.log(f"{row['sample_number']}\t{row['count']}")
            fo.write(f"{row['sample_number']}\t{row['count']}\n")
        logging.log('-----------------------------------')
        logging.log(f'All\t{len(df)}')


if __name__ == '__main__':
    main()
