from yxseq.seq import read_fastq_big

def fq2fa_main(args):
    if args.pair1 is None:
        raise ValueError("pair1 is None")

    if args.pair1.split(".")[-1] == "gz":
        gzip_flag = True
    else:
        gzip_flag = False

    with open(args.output, "w") as f:
        for i in read_fastq_big(args.pair1, args.pair2, gzip_flag=gzip_flag):
            if len(i) == 2:
                i1, i2 = i
                f.write(">%s\n%s\n" % (i1.seqname + "/1", i1.seq))
                f.write(">%s\n%s\n" % (i2.seqname + "/2", i2.seq))
            else:
                i1 = i[0]
                f.write(">%s\n%s\n" % (i1.seqname, i1.seq))


if __name__ == "__main__":
    class abc():
        pass

    args = abc()
    args.pair1 = "/lustre/home/xuyuxing/Database/Orchid/Apostasia/survey/Ni_clean_1.fq.gz"
    args.pair2 = "/lustre/home/xuyuxing/Database/Orchid/Apostasia/survey/Ni_clean_2.fq.gz"
    args.output = "output.fa"

    fq2fa_main(args)

    
