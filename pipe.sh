# Author: Mike Gloudemans

# Full pipeline for running iPSC QTL colocalization analysis

# NOTE: This script MUST be run from the top-level directory of the project
# where it is located, because it and all the helper scripts use paths relative to this location.

########################################
# Preprocessing
########################################

# TODO: Make all directories that will be used by these scripts
# but aren't automatically created with git clone
mkdir -p tmp
mkdir -p output/test-snps

# Re-format data files properly for
# running colocalization analysis
python scripts/pre_coloc/sort_and_tabix_eqtl.py
python scripts/pre_coloc/sort_and_tabix_gwas.py
bash scripts/pre_coloc/tabix_trans.sh

# TODO: Get and munge SNPs

# Munge the ones specifically for immune-GWAS analysis

# Make a list of which SNPs we'll be testing (together for all three file categories)
python bin/gwas-download/overlap/list_snps_to_test.py scripts/pre_coloc/overlap/all_snp_overlap.overlap.config

########################################
# Colocalization
########################################

# Run colocalization for all GWAS sets,
# one batch at a time
bash scripts/colocalization/test_all_variant_sets.sh

########################################
# Post-processing
########################################

# Concatenate results into a single file,
# and filter them
bash scripts/post_coloc/format_results.sh

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
bash scripts/auxiliary/justify_exon_name_trimming.sh
