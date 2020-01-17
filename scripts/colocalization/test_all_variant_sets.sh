# General parameters
results_base_dir='../output/colocalization/raw_results/'
old_results_new_dir='../output/colocalization/old_raw_results/'
max_threads=3

# Run only test one set at a time

bonus_specific_results_dir='ipsc-bonus-finemap-results'
bonus_overlap_snps='ipsc_marcs_extra*coloc-tests.txt'
python scripts/colocalization/test_variants_general.py $results_base_dir $bonus_specific_results_dir $old_results_new_dir $bonus_overlap_snps $max_threads

locuscompare_specific_results_dir='ipsc-locuscompare-finemap-results'
locuscompare_overlap_snps='ipsc_locus_compare*coloc-tests.txt'
python scripts/colocalization/test_variants_general.py $results_base_dir $locus_compare_specific_results_dir $old_results_new_dir $locuscompare_overlap_snps $max_threads

ukbb_specific_results_dir='ipsc-ukbb-finemap-results'
ukbb_overlap_snps='ipsc_ukbb*coloc-tests.txt'
python scripts/colocalization/test_variants_general.py $results_base_dir $ukbb_specific_results_dir $old_results_new_dir $ukbb_overlap_snps $max_threads

trans_specific_results_dir='ipsc-trans-finemap-results'
trans_overlap_snps='ipsc_trans*coloc-tests.txt'
python scripts/colocalization/test_variants_general.py $results_base_dir $trans_specific_results_dir $old_results_new_dir $trans_overlap_snps $max_threads

python trans_qtls/test_trans_qtl_variants.py

