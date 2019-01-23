#!/usr/bin/python
# Author: Mike Gloudemans
# Date created: 6/7/2018

# Print key attributes about GWAS, that we can use to select best GWAS
# (May also be useful for others in lab to make this table and post)

import glob
import gzip
import subprocess
import sys
import operator
import pandas as pd
sys.path.insert(0, '/users/mgloud/projects/brain_gwas/scripts')
import SNP 

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

from scipy import stats

phenos = ["/users/mgloud/projects/ipsc/data/Input/ApaLevel/full_qtl_results_formatted.txt.gz",
        "/users/mgloud/projects/ipsc/data/Input/GeneLevel/full_qtl_results_formatted.txt.gz",
        "/users/mgloud/projects/ipsc/data/Input/ExonLevel/full_qtl_results_formatted.txt.gz",
        "/users/mgloud/projects/ipsc/data/Input/SplicingLevel/full_qtl_results_formatted.txt.gz",
        "/users/mgloud/projects/ipsc/data/Input/TranscriptRatio/full_qtl_results_formatted.txt.gz"]

def main():

    cutoffs = get_fdr_cutoffs(phenos)
    
    files = glob.glob("/mnt/lab_data/montgomery/mgloud/gwas/data/munged/*.gz")

    # Write header
    with open("/users/mgloud/projects/ipsc/output/snps_to_test_locuscompare_fdr05_window10000.txt", "w") as w:
        w.write("chr\tsnp_pos\tgwas_file\teqtl_file\ttrait\tgwas_pvalue\teqtl_pvalue\tgene\n")

    for file in sorted(files):

        info = snps_by_threshold(file, 5e-8, file)

        for snp in info:
            print snp

            for pheno in phenos:
              
                wide_matches = subprocess.check_output("tabix {0} {1}:{2}-{3}".format(pheno, snp[0], snp[1]-10000, snp[1]+10000), shell=True)
                if wide_matches.strip() == "":
                    continue
                wide_matches = wide_matches.strip().split("\n")

                matched_05 = set([])     # Don't print repeats if there are multiple matches
                for match in wide_matches:
                    data = match.strip().split("\t")
                    if float(data[7]) <= cutoffs[0][pheno] and data[0] not in matched_05:
                        with open("/users/mgloud/projects/ipsc/output/snps_to_test_locuscompare_fdr05_window10000.txt", "a") as a:
                            a.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(snp[0], snp[1], file, pheno, snp[3], snp[2], data[7], data[0]))
                            matched_05.add(data[0])

def snps_by_threshold(gwas_file, gwas_threshold, trait, window=1000000):

    snp_counts = {}
    hit_counts = {}

    with gzip.open(gwas_file) as f:
        header = f.readline().strip().split()

        trait_index = -1
        pval_index = header.index("pvalue")
        chr_index = header.index("chr")
        snp_pos_index = header.index("snp_pos")

        all_snps = []

        #i = 0
        for line in f:
            #i += 1
            #if i > 1000000:
            #    break
            data = line.strip().split("\t")
            if trait_index != -1:
                trait = data[trait_index]
            try:
                pvalue = float(data[pval_index])
            except:
                continue
            chr = data[chr_index]
            pos = int(data[snp_pos_index])
            snp_counts[trait] = snp_counts.get(trait, 0) + 1
            if pvalue > gwas_threshold:
                continue

            all_snps.append((chr, pos, pvalue, trait))
    
    # For now, include only autosomal SNPs.
    filtered = []
    for s in all_snps:
        if "chr" in str(s[0]):
            filtered.append((s[0][3:], s[1], s[2], s[3]))
        else:
            filtered.append((s[0], s[1], s[2], s[3]))

    all_snps = sorted(filtered, key=operator.itemgetter(2)) 

    # Go through the list of SNPs in order, adding the ones
    # passing our criteria.
    snps_to_test = []
    for snp in all_snps:

        # For now, ignore a SNP if it's in the MHC region -- this
        # would require alternative methods.
        if (snp[0] == "6") and snp[1] > 25000000 and snp[1] < 35000000:
                continue

        # Before adding a SNP, make sure it's not right next
        # to another SNP that we've already selected.
        skip = False
        for kept_snp in snps_to_test:
                if kept_snp[0] == snp[0] and abs(kept_snp[1] - snp[1]) < window and kept_snp[3] == snp[3]:
                        skip = True
                        break
        if not skip:
            snps_to_test.append(snp)
            
    return(snps_to_test)

def get_fdr_cutoffs(pheno_files):

    perc_5_cutoffs = {}
    perc_1_cutoffs = {}

    for filename in pheno_files:
        fdr_file = "/".join(filename.split("/")[:-1] + ["PvalueThresholds.txt"])

        with open(fdr_file) as f:
           perc_5_cutoffs[filename] = float(f.readline().strip().split()[2])
           perc_1_cutoffs[filename] = float(f.readline().strip().split()[2])

    return (perc_5_cutoffs, perc_1_cutoffs)
            
if __name__ == "__main__":
    main()
                

