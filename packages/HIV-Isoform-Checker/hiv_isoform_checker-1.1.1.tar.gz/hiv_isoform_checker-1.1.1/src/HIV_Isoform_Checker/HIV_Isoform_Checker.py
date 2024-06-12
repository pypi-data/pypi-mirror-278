### 8/30/23
### Jessica L Albert
### HIV Isoform Filtering
### last updated 05/16/24 by JLA

import regex as re
import csv
import math
from Reference_aligner import *

#########################

#FILTER 1: only include class codes =, J, and m
#FILTER 2: only include samples with end values >= min_end_bp and start values <= max_start_bp
#FILTER 3: get rid of any samples with read errors/small gaps
#FILTER 4: keep only correct Env samples
#FILTER 5: keep only correct Nef samples (long samples added to possible_misassigned)  
#FILTER 6: keep only correct Rev samples (long samples added to possible_misassigned)  
#FILTER 7: keep only correct Tat samples (long samples added to possible_misassigned)   
#FILTER 8: keep only correct Vif samples
#FILTER 9: keep only correct Vpr samples
#FILTER 10: check possible_misassigned for partial splice compatibility (vif, vpr, unslpiced_tat, env)

#########################


def filter_transcripts(input_file, output_file, gap_tolerance, min_end_bp, max_start_bp, min_FS_len, NCE_option, ref_file):

    transcripts = []

    #caluculate reference genome info
    CIGAR = CIGAR_for_new_ref(ref_file)

    D1 = calc_shift(CIGAR, 743)
    D2 = calc_shift(CIGAR, 4962) 
    D2b = calc_shift(CIGAR, 5058) 
    D3 = calc_shift(CIGAR, 5463)
    D4 = calc_shift(CIGAR, 6044) 
    A1 = calc_shift(CIGAR, 4913) 
    A2 = calc_shift(CIGAR, 5390) 
    A3 = calc_shift(CIGAR, 5777) 
    A4a = calc_shift(CIGAR, 5954)
    A4b = calc_shift(CIGAR, 5960)
    A4c = calc_shift(CIGAR, 5936)
    A5 = calc_shift(CIGAR, 5976)
    A7 = calc_shift(CIGAR, 8369)
    A7c = calc_shift(CIGAR, 8345)
    gag_CDS = [calc_shift(CIGAR, 790), calc_shift(CIGAR, 2289)]
    pol_CDS = [calc_shift(CIGAR, 2085), calc_shift(CIGAR, 5093)]
    env_CDS = [calc_shift(CIGAR, 6221), calc_shift(CIGAR, 8782)]
    nef_CDS = [calc_shift(CIGAR, 8787), calc_shift(CIGAR, 9404)]
    rev_CDS1 = [calc_shift(CIGAR, 5969), calc_shift(CIGAR, 6044)]
    rev_CDS2 = [calc_shift(CIGAR, 8369), calc_shift(CIGAR, 8640)]
    tat_CDS1 = [calc_shift(CIGAR, 5830), calc_shift(CIGAR, 6044)]
    tat_CDS2 = [calc_shift(CIGAR, 8369), calc_shift(CIGAR, 8411)]
    vif_CDS = [calc_shift(CIGAR, 5041), calc_shift(CIGAR, 5616)]
    vpr_CDS = [calc_shift(CIGAR, 5559), calc_shift(CIGAR, 5846)]
    list_of_acceptors = [A1, A2, A3, A4a, A4b, A4c, A5, A7, A7c]
    list_of_donors = [D1, D2, D2b, D3, D4]
    
    #Change gtf file to a list of lists
    with open(input_file) as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"):
            transcripts.append(line)

    #Each transcript dictonary entry is formated as (position in parenthesis):
    # [ref genome(0), pinfish(1), transcript(2), start(3), end(4), "."(5), "+"(6), "."(7), transcript id;
    # gene id; gene_name; xloc; ref_gene_id; contained_in; cmp_ref; class_code; tss_id(8)]

    'NOTE: order of atrribute list (8) needs to be in this order for the program to run properly'

    #Each exon dictonary entry is formated as (position in parenthesis):
    # [ref genome(0), pinfish(1), exon(2), start(3), end(4), "."(5), "+"(6), "."(7), transcript id;
    # gene id; exon number(8)]

    working_list =[]

    #Changes a list of lists into a sigle list

    def flatten_list(data):
        flat_list = []
        for element in data:
            if type(element) == list:
                for item in element:
                    flat_list.append(item)
            else:
                flat_list.append(element)
        return flat_list


    #Gets rid of some unnecessary info and splits the notes into individual items
            
    entry_num = 0

    for entry in transcripts:
        transcripts[entry_num] = [entry[2] , entry[3], entry[4], entry[8].split(";")]
        transcripts[entry_num] = flatten_list(transcripts[entry_num])
        entry_num = entry_num + 1

    #Creates a list for each sample with only the desired information in the correct order from the list

    for sublist in transcripts:
        splice_varient = []
        if sublist[0] == 'transcript':
            #add transcript_id to list [0]
            splice_varient.append(sublist[3])
            transcript_id = re.findall('["](.*)["]', splice_varient[0])
            splice_varient[0] = transcript_id[0]
            #add cluster size to list [1]
            cluster_size = re.findall('[|](.*)["]', sublist[3])
            splice_varient.append(int(cluster_size[0]))
            #add cmp_ref to list [2]
            splice_varient.append(sublist[-4])
            cmp_ref = re.findall('["](.*)["]', splice_varient[2])
            splice_varient[2] = cmp_ref[0]
            #add start to list [3]
            splice_varient.append(int(sublist[1]))
            #add end to list [4]
            splice_varient.append(int(sublist[2]))
            #add class code to list [5]
            'NOTE: for i class codes, the order of the original input from the gtf file is in a different order'
            'if we want to include those at some point, we will need to rework this part of the code'
            splice_varient.append(sublist[-3])
            class_code = re.findall('["](.*)["]', splice_varient[5])
            splice_varient[5] = class_code[0]
            #add list of exons to list [6]
            exon_list =[]
            for entry in transcripts:
                if entry[0] == 'exon':
                    if entry[3] == sublist[3]:
                        start = int(entry[1])
                        end = int(entry[2])
                        exon_list.append([start, end])
            splice_varient.append(exon_list) 
            #add coverage length to list [7]
            total_length = 0
            for exon in splice_varient[6]:
                exon_length = exon[1] - exon[0] + 1 #plus 1 is to add back the bp that is the starting bp
                total_length = total_length + exon_length
            splice_varient.append(total_length)
            #add sqrt of cov_len [8]
            sqrt_cov_len = math.sqrt(splice_varient[7])
            splice_varient.append(sqrt_cov_len)
            #add normalized counts [9]
            norm_counts = splice_varient[1]* splice_varient[8]
            splice_varient.append(norm_counts)
            if NCE_option == "True" or NCE_option == "true" or NCE_option == "T" or NCE_option == "t":
                #check for NCE2 [10]
                for exon in splice_varient[6]:
                    if exon[1] == D2 and exon[0] == A1:
                        splice_varient.append("Y")
                if len(splice_varient) < 11:
                    splice_varient.append("N")
                #check for NCE2b [11]
                for exon in splice_varient[6]:
                    if exon[1] == D2b and exon[0] == A1:
                        splice_varient.append("Y")
                if len(splice_varient) < 12:
                    splice_varient.append("N")
                #check for NCE3 [12]
                for exon in splice_varient[6]:
                    if exon[1] == D3 and exon[0] == A2:
                        splice_varient.append("Y")
                if len(splice_varient) < 13:
                    splice_varient.append("N")   
            #add created list to list of all samples 
            working_list.append(splice_varient)

    ##FILTER 1: sort working list to only include class codes =, J, and m
    filter1_list = []
    sample_num = 0
    filter1_fail = []

    for sample in working_list:
        if sample[5] == '=' or sample[5] == 'j' or sample[5] == 'm':
            filter1_list.append(sample)
        else:
            filter1_fail.append(sample)
        sample_num = sample_num + 1

    ##FILTER 2: sort filter1_list to only include samples with end values >= min_end_bp and start values <= max_start_bp

    filter2_list = []
    sample_num = 0
    filter2_fail = []

    for sample in filter1_list:
        if sample[4] >= min_end_bp and sample[3] <= max_start_bp:
            filter2_list.append(sample)
        else:
            filter2_fail.append(sample)
        sample_num = sample_num + 1

    ##FILTER 3: sort filter2_list to get rid of any samples with read errors/small gaps

    filter3_list = []
    sample_num = 0
    filter3_fail = []
    exons_altered_list = []

    for sample in filter2_list:
        exon_start = []
        exon_end = []
        for exon in sample[6]:
            exon_start.append(exon[0])
            exon_end.append(exon[1])
        num_exons = len(exon_start)
        add_sample = 1
        while num_exons > 1:
            if (exon_start[(num_exons-1)] - exon_end[(num_exons-2)]) < gap_tolerance:
                del exon_start[(num_exons-1)]
                del exon_end[(num_exons-2)]
                sample.append("exon edited")
                exons_altered_list.append(sample)
            else:
                if (exon_start[(num_exons-1)] in list_of_acceptors or exon_start[(num_exons-1)]< max_start_bp) and (exon_end[(num_exons-2)] in list_of_donors or exon_end[(num_exons-2)] > min_end_bp):
                   add_sample = add_sample + 1 
            num_exons = num_exons - 1      
        if add_sample == len(exon_start):
            new_exon_list = []
            added_exons = 0
            while added_exons < len(exon_start):
                start = exon_start[added_exons]
                end = exon_end[added_exons]
                new_exon_list.append([start, end])
                added_exons = added_exons + 1
            sample[6] = new_exon_list
            if len(sample) < 14:
                sample.append("N/A")
            filter3_list.append(sample)
        else:
            filter3_fail.append(sample)
        sample_num = sample_num + 1      


    ##FILTER 4: sort filter2_list to create env_list with only correct Env samples

    env_list = []
    sample_num = 0

    for sample in filter3_list:
        if sample[2] == "env" or sample[2] == "env-A4a" or sample[2] == "env-A4b" or sample[2] == "env-A4c":
            bp_list =[]
            for exon in sample[6]:
                exon_bps = []
                exon_bps = list(range(exon[0], exon[1]))
                #print (exon_bps)
                bp_list.append(exon_bps)
            bp_list = flatten_list(bp_list)
            if all(value in bp_list for value in list(range(env_CDS[0], env_CDS[1]))):
                env_list.append(sample)
            else:
                possible_misassigned.append(sample)
        sample_num = sample_num + 1

    ##FILTER 5: sort filter2_list to create nef_list with only correct nef samples

    nef_list = []
    possible_misassigned =[]
    sample_num = 0

    for sample in filter3_list:
        if sample[2] == "nef":
            if sample[7] <= min_FS_len:
                bp_list =[]
                for exon in sample[6]:
                    exon_bps = []
                    exon_bps = list(range(exon[0], exon[1]))
                    #print (exon_bps)
                    bp_list.append(exon_bps)
                bp_list = flatten_list(bp_list)
                if all(value in bp_list for value in list(range(nef_CDS[0], nef_CDS[1]))):
                    nef_list.append(sample)
                else:
                    possible_misassigned.append(sample)
            else:
                possible_misassigned.append(sample)
        sample_num = sample_num + 1
      
    ##FILTER 6: sort filter2_list to create rev_list with only correct rev samples

    rev_list = []
    sample_num = 0

    for sample in filter3_list:
        if sample[2] == "rev" or sample[2] == "rev-A4a" or sample[2] == "rev-A4b" or sample[2] == "rev-A4c":
            if sample[7] <= min_FS_len:
                bp_list =[]
                for exon in sample[6]:
                    exon_bps = []
                    exon_bps = list(range(exon[0], exon[1]))
                    #print (exon_bps)
                    bp_list.append(exon_bps)
                bp_list = flatten_list(bp_list)
                if all(value in bp_list for value in list(range(rev_CDS1[0], rev_CDS1[1]))) and all(value in bp_list for value in list(range(rev_CDS2[0], rev_CDS2[1]))):
                    rev_list.append(sample)
                else:
                    possible_misassigned.append(sample)
            else:
                possible_misassigned.append(sample)
        sample_num = sample_num + 1

    ##FILTER 7: sort filter2_list to create tat_list with only correct tat samples

    tat_list = []
    sample_num = 0

    for sample in filter3_list:
        if sample[2] == "tat":
            if sample[7] <= min_FS_len:
                bp_list =[]
                for exon in sample[6]:
                    exon_bps = []
                    exon_bps = list(range(exon[0], exon[1]))
                    #print (exon_bps)
                    bp_list.append(exon_bps)
                bp_list = flatten_list(bp_list)
                if all(value in bp_list for value in list(range(tat_CDS1[0], tat_CDS1[1]))) and all(value in bp_list for value in list(range(tat_CDS2[0], tat_CDS2[1]))):
                    tat_list.append(sample)
                else:
                    possible_misassigned.append(sample)
            else:
                possible_misassigned.append(sample)
        sample_num = sample_num + 1

    ##FILTER 8: sort filter2_list to create vif_list with only correct Vif samples

    vif_list = []
    sample_num = 0

    for sample in filter3_list:
        if sample[2] == "vif":
            bp_list =[]
            for exon in sample[6]:
                exon_bps = []
                exon_bps = list(range(exon[0], exon[1]))
                #print (exon_bps)
                bp_list.append(exon_bps)
            bp_list = flatten_list(bp_list)
            if all(value in bp_list for value in list(range(vif_CDS[0], vif_CDS[1]))):
                vif_list.append(sample)
            else:
                possible_misassigned.append(sample)
        sample_num = sample_num + 1

    ##FILTER 9: sort filter2_list to create vpr_list with only correct Vpr samples

    vpr_list = []
    sample_num = 0

    for sample in filter3_list:
        if sample[2] == "vpr":
            bp_list =[]
            for exon in sample[6]:
                exon_bps = []
                exon_bps = list(range(exon[0], exon[1]))
                bp_list.append(exon_bps)
            bp_list = flatten_list(bp_list)
            if all(value in bp_list for value in list(range(vpr_CDS[0], vpr_CDS[1]))):
                vpr_list.append(sample)
            else:
                possible_misassigned.append(sample)
        sample_num = sample_num + 1

    ##FILTER 10: check possible_misassigned for compatibility with other isoforms

    sample_num = 0
    still_misassigned =[]

    for sample in possible_misassigned:
        bp_list =[]
        for exon in sample[6]:
            exon_bps = []
            exon_bps = list(range(exon[0], exon[1]))
            bp_list.append(exon_bps)
        bp_list = flatten_list(bp_list)
        #check for nef compatability
        if all(value in bp_list for value in list(range(nef_CDS[0], nef_CDS[1]))) and sample[7] <= min_FS_len:
            sample[2] = "nef"
            nef_list.append(sample)
        #check for rev compatability
        elif all(value in bp_list for value in list(range(rev_CDS1[0], rev_CDS1[1]))) and all(value in bp_list for value in list(range(rev_CDS2[0], rev_CDS2[1]))) and sample[7] <= min_FS_len:
            for exon in sample[6]:
                if exon[0] == A4a:
                    sample[2] = "rev-A4a"
                    rev_list.append(sample)
                elif exon[0] == A4b:
                    sample[2] = "rev-A4b"
                    rev_list.append(sample)
                elif exon[0] == A4c:
                    sample[2] = "rev-A4c"
                    rev_list.append(sample)
        #check for tat compatability
        elif all(value in bp_list for value in list(range(tat_CDS1[0], tat_CDS1[1]))) and all(value in bp_list for value in list(range(tat_CDS2[0], tat_CDS2[1]))) and sample[7] <= min_FS_len:
            sample[2] = "tat"
            tat_list.append(sample)
        #check for vif compatibility
        elif all(value in bp_list for value in list(range(vif_CDS[0], vif_CDS[1]))):
            sample[2] = "vif"
            vif_list.append(sample)
        #check for vpr compatibility
        elif all(value in bp_list for value in list(range(vpr_CDS[0], vpr_CDS[1]))):
            sample[2] = "vpr"
            vpr_list.append(sample)
        #check for tat_unspliced compatibility
        elif all(value in bp_list for value in list(range(tat_CDS1[0], tat_CDS1[1]))) and all(value in bp_list for value in list(range(tat_CDS2[0], tat_CDS2[1]))):
                    sample[2] = "tat-unspliced"
                    tat_list.append(sample)
        #check for env compatibility
        elif all(value in bp_list for value in list(range(env_CDS[0], env_CDS[1]))):
            for exon in sample[6]:
                if exon[0] == A5:
                    sample[2] = "env"
                    env_list.append(sample)
                elif exon[0] == A4a:
                    sample[2] = "env-A4a"
                    env_list.append(sample)
                elif exon[0] == A4b:
                    sample[2] = "env-A4b"
                    env_list.append(sample)
                elif exon[0] == A4c:
                    sample[2] = "env-A4c"
                    env_list.append(sample)
        else:
            still_misassigned.append(sample)
        sample_num = sample_num + 1
        
    #Output message to terminal for passing but misassigned samples
    if len(still_misassigned) != 0:
        print ("There are still possible misassigened samples:")
        print (still_misassigned)

    #Combine all failed reads
    failed_list = []
    for sample in filter1_fail:
        failed_list.append(sample)
    for sample in filter2_fail:
        failed_list.append(sample)    
    for sample in filter3_fail:
        failed_list.append(sample)
    for sample in still_misassigned:
        failed_list.append(sample)

    #Combine all sequence lists into final list to be output to csv file
    #Calculate Size normalized Isoform counts
    final_list = []
    env_count = 0
    envA4a_count = 0
    envA4b_count = 0
    envA4c_count = 0
    nef_count = 0
    revA4a_count = 0
    revA4b_count = 0
    revA4c_count = 0
    tat_count = 0
    tat_unspliced_count = 0
    vif_count = 0
    vpr_count = 0

    
    for sample in env_list:
        if sample[2] == "env":
            env_count = env_count + sample[9]
        elif sample[2] == "env-A4a":
            envA4a_count = envA4a_count + sample[9]
        elif sample[2] == "env-A4b":
            envA4b_count = envA4b_count + sample[9]
        elif sample[2] == "env-A4c":
            envA4c_count = envA4c_count + sample[9]
        final_list.append(sample)

    for sample in nef_list:
        nef_count = nef_count + sample[9]
        final_list.append(sample)

    for sample in rev_list:
        if sample[2] == "rev-A4a":
            revA4a_count = revA4a_count + sample[9]
        elif sample[2] == "rev-A4b":
            revA4b_count = revA4b_count + sample[9]
        elif sample[2] == "rev-A4c":
            revA4c_count = revA4c_count + sample[9]
        final_list.append(sample)

    for sample in tat_list:
        if sample[2] == "tat":
            tat_count = tat_count + sample[9]
        elif sample[2] == "tat-unspliced":
            tat_unspliced_count = tat_unspliced_count + sample[9]
        final_list.append(sample)
        
    for sample in vif_list:
        vif_count = vif_count + sample[9]
        final_list.append(sample)

    for sample in vpr_list:
        vpr_count = vpr_count + sample[9]
        final_list.append(sample)

    total_norm_count = env_count + envA4a_count + envA4b_count + envA4c_count + nef_count + revA4a_count + revA4b_count + revA4c_count + tat_count + tat_unspliced_count + vif_count + vpr_count

    #Calculate Spice site usage
    splice_count = 0
    
    D1_count = 0
    D2_count = 0
    D2b_count = 0
    D3_count = 0
    D4_count = 0
    
    A1_count = 0
    A2_count = 0
    A3_count = 0
    A4a_count = 0
    A4b_count = 0
    A4c_count = 0
    A5_count = 0
    A7_count = 0
    A7c_count = 0

    D1_A1_count = 0
    D1_A2_count = 0
    D1_A3_count = 0
    D1_A4a_count = 0
    D1_A4b_count = 0
    D1_A4c_count = 0    
    D1_A5_count = 0
    D1_A7_count = 0
    D1_A7c_count = 0
    
    D2_A2_count = 0
    D2_A3_count = 0
    D2_A4a_count = 0
    D2_A4b_count = 0
    D2_A4c_count = 0    
    D2_A5_count = 0
    D2_A7_count = 0
    D2_A7c_count = 0

    D2b_A2_count = 0
    D2b_A3_count = 0
    D2b_A4a_count = 0
    D2b_A4b_count = 0
    D2b_A4c_count = 0    
    D2b_A5_count = 0
    D2b_A7_count = 0
    D2b_A7c_count = 0

    D3_A3_count = 0
    D3_A4a_count = 0
    D3_A4b_count = 0
    D3_A4c_count = 0    
    D3_A5_count = 0
    D3_A7_count = 0
    D3_A7c_count = 0
    
    D4_A7_count = 0
    D4_A7c_count = 0
    
    for sample in final_list:
        list_exons = sample[6]
        exon_num = 0
        for exon in list_exons:
            splice_count = splice_count + sample[1]
            if exon_num < (len(list_exons)-1):
                next_exon = list_exons[exon_num + 1]
            if exon[1] == D1:
                D1_count = D1_count + sample[1]
                if next_exon[0] == A1:
                    A1_count = A1_count + sample[1]
                    D1_A1_count = D1_A1_count + sample[1]
                elif next_exon[0] == A2:
                    A2_count = A2_count + sample[1]
                    D1_A2_count = D1_A2_count + sample[1]
                elif next_exon[0] == A3:
                    A3_count = A3_count + sample[1]
                    D1_A3_count = D1_A3_count + sample[1]
                elif next_exon[0] == A4a:
                    A4a_count = A4a_count + sample[1]
                    D1_A4a_count = D1_A4a_count + sample[1]
                elif next_exon[0] == A4b:
                    A4b_count = A4b_count + sample[1]
                    D1_A4b_count = D1_A4b_count + sample[1]
                elif next_exon[0] == A4c:
                    A4c_count = A4c_count + sample[1]
                    D1_A4c_count = D1_A4c_count + sample[1]
                elif next_exon[0] == A5:
                    A5_count = A5_count + sample[1]
                    D1_A5_count = D1_A5_count + sample[1]
                elif next_exon[0] == A7:
                    A7_count = A7_count + sample[1]
                    D1_A7_count = D1_A7_count + sample[1]
                elif next_exon[0] == A7c:
                    A7c_count = A7c_count + sample[1]
                    D1_A7c_count = D1_A7c_count + sample[1]
                else:
                    if next_exon[0] > 700:
                        print (str(sample[0]) + " has an unknown acceptor. Exon = " + str(exon) )
            elif exon[1] == D2:
                D2_count = D2_count + sample[1]
                if next_exon[0] == A2:
                    A2_count = A2_count + sample[1]
                    D2_A2_count = D2_A2_count + sample[1]
                elif next_exon[0] == A3:
                    A3_count = A3_count + sample[1]
                    D2_A3_count = D2_A3_count + sample[1]
                elif next_exon[0] == A4a:
                    A4a_count = A4a_count + sample[1]
                    D2_A4a_count = D2_A4a_count + sample[1]
                elif next_exon[0] == A4b:
                    A4b_count = A4b_count + sample[1]
                    D2_A4b_count = D2_A4b_count + sample[1]
                elif next_exon[0] == A4c:
                    A4c_count = A4c_count + sample[1]
                    D2_A4c_count = D2_A4c_count + sample[1]
                elif next_exon[0] == A5:
                    A5_count = A5_count + sample[1]
                    D2_A5_count = D2_A5_count + sample[1]
                elif next_exon[0] == A7:
                    A7_count = A7_count + sample[1]
                    D2_A7_count = D2_A7_count + sample[1]
                elif next_exon[0] == A7c:
                    A7c_count = A7c_count + sample[1]
                    D2_A7c_count = D2_A7c_count + sample[1]
                else:
                    if next_exon[0] > 700:
                        print (str(sample[0]) + " has an unknown acceptor. Exon = " + str(exon) )
            elif exon[1] == D2b:
                D2b_count = D2b_count + sample[1]
                if next_exon[0] == A2:
                    A2_count = A2_count + sample[1]
                    D2b_A2_count = D2b_A2_count + sample[1]
                elif next_exon[0] == A3:
                    A3_count = A3_count + sample[1]
                    D2b_A3_count = D2b_A3_count + sample[1]
                elif next_exon[0] == A4a:
                    A4a_count = A4a_count + sample[1]
                    D2b_A4a_count = D2b_A4a_count + sample[1]
                elif next_exon[0] == A4b:
                    A4b_count = A4b_count + sample[1]
                    D2b_A4b_count = D2b_A4b_count + sample[1]
                elif next_exon[0] == A4c:
                    A4c_count = A4c_count + sample[1]
                    D2b_A4c_count = D2b_A4c_count + sample[1]
                elif next_exon[0] == A5:
                    A5_count = A5_count + sample[1]
                    D2b_A5_count = D2b_A5_count + sample[1]
                elif next_exon[0] == A7:
                    A7_count = A7_count + sample[1]
                    D2b_A7_count = D2b_A7_count + sample[1]
                elif next_exon[0] == A7c:
                    A7c_count = A7c_count + sample[1]
                    D2b_A7c_count = D2b_A7c_count + sample[1]
                else:
                    if next_exon[0] > 700:
                        print (str(sample[0]) + " has an unknown acceptor. Exon = " + str(exon) )
            elif exon[1] == D3:
                D3_count = D3_count + sample[1]
                if next_exon[0] == A3:
                    A3_count = A3_count + sample[1]
                    D3_A3_count = D3_A3_count + sample[1]
                elif next_exon[0] == A4a:
                    A4a_count = A4a_count + sample[1]
                    D3_A4a_count = D3_A4a_count + sample[1]
                elif next_exon[0] == A4b:
                    A4b_count = A4b_count + sample[1]
                    D3_A4b_count = D3_A4b_count + sample[1]
                elif next_exon[0] == A4c:
                    A4c_count = A4c_count + sample[1]
                    D3_A4c_count = D3_A4c_count + sample[1]
                elif next_exon[0] == A5:
                    A5_count = A5_count + sample[1]
                    D3_A5_count = D3_A5_count + sample[1]
                elif next_exon[0] == A7:
                    A7_count = A7_count + sample[1]
                    D3_A7_count = D3_A7_count + sample[1]
                elif next_exon[0] == A7c:
                    A7c_count = A7c_count + sample[1]
                    D3_A7c_count = D3_A7c_count + sample[1]
                else:
                    if next_exon[0] > 700:
                        print (str(sample[0]) + " has an unknown acceptor. Exon = " + str(exon) )
            elif exon[1] == D4:
                D4_count = D4_count + sample[1]
                if next_exon[0] == A7:
                    A7_count = A7_count + sample[1]
                    D4_A7_count = D4_A7_count + sample[1]
                elif next_exon[0] == A7c:
                    A7c_count = A7c_count + sample[1]
                    D4_A7c_count = D4_A7c_count + sample[1]
                else:
                    if next_exon[0] > 700:
                        print (str(sample[0]) + " has an unknown acceptor. Exon = " + str(exon) )
            else:
                if exon[1] < 8500:
                        print (str(sample[0]) + " has an unknown donor. Exon = " + str(exon) )
            exon_num = exon_num + 1
        splice_count = splice_count - sample[1]

    
    ##Write the final output files to working directory
    output_gtf = output_file + ".csv"
    output_pass = output_file + "_pass.txt"
    output_fail = output_file + "_fail.txt"
    output_altered = output_file + "_altered.txt"
    output_log = output_file + ".log"
    output_SS_usage = output_file + "_splice_site_usage.csv"
    output_isoform_calc = output_file + "_isoform_counts.csv"
    output_ref_coords = output_file + "_ref_coordinates.txt"
    
    #Write the csv file
    if NCE_option == "True" or NCE_option == "true" or NCE_option == "T" or NCE_option == "t":
        with open(output_gtf, 'w', newline='') as csvfile:
            fieldnames = ['transcript_id', 'cluster size', 'cmp_ref', 'start', 'end', 'class_code', 'exons', 'cov_len', 'sqrt cov_len', 'normalized counts', 'NCE2', 'NCE2b', 'NCE3', 'notes']
            writer = csv.DictWriter(csvfile, dialect = 'excel', fieldnames=fieldnames)
            writer.writeheader()
            for sample in final_list:
                if type(sample[6]) is list:
                    exons_as_string = ''
                    for exon in sample[6]:
                        exon_string = str(exon[0]) + '-' + str(exon[1]) + '/'
                        exons_as_string += exon_string
                    sample[6] = exons_as_string
                sample_dict = {"transcript_id":sample[0], 'cluster size':sample[1], 'cmp_ref':sample[2], 'start':sample[3], 'end':sample[4], 'class_code':sample[5], 'exons':sample[6], 'cov_len':sample[7], 'sqrt cov_len':sample[8], 'normalized counts':sample[9], 'NCE2':sample[10], 'NCE2b':sample[11], 'NCE3':sample[12], 'notes':sample[13]}
                writer.writerow(sample_dict)
    
    else:
        with open(output_gtf, 'w', newline='') as csvfile:
            fieldnames = ['transcript_id', 'cluster size', 'cmp_ref', 'start', 'end', 'class_code', 'exons', 'cov_len', 'sqrt cov_len', 'normalized counts', 'notes']
            writer = csv.DictWriter(csvfile, dialect = 'excel', fieldnames=fieldnames)
            writer.writeheader()
            for sample in final_list:
                if type(sample[6]) is list:
                    exons_as_string = ''
                    for exon in sample[6]:
                        exon_string = str(exon[0]) + '-' + str(exon[1]) + '/'
                        exons_as_string += exon_string
                    sample[6] = exons_as_string
                sample_dict = {"transcript_id":sample[0], 'cluster size':sample[1], 'cmp_ref':sample[2], 'start':sample[3], 'end':sample[4], 'class_code':sample[5], 'exons':sample[6], 'cov_len':sample[7], 'sqrt cov_len':sample[8], 'normalized counts':sample[9], 'notes':sample[10]}
                writer.writerow(sample_dict)
    #write text file of passing transcript IDs
    with open(output_pass,'w') as tfile:
        for sample in final_list:
            tfile.write(sample[0] +"\n")

    #write text file of failed transcript IDs        
    with open(output_fail,'w') as tfile:
        for sample in failed_list:
            tfile.write(sample[0] +"\n")
            
    #write text file of altered transcript IDs
    with open(output_altered,'w') as tfile:
        for sample in exons_altered_list:
            tfile.write(sample[0] +"\n")
            
    #write text file of running conditions 
    with open(output_log,'w') as tfile:
        tfile.write("input_file = " + input_file + "\n")
        tfile.write("output_file = " + output_file + "\n")
        tfile.write("ref_file = " + ref_file + "\n") 
        tfile.write("gap_tolerance = " + str(gap_tolerance) + "\n")
        tfile.write("min_end_bp = " + str(min_end_bp) + "\n")
        tfile.write("max_start_bp = " + str(max_start_bp) + "\n")
        tfile.write("min_FS_len = " + str(min_FS_len) + "\n")
        tfile.write("NCE_option = " + NCE_option + "\n")
        
    #write text file of reference coordinates 
    with open(output_ref_coords,'w') as tfile:
        tfile.write("D1 = " + str(D1) + "\n")
        tfile.write("D2 = " + str(D2) + "\n")
        tfile.write("D2b = " + str(D2b) + "\n") 
        tfile.write("D3 = " + str(D3) + "\n")
        tfile.write("D4 = " + str(D4) + "\n")
        tfile.write("A1 = " + str(A1) + "\n")
        tfile.write("A2 = " + str(A2) + "\n")
        tfile.write("A3 = " + str(A3) + "\n")
        tfile.write("A4a = " + str(A4a) + "\n")
        tfile.write("A4b = " + str(A4b) + "\n")
        tfile.write("A4c = " + str(A4c) + "\n")
        tfile.write("A5 = " + str(A5) + "\n")
        tfile.write("A7 = " + str(A7) + "\n")
        tfile.write("A7c = " + str(A7c) + "\n")
        tfile.write("Gag CDS = " + str(gag_CDS) + "\n")
        tfile.write("Pol CDS = " + str(pol_CDS) + "\n")
        tfile.write("Env CDS = " + str(env_CDS) + "\n")
        tfile.write("Rev CDS = " + str(rev_CDS1) + " and " + str(rev_CDS2) + "\n")
        tfile.write("Tat CDS = " + str(tat_CDS1) + " and " + str(tat_CDS2) + "\n")
        tfile.write("Vif CDS = " + str(vif_CDS) + "\n")
        tfile.write("Vpr CDS = " + str(vpr_CDS) + "\n")
        
    #write csv file of Splice Site Usage calculations   
    if splice_count != 0:
        with open(output_SS_usage, 'w', newline='') as csvfile:
            fieldnames = ['Splice site(s)', 'count', 'percent']
            writer = csv.DictWriter(csvfile, dialect = 'excel', fieldnames=fieldnames)
            writer.writeheader()
            D1_dict = {'Splice site(s)':"D1", 'count':str(D1_count), 'percent':(str(((D1_count/splice_count)*100)))}
            writer.writerow(D1_dict)
            D2_dict = {'Splice site(s)':"D2", 'count':str(D2_count), 'percent':(str(((D2_count/splice_count)*100)))}
            writer.writerow(D2_dict)
            D2b_dict = {'Splice site(s)':"D2b", 'count':str(D2b_count), 'percent':(str(((D2b_count/splice_count)*100)))}
            writer.writerow(D2b_dict)
            D3_dict = {'Splice site(s)':"D3", 'count':str(D3_count), 'percent':(str(((D3_count/splice_count)*100)))}
            writer.writerow(D3_dict)
            D4_dict = {'Splice site(s)':"D4", 'count':str(D4_count), 'percent':(str(((D4_count/splice_count)*100)))}
            writer.writerow(D4_dict)
            A1_dict = {'Splice site(s)':"A1", 'count':str(A1_count), 'percent':(str(((A1_count/splice_count)*100)))}
            writer.writerow(A1_dict)
            A2_dict = {'Splice site(s)':"A2", 'count':str(A2_count), 'percent':(str(((A2_count/splice_count)*100)))}
            writer.writerow(A2_dict)
            A3_dict = {'Splice site(s)':"A3", 'count':str(A3_count), 'percent':(str(((A3_count/splice_count)*100)))}
            writer.writerow(A3_dict)
            A4a_dict = {'Splice site(s)':"A4a", 'count':str(A4a_count), 'percent':(str(((A4a_count/splice_count)*100)))}
            writer.writerow(A4a_dict)
            A4b_dict = {'Splice site(s)':"A4b", 'count':str(A4b_count), 'percent':(str(((A4b_count/splice_count)*100)))}
            writer.writerow(A4b_dict)
            A4c_dict = {'Splice site(s)':"A4c", 'count':str(A4c_count), 'percent':(str(((A4c_count/splice_count)*100)))}
            writer.writerow(A4c_dict)
            A5_dict = {'Splice site(s)':"A5", 'count':str(A5_count), 'percent':(str(((A5_count/splice_count)*100)))}
            writer.writerow(A5_dict)
            A7_dict = {'Splice site(s)':"A7", 'count':str(A7_count), 'percent':(str(((A7_count/splice_count)*100)))}
            writer.writerow(A7_dict)
            A7c_dict = {'Splice site(s)':"A7c", 'count':str(A7c_count), 'percent':(str(((A7c_count/splice_count)*100)))}
            writer.writerow(A7c_dict)
            D1_A1_dict = {'Splice site(s)':"D1_A1", 'count':str(D1_A1_count), 'percent':(str(((D1_A1_count/splice_count)*100)))}
            writer.writerow(D1_A1_dict)
            D1_A2_dict = {'Splice site(s)':"D1_A2", 'count':str(D1_A2_count), 'percent':(str(((D1_A2_count/splice_count)*100)))}
            writer.writerow(D1_A2_dict)
            D1_A3_dict = {'Splice site(s)':"D1_A3", 'count':str(D1_A3_count), 'percent':(str(((D1_A3_count/splice_count)*100)))}
            writer.writerow(D1_A3_dict)
            D1_A4a_dict = {'Splice site(s)':"D1_A4a", 'count':str(D1_A4a_count), 'percent':(str(((D1_A4a_count/splice_count)*100)))}
            writer.writerow(D1_A4a_dict)
            D1_A4b_dict = {'Splice site(s)':"D1_A4b", 'count':str(D1_A4b_count), 'percent':(str(((D1_A4b_count/splice_count)*100)))}
            writer.writerow(D1_A4b_dict)
            D1_A4c_dict = {'Splice site(s)':"D1_A4c", 'count':str(D1_A4c_count), 'percent':(str(((D1_A4c_count/splice_count)*100)))}
            writer.writerow(D1_A4c_dict)
            D1_A5_dict = {'Splice site(s)':"D1_A5", 'count':str(D1_A5_count), 'percent':(str(((D1_A5_count/splice_count)*100)))}
            writer.writerow(D1_A5_dict)
            D1_A7_dict = {'Splice site(s)':"D1_A7", 'count':str(D1_A7_count), 'percent':(str(((D1_A7_count/splice_count)*100)))}
            writer.writerow(D1_A7_dict)
            D1_A7c_dict = {'Splice site(s)':"D1_A7c", 'count':str(D1_A7c_count), 'percent':(str(((D1_A7c_count/splice_count)*100)))}
            writer.writerow(D1_A7c_dict)
            D2_A2_dict = {'Splice site(s)':"D2_A2", 'count':str(D2_A2_count), 'percent':(str(((D2_A2_count/splice_count)*100)))}
            writer.writerow(D2_A2_dict)
            D2_A3_dict = {'Splice site(s)':"D2_A3", 'count':str(D2_A3_count), 'percent':(str(((D2_A3_count/splice_count)*100)))}
            writer.writerow(D2_A3_dict)
            D2_A4a_dict = {'Splice site(s)':"D2_A4a", 'count':str(D2_A4a_count), 'percent':(str(((D2_A4a_count/splice_count)*100)))}
            writer.writerow(D2_A4a_dict)
            D2_A4b_dict = {'Splice site(s)':"D2_A4b", 'count':str(D2_A4b_count), 'percent':(str(((D2_A4b_count/splice_count)*100)))}
            writer.writerow(D2_A4b_dict)
            D2_A4c_dict = {'Splice site(s)':"D2_A4c", 'count':str(D2_A4c_count), 'percent':(str(((D2_A4c_count/splice_count)*100)))}
            writer.writerow(D2_A4c_dict)
            D2_A5_dict = {'Splice site(s)':"D2_A5", 'count':str(D2_A5_count), 'percent':(str(((D2_A5_count/splice_count)*100)))}
            writer.writerow(D2_A5_dict)
            D2_A7_dict = {'Splice site(s)':"D2_A7", 'count':str(D2_A7_count), 'percent':(str(((D2_A7_count/splice_count)*100)))}
            writer.writerow(D2_A7_dict)
            D2_A7c_dict = {'Splice site(s)':"D2_A7c", 'count':str(D2_A7c_count), 'percent':(str(((D2_A7c_count/splice_count)*100)))}
            writer.writerow(D2_A7c_dict)
            D2b_A2_dict = {'Splice site(s)':"D2b_A2", 'count':str(D2b_A2_count), 'percent':(str(((D2b_A2_count/splice_count)*100)))}
            writer.writerow(D2b_A2_dict)
            D2b_A3_dict = {'Splice site(s)':"D2b_A3", 'count':str(D2b_A3_count), 'percent':(str(((D2b_A3_count/splice_count)*100)))}
            writer.writerow(D2b_A3_dict)
            D2b_A4a_dict = {'Splice site(s)':"D2b_A4a", 'count':str(D2b_A4a_count), 'percent':(str(((D2b_A4a_count/splice_count)*100)))}
            writer.writerow(D2b_A4a_dict)
            D2b_A4b_dict = {'Splice site(s)':"D2b_A4b", 'count':str(D2b_A4b_count), 'percent':(str(((D2b_A4b_count/splice_count)*100)))}
            writer.writerow(D2b_A4b_dict)
            D2b_A4c_dict = {'Splice site(s)':"D2b_A4c", 'count':str(D2b_A4c_count), 'percent':(str(((D2b_A4c_count/splice_count)*100)))}
            writer.writerow(D2b_A4c_dict)
            D2b_A5_dict = {'Splice site(s)':"D2b_A5", 'count':str(D2b_A5_count), 'percent':(str(((D2b_A5_count/splice_count)*100)))}
            writer.writerow(D2b_A5_dict)
            D2b_A7_dict = {'Splice site(s)':"D2b_A7", 'count':str(D2b_A7_count), 'percent':(str(((D2b_A7_count/splice_count)*100)))}
            writer.writerow(D2b_A7_dict)
            D2b_A7c_dict = {'Splice site(s)':"D2b_A7c", 'count':str(D2b_A7c_count), 'percent':(str(((D2b_A7c_count/splice_count)*100)))}
            writer.writerow(D2b_A7c_dict)
            D3_A3_dict = {'Splice site(s)':"D3_A3", 'count':str(D3_A3_count), 'percent':(str(((D3_A3_count/splice_count)*100)))}
            writer.writerow(D3_A3_dict)
            D3_A4a_dict = {'Splice site(s)':"D3_A4a", 'count':str(D3_A4a_count), 'percent':(str(((D3_A4a_count/splice_count)*100)))}
            writer.writerow(D3_A4a_dict)
            D3_A4b_dict = {'Splice site(s)':"D3_A4b", 'count':str(D3_A4b_count), 'percent':(str(((D3_A4b_count/splice_count)*100)))}
            writer.writerow(D3_A4b_dict)
            D3_A4c_dict = {'Splice site(s)':"D3_A4c", 'count':str(D3_A4c_count), 'percent':(str(((D3_A4c_count/splice_count)*100)))}
            writer.writerow(D3_A4c_dict)
            D3_A5_dict = {'Splice site(s)':"D3_A5", 'count':str(D3_A5_count), 'percent':(str(((D3_A5_count/splice_count)*100)))}
            writer.writerow(D3_A5_dict)
            D3_A7_dict = {'Splice site(s)':"D3_A7", 'count':str(D3_A7_count), 'percent':(str(((D3_A7_count/splice_count)*100)))}
            writer.writerow(D3_A7_dict)
            D3_A7c_dict = {'Splice site(s)':"D3_A7c", 'count':str(D3_A7c_count), 'percent':(str(((D3_A7c_count/splice_count)*100)))}
            writer.writerow(D3_A7c_dict)
            D4_A7_dict = {'Splice site(s)':"D4_A7", 'count':str(D4_A7_count), 'percent':(str(((D4_A7_count/splice_count)*100)))}
            writer.writerow(D4_A7_dict)
            D4_A7c_dict = {'Splice site(s)':"D4_A7c", 'count':str(D4_A7c_count), 'percent':(str(((D4_A7c_count/splice_count)*100)))}
            writer.writerow(D4_A7c_dict)

    #write csv file of Isoform Usage calculations         
    with open(output_isoform_calc, 'w', newline='') as csvfile:
            fieldnames = ['Isoform', 'Size Normalized Count', 'percent']
            writer = csv.DictWriter(csvfile, dialect = 'excel', fieldnames=fieldnames)
            writer.writeheader()
            env_dict = {'Isoform':"Env", 'Size Normalized Count':str(env_count), 'percent':(str(((env_count/total_norm_count)*100)))}
            writer.writerow(env_dict)
            envA4a_dict = {'Isoform':"Env-A4a", 'Size Normalized Count':str(envA4a_count), 'percent':(str(((envA4a_count/total_norm_count)*100)))}
            writer.writerow(envA4a_dict)
            envA4b_dict = {'Isoform':"Env-A4b", 'Size Normalized Count':str(envA4b_count), 'percent':(str(((envA4b_count/total_norm_count)*100)))}
            writer.writerow(envA4b_dict)
            envA4c_dict = {'Isoform':"Env-A4c", 'Size Normalized Count':str(envA4c_count), 'percent':(str(((envA4c_count/total_norm_count)*100)))}
            writer.writerow(envA4c_dict)
            nef_dict = {'Isoform':"Nef", 'Size Normalized Count':str(nef_count), 'percent':(str(((nef_count/total_norm_count)*100)))}
            writer.writerow(nef_dict)
            revA4a_dict = {'Isoform':"Rev-A4a", 'Size Normalized Count':str(revA4a_count), 'percent':(str(((revA4a_count/total_norm_count)*100)))}
            writer.writerow(revA4a_dict)
            revA4b_dict = {'Isoform':"Rev-A4b", 'Size Normalized Count':str(revA4b_count), 'percent':(str(((revA4b_count/total_norm_count)*100)))}
            writer.writerow(revA4b_dict)
            revA4c_dict = {'Isoform':"Rev-A4c", 'Size Normalized Count':str(revA4c_count), 'percent':(str(((revA4c_count/total_norm_count)*100)))}
            writer.writerow(revA4c_dict)
            tat_dict = {'Isoform':"Tat", 'Size Normalized Count':str(tat_count), 'percent':(str(((tat_count/total_norm_count)*100)))}
            writer.writerow(tat_dict)
            tat_unspliced_dict = {'Isoform':"Tat-unspliced", 'Size Normalized Count':str(tat_unspliced_count), 'percent':(str(((tat_unspliced_count/total_norm_count)*100)))}
            writer.writerow(tat_unspliced_dict)
            vif_dict = {'Isoform':"Vif", 'Size Normalized Count':str(vif_count), 'percent':(str(((vif_count/total_norm_count)*100)))}
            writer.writerow(vif_dict)
            vpr_dict = {'Isoform':"Vpr", 'Size Normalized Count':str(vpr_count), 'percent':(str(((vpr_count/total_norm_count)*100)))}
            writer.writerow(vpr_dict)

    print ("Complete")
   



























