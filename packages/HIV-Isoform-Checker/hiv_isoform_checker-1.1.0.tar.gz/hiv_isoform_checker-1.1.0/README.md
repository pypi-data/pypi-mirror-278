# HIV Isoform Checker

This package takes a .gtf file of preliminarily filtered HIV transcripts from ONT sequencing
and filters them to include only correctly assigned transcripts using the
following filters.
- FILTER 1: only include class codes =, J, and m
- FILTER 2: only include samples with end values >= min_end_bp and
           start values <= max_start_bp
- FILTER 3: get rid of any samples with read errors/small gaps
- FILTER 4: keep only correct Env samples
- FILTER 5: keep only correct Nef samples(long samples added to possible_misassigned)  
- FILTER 6: keep only correct Rev samples(long samples added to possible_misassigned)  
- FILTER 7: keep only correct Tat samples(long samples added to possible_misassigned)   
- FILTER 8: keep only correct Vif samples
- FILTER 9: keep only correct Vpr samples
- FILTER 10: check possible_misassigned for partial splice compatibility
           (vif -> vpr -> unslpiced_tat -> env)

> Note: This code currently relies on a very specific setup of the gtf file to work properly. The note must be in the order designated in the [].
transcript entry = ref genome, analysis_pathway, transcript, start, end, ".", "+", ".", [transcript id; gene id; gene_name; xloc; ref_gene_id; contained_in; cmp_ref; class_code; tss_id]
>exon entry = ref genome, analysis_pathway, exon, start, end, ".", "+", ".", [transcript id; gene id; exon number]

## Installation
Fast install:

    pip install HIV_Isoform_Checker
   

## Usage
    HIV_Isoform_Checker [options] input_file_name output_file_prefix ref_file_name

positional arguments:
  input_file_name       Designates input file to be filtered. This is required.
  output_file_prefix    Designates output file prefix. This is required.
  ref_file_name         Designates reference CDS file name. This should be a python file with only a dictionary with the splice donor sites, splice acceptor sites and gene CDS regions defined. This is required. An example is available in the test data set.

options:
| Arguement | Function |
| ------ | ------ |
|-h, --help |  show this help message and exit |
|-g value, --gap value|Sets gap tolerance. Default is 15.
|-a value, --startBP value|Sets maximum starting bp. Default is 700.
|-z value, --endBP value|Sets minimum ending bp. Default is 9500.
|-l value, --lengthFS value|Sets maximum fully spliced transcript length. Default is 2100.
|-n value, --NCE value|When set to True, csv file will have y/n columns for the precence of NCEs. Default is False.

## License

MIT - Copyright (c) 2023 Jessica Lauren Albert

# HIV_Isoform_Checker
