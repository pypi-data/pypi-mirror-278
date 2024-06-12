import logging
import subprocess
import gffutils
import shutil

from pansg._pool import parallel_process
from pansg._logging import set_logging_level
from pathlib import Path

def install_software(software, command):
    """安装软件包"""
    if shutil.which(command):
        pass
    else:
        if command == 'DupGen_finder.pl':
            logging.warning("please install DupGen_finder by yourself")
            logging.warning('git clone https://github.com/qiao-xin/DupGen_finder.git')
            logging.warning('cd DupGen_finder')
            logging.warning(
                f'make\nchmod 775 DupGen_finder.pl\nchmod 775 DupGen_finder-unique.pl\nchmod 775 set_PATH.sh\nsource set_PATH.sh')
            raise
        else:
            try:
                logging.info(f"{software} not found. Installing {software} using Conda...")
                subprocess.run(["conda", "install", "-c", "bioconda", "-y", software], check=True)
                logging.info(f"{software} installation completed.")
            except subprocess.CalledProcessError as e:
                logging.info(f"An error occurred during {software} installation: {e}")

def run_blastp(query, sub, out, thread, evalue):
    # 运行blastp
    if Path(out).is_file():
        pass
    else:
        subprocess.run(['blastp',
                        '-evalue', str(evalue),
                        '-query', query,
                        '-db', sub,
                        '-out', out,
                        '-outfmt', '6',
                        '-num_threads', str(thread)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)


def DupGen_finder(sample: str, gff: Path):
    # 处理gff文件
    db = gffutils.FeatureDB(str(gff.with_suffix('.db')))
    fo = open(f"{sample}/{sample}.gff", 'wt')
    for mrna in db.features_of_type('mRNA'):
        fo.write(f"{mrna.chrom}\t{mrna.id}\t{mrna.start}\t{mrna.end}\n")
    try:
        Path(f"{sample}/{sample}.blast").symlink_to(Path(f"./{sample}/{sample}_{sample}.blast").resolve())
        Path(f"{sample}/{sample}_{sample}.gff").symlink_to(Path(f"{sample}/{sample}.gff").resolve())
    except FileExistsError:
        logging.info(f"{sample}/{sample}.gff or {sample}/{sample}.blast is existed")
    subprocess.run(['DupGen_finder.pl',
                    '-i', sample,
                    '-t', sample,
                    '-c', sample,
                    '-o', f"{sample}/result"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def cluster_tandem(tandem_pwd):
    fi = open(tandem_pwd, 'rt')
    fi.readline()
    tandem_dic = {}
    last_key = ""
    lines = fi.readline()
    while lines:
        line = lines.rstrip().split('\t')
        if tandem_dic.get(line[0]) == 1:
            tandem_dic[last_key] = tandem_dic[last_key] + "," + line[2]
        else:
            tandem_dic[line[0]] = line[2]
            last_key = line[0]
        tandem_dic[line[2]] = 1
        lines = fi.readline()

    return tandem_dic


def run_dag_chainer(blastp_out, D, g, A):
    # 将blastp输出结果转化为dagchainer的输入，并最终调用
    ref, que = blastp_out.split('/')[-2].split('_')
    dag_fn = str(Path(blastp_out).with_suffix('.dag').resolve())
    temp_fo = open(dag_fn, 'wt')
    r_gff = open(f"{ref}/{ref}.gff", 'rt')
    q_gff = open(f"{que}/{que}.gff", 'rt')

    r_td_dic = cluster_tandem(f"{ref}/result/{ref}.tandem.pairs")
    q_td_dic = cluster_tandem(f"{que}/result/{que}.tandem.pairs")
    qs = {}
    qe = {}
    qchr = {}
    rs = {}
    re = {}
    rchr = {}

    lines = r_gff.readline()
    while lines:
        r_chr, gene, r_s, r_e = lines.rstrip().split("\t")
        rs[gene] = r_s
        re[gene] = r_e
        rchr[gene] = r_chr
        lines = r_gff.readline()
    lines = q_gff.readline()
    r_gff.close()
    while lines:
        q_chr, gene, q_s, q_e = lines.rstrip().split("\t")
        qs[gene] = q_s
        qe[gene] = q_e
        qchr[gene] = q_chr
        lines = q_gff.readline()
    q_gff.close()

    fi = open(blastp_out, 'rt')
    lines = fi.readline()
    while lines:
        line = lines.rstrip().split('\t')
        qblast = line[1]
        rblast = line[0]
        pvalue = line[-2]
        if qblast not in qs.keys() or rblast not in rs.keys():
            # 去掉不存在于gff文件中的基因
            break
        else:
            if rchr[rblast] != qchr[qblast]:
                # 去掉不同染色体上的比对
                pass
            else:
                if q_td_dic.get(qblast) or r_td_dic.get(rblast):
                    # 去掉串联重复(将在后续步骤中返回流程)
                    pass
                else:
                    temp_fo.write(
                        f"{ref}_{rchr[rblast]}\t{rblast}\t{rs[rblast]}\t{re[rblast]}\t{que}_{qchr[qblast]}\t{qblast}\t{qs[qblast]}\t{qe[qblast]}\t{pvalue}\n")

        lines = fi.readline()
    # 运行 DAG chainer
    try:
        subprocess.run(['run_DAG_chainer.pl', '-s', '-I',
                        '-i', dag_fn,
                        '-D', str(D),
                        '-g', str(g),
                        '-A', str(A)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while running run_DAG_chainer.pl: {e.stderr}")
        raise


def process_pairs(pair, thread, evalue, D, g, A):
    tasks = []
    for x, y in pair:
        Path(f'{Path(x).stem}_{Path(y).stem}').mkdir(parents=True, exist_ok=True)
        blastp_out = f'{Path(x).stem}_{Path(y).stem}/{Path(x).stem}_{Path(y).stem}.blast'
        logging.info(blastp_out + ' run blastp now')
        Path(f"{Path(x).stem}_{Path(y).stem}").mkdir(parents=True, exist_ok=True)
        run_blastp(x, y, blastp_out, thread, evalue)
        tasks.append((run_dag_chainer, blastp_out, D, g, A))
    return tasks


def main(config: str, thread: int = 8, D: int = 200000, g: int = 10000,
         A: int = 6, evalue: float = 1e-20, verbose='ERROR'):
    set_logging_level(verbose)
    pro_fasta_list = []
    gff_dic = {}
    for line in open(config, 'rt').read().rstrip().split('\n'):
        sample, fasta, gff = line.split('\t')
        Path(sample).mkdir(parents=True, exist_ok=True)
        pro_fasta_list.append(f"{Path(fasta).parent}/{sample}.pro_fasta")
        gff_dic[sample] = Path(gff)
    pair = []
    install_software('blast', 'makeblastdb')


    for i in range(0, len(pro_fasta_list)):
        subprocess.run(['makeblastdb',
                        '-in', pro_fasta_list[i],
                        '-dbtype', 'prot',
                        '-out', pro_fasta_list[i]], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       text=True)
        # 鉴定串联重复
        sample_dir = Path(pro_fasta_list[i]).stem
        run_blastp(pro_fasta_list[i], pro_fasta_list[i],
                   f'{sample_dir}/{Path(pro_fasta_list[i]).stem}_{sample_dir}.blast', thread, evalue)
        install_software('DupGen_finder', 'DupGen_finder.pl')
        DupGen_finder(sample_dir, gff_dic[sample_dir])
        for j in range(i + 1, len(pro_fasta_list)):
            pair.append([pro_fasta_list[i], pro_fasta_list[j]])
            pair.append([pro_fasta_list[j], pro_fasta_list[i]])
    install_software("dagchainer", "run_DAG_chainer.pl")
    tasks = process_pairs(pair, thread, evalue, D, g, A)
    try:
        parallel_process(tasks, num_processes=min(len(tasks), thread, 1))  # 并行处理 run_dag_chainer 任务
    except TypeError:
        logging.info("Why NoneType?")
        raise


if __name__ == '__main__':
    main()
