### 9/7/23
### Jessica L Albert
### CLI file - HIV Isoform Filtering
### last updated 9/12/23 by JLA

import argparse
import os
from HIV_Isoform_Checker.HIV_Isoform_Checker import *
    
def main():
    # create parser object
    parser = argparse.ArgumentParser(prog = "HIV Isoform Checker",
                                     formatter_class = argparse.RawDescriptionHelpFormatter,
                                     description =('''HIV Isoform Checker
Author: Jessica L Albert'''))
 
    # defining arguments for parser object
    parser.add_argument("input", type = str, 
                        metavar = "input_file_name", default = None,
                        help = "Designates input file to be filtered. This is required.")
    
    parser.add_argument("output", type = str, 
                        metavar = "output_file_prefix", default = None,
                        help = "Designates output file prefix. This is required.")
    
    parser.add_argument("ref", type = str,
                        metavar = "ref_file", default = None,
                        help = "Designates reference file name. This should be a fasta file. This is required.")
     
    parser.add_argument("-g", "--gap", type = int,
                        metavar = "value", default = 15,
                        help = "Sets gap tolerance. Default is 15.")
    
    parser.add_argument("-a", "--startBP", type = int, 
                        metavar = "value", default = 700,
                        help = "Sets maximum starting bp. Default is 700.")
     
    parser.add_argument("-z", "--endBP", type = int,
                        metavar = "value", default = 9500,
                        help = "Sets minimum ending bp.  Default is 9500.")
    
    parser.add_argument("-l", "--lengthFS", type = int, 
                        metavar = "value", default = 2100,
                        help = "Sets maximum fully spliced transcript length.  Default is 2100.")
    
    parser.add_argument("-n", "--NCE", type = str, 
                        metavar = "value", default = "False",
                        help = "When set to True, csv file will have y/n columns for the precence of NCEs. Default is False.")
    
 
    # parse the arguments from standard input
    args = parser.parse_args()

    input_file = args.input
    
    
    output_file = args.output

    ref_file = args.ref
     
    # calling functions depending on type of argument
    if args.gap !=None:
        gap_tolerance = args.gap
    if args.endBP != None:
        min_end_bp = args.endBP
    if args.startBP != None:
        max_start_bp = args.startBP
    if args.lengthFS != None:
        min_FS_len = args.lengthFS
    if args.NCE != None:
        NCE_option = args.NCE
    filter_transcripts(input_file, output_file, gap_tolerance, min_end_bp, max_start_bp, min_FS_len, NCE_option, ref_file)
 
if __name__ == "__main__":
    # calling the main function
    main()






