import argparse
from yxseq.pipeline import fq2fa_main


class Job(object):
    def __init__(self):
        pass

    def run_arg_parser(self):
        # argument parse
        parser = argparse.ArgumentParser(
            prog='yxseq',
        )

        subparsers = parser.add_subparsers(
            title='subcommands', dest="subcommand_name")

        # argparse for fq2fa
        parser_a = subparsers.add_parser('fq2fa',
                                         description='Convert fastq to fasta\n')

        parser_a.add_argument('-1', '--pair1', type=str,
                                help='input fastq pair1')
        parser_a.add_argument('-2', '--pair2', type=str,
                                help='input fastq pair2')
        parser_a.add_argument('-o', '--output', type=str,
                                help='output fasta', default="output.fa")
        parser_a.set_defaults(func=fq2fa_main)

        # # argparse for extractor
        # parser_a = subparsers.add_parser('extractor',
        #                                  description='Extraction of useful submatrices by sample listing, variant site quality control\n')

        # parser_a.add_argument('sample_id_list_file', type=str,
        #                       help='a list file which store samples id')
        # parser_a.add_argument('input_vmo_path', type=str,
        #                       help='input vmo directory')
        # parser_a.add_argument('output_vmo_path', type=str,
        #                       help='output vmo directory')
        # parser_a.add_argument('-m', '--maf_thr', type=float,
        #                       help='min minor allele frequency', default=0.05)
        # parser_a.add_argument('-s', '--mis_thr', type=float,
        #                       help='max proportion of missing data', default=0.5)
        # parser_a.add_argument('-c', '--chunk_size', type=int,
        #                       help='chunk size', default=2000)
        # parser_a.add_argument('-n', '--n_jobs', type=int,
        #                       help='number of parallel jobs', default=20)
        # parser_a.set_defaults(func=extractor_main)

        self.arg_parser = parser

        self.args = parser.parse_args()

        # parser.set_defaults(func=parser.print_help())

    def run(self):
        self.run_arg_parser()

        if self.args.subcommand_name == 'fq2fa':
            fq2fa_main(self.args)
        # elif args_dict["subcommand_name"] == "extractor":
        #     extractor_main(self.args)
        # elif args_dict["subcommand_name"] == "distance":
        #     distance_main(self.args)
        else:
            self.arg_parser.print_help()


def main():
    job = Job()
    job.run()


if __name__ == '__main__':
    main()
