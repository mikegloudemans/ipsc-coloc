# Author: Mike Gloudemans

# Full pipeline for running iPSC QTL colocalization analysis

########################################
# Preprocessing
########################################

# Re-format data files properly for
# running colocalization analysis
python pre_coloc/sort_and_tabix_eqtl.py
python pre_coloc/sort_and_tabix_gwas.py

# Make a list of which SNPs we'll be testing (together for all three file categories)
python ../bin/gwas-download/list_snps_to_test.py pre_coloc/overlap/all_snp_overlap.overlap.config

########################################
# Colocalization
########################################

# Run colocalization for all GWAS sets,
# one batch at a time
bash colocalization/test_all_variant_sets.sh

########################################
# Post-processing
########################################

# Concatenate results into a single file,
# and filter them
bash post_coloc/format_results.sh

########################################
# Sanity checking steps that were not
# directly involved in producing results
########################################

# Is it OK to trim exon names in coloc analysis,
# since some are too long to be file names?
#
# Specifically, will it produce overlapping
# files from originally different exons?
#
# Answer: It's OK to do, no collisions
bash auxiliary/justify_exon_name_trimming.sh
