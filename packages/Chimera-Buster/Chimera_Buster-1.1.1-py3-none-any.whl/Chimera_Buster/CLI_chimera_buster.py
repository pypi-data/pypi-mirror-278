## CLI for Chimera_buster
## By: Jessica L Albert
## Last edited : 3/5/24

import argparse
import os
from chimera_buster import *

def main():
    # create parser object
    parser = argparse.ArgumentParser(prog = "Chimera_buster",
                                     formatter_class = argparse.RawDescriptionHelpFormatter,
                                     description =('''UMI-based Chimera Buster
Author: Jessica L Albert'''))
 
    # defining arguments for parser object
    parser.add_argument("input_folder", type = str, 
                        metavar = "input_folder", default = None,
                        help = "Designates MrHamer sample folder to process UMIs from. This is required.")

    parser.add_argument("output", type = str, 
                        metavar = "output_file_prefix", default = None,
                        help = "Designates output file prefix. This is required.")
    
    parser.add_argument("-m", "--mismatch", type = int,
                        metavar = "int", default = 1,
                        help = "Designates the maximun number of mismatched/indel bases. Default is 1.")
     

 
    # parse the arguments from standard input
    args = parser.parse_args()

    folder = './' + args.input_folder + '/clustering_consensus/'
    sub_folders = (os.listdir(folder))
    for folder in sub_folders:
        if folder != '.DS_Store':
            sample_folder = folder
    
    sample_file = args.input_folder + "/clustering_consensus/" + sample_folder + "/clusters_consensus.fasta"

    size_file = args.input_folder + "/clustering/" + sample_folder + "/clusters_consensus.fasta"
    
    output_name = args.output
         
    # calling functions depending on type of argument
    if args.mismatch !=None:
        mismatch_tolerance = args.mismatch
             
    chimera_buster(sample_file, size_file, output_name, mismatch_tolerance)
    
if __name__ == "__main__":
    # calling the main function
    main()

