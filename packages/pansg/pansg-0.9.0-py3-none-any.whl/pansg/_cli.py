from fire import Fire
from pansg.blastp_2_dagchainer import main as blastp_2_dagchainer
from pansg.extract_longest_protein import main as extract_longest_protein
from pansg.merge import main as merge
from pansg.polish import main as polish
from pansg.complement import main as complement


class Cli(object):
    """make your syntelog-based pan-genome

    - pansa is a commandline tool and a python package to build a syntelog-based pan-genome matrix.
    - It is recommended to create a new folder to run the processes in this software.
    - To avoid unnecessary bugs, it is recommended to retain only the information from the chromosomal regions and remove the scaffold regions in the input GFF file.
    """

    def extract_longest_protein(self, config: str, verbose: str = 'ERROR'):
        """ Extract the longest amino acid sequence for each gene from the DNA sequence file using the GFF3 annotation file for subsequent synteny identification.
        :param config: <sample_name>    <fasta_path>    <gff3_path>
        :param verbose: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
        :return :
        """
        return extract_longest_protein(config=config, verbose=verbose)

    def blastp_2_dagchainer(self, config: str, thread: int = 8, D: int = 1000000, g: int = 40000,
                            A: int = 5, evalue: float = 1e-5, verbose: str = 'ERROR'):
        """ Run dagchainer
        :param config: <sample_name>    <fasta_path>    <gff3_path>
        :param thread: thread number
        :param D: maximum distance allowed between two matches in basepairs
        :param g: length of a gap in bp
        :param A: Minium number of Aligned Pairs
        :param evalue: E-value threshold for blastp. A stricter parameter results in a faster DAGchainer run. It is an important parameter
        :param verbose: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
        :return:
        """
        return blastp_2_dagchainer(config=config, thread=thread, D=D, g=g, A=A, evalue=evalue, verbose=verbose)

    def merge(self, config: str, output: str = 'SG_test', verbose: str = 'ERROR'):
        """ Merge the results of syntelog
        :param config: <sample_name>    <fasta_path>    <gff3_path>  You can merge only the part of the samples you want.\
        The first sample will serve as the reference genome for subsequent merged syntelog matrices. Please select the assembly with the highest quality.
        :param output: your raw syntelog-based pan-genome matrix
        :param verbose: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
        :return:
        """
        return merge(config=config, output=output, verbose=verbose)

    def polish(self, config: str, pan_matrix: str = 'SG_test', verbose: str = 'INFO'):
        """ Generate a more readable and simplified pan-genome matrix
        :param config: <sample_name>    <fasta_path>    <gff3_path>
        :param pan_matrix: your syntelog-based pan-genome matrix pathway
        :param verbose: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
        :return:
        """
        return polish(config=config, pan_matrix=pan_matrix, verbose=verbose)

    def complement(self, config: str, pan_matrix: str = 'SG_test.pan', verbose: str = 'INFO'):
        """
        :param config: <sample_name>    <fasta_path>    <gff3_path>
        :param pan_matrix: your syntelog-based pan-genome matrix after polishing
        :param verbose: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
        :return:
        """
        return complement(config=config, pan_matrix=pan_matrix, verbose=verbose)


def main():
    cli = Cli()
    Fire(cli, name='pansg')


if __name__ == '__main__':
    main()
