import subprocess
import shutil
import logging

from pansg._logging import set_logging_level
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


def main(config, pan_matrix, verbose):
    set_logging_level(verbose)
    install_software('miniprot', 'miniprot')
    install_software('bedtools', 'bedtools')
    install_software('parallel','parallel')
    subprocess.run(['bash',
                    'run.complement.sh',
                    config, pan_matrix], shell=True, check=True)

if __name__ == '__main__':
    main('data/pansg.config')