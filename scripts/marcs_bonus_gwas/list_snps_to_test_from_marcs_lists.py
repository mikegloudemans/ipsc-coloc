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

def main():

    # First, load names and genomic locations of all significant features
    sig_features = load_significant_features()

    files = glob.glob("/users/mgloud/projects/ipsc/data/marcs_gwas_files/reformatted/GWAS_Catalog/*.gz")
    files += glob.glob("/users/mgloud/projects/ipsc/data/marcs_gwas_files/reformatted/PhenomeScanner/*.gz")

    with open("/users/mgloud/projects/ipsc/output/snps_to_test_marcs_bonus.txt", "w") as w:

        w.write("chr\tsnp_pos\tgwas_file\teqtl_file\ttrait\tgwas_pvalue\tfeature\n")
        w.flush()

        for file in sorted(files):

            info = snps_by_threshold(file, 5e-8, file)

            for snp in info:

                if snp[0] not in sig_features:
                    continue
                print snp
                for feat in sig_features[snp[0]]:

                    if snp[1] <= feat[2] + 500000 and snp[1] >= feat[1] - 500000:
                        w.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format(snp[0], snp[1], file, feat[3], snp[3], snp[2], feat[0]))
                        w.flush()


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

def load_all_features(filename):
    all_features = {}
    with open(filename) as f:
        f.readline()
        for line in f:
            data = line.strip().split()
            all_features[data[0]] = (data[1], float(data[2]), float(data[3]))

    return all_features

def load_significant_features():
    sig_files = [("/users/mgloud/projects/ipsc/data/Input/apa_affectedFeatures.txt", "/users/mgloud/projects/ipsc/data/Input/ApaLevel/APA_QTL_annot.txt"),
                ("/users/mgloud/projects/ipsc/data/Input/exon_affectedFeatures.txt", "/users/mgloud/projects/ipsc/data/Input/ExonLevel/Exons_mapping.txt"),
                ("/users/mgloud/projects/ipsc/data/Input/gene_affectedFeatures.txt", "/users/mgloud/projects/ipsc/data/Input/GeneLevel/Annotation_FC_Gene.txt"),
                ("/users/mgloud/projects/ipsc/data/Input/Splicing_affectedFeatures.txt", "/users/mgloud/projects/ipsc/data/Input/SplicingLevel/SplicingFractionMatrixMapping.txt"),
                ("/users/mgloud/projects/ipsc/data/Input/transcript_affectedFeatures.txt", "/users/mgloud/projects/ipsc/data/Input/TranscriptRatio/TranscriptMapping.txt")]

    sig_features = {}
    for sf in sig_files:
        all_features = load_all_features(sf[1])
        with open(sf[0]) as f:
            f.readline()
            for line in f:
                feat = all_features[line.strip()]
                if str(feat[0]) not in sig_features:
                    sig_features[str(feat[0])] = []
                sig_features[str(feat[0])].append((line.strip(), feat[1], feat[2], sf[1]))

    return sig_features


        
if __name__ == "__main__":
    main()
