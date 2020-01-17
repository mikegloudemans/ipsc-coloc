bonus_coloc_results_dir=''
locuscompare_coloc_results_dir=''
ukbb_coloc_results_dir=''

###########################################
# Coloc results for stuff from Marc
###########################################

# Concatenate all results to tmp file
rm /users/mgloud/projects/ipsc/output/ipsc_bonus_tests_errors.txt
rm /users/mgloud/projects/ipsc/output/ipsc_bonus_tests_skipped.txt
rm /users/mgloud/projects/ipsc/tmp/full_ipsc_bonus_coloc_results.tmp
mkdir /users/mgloud/projects/ipsc/output/bonus-plots
for f in `ls /users/mgloud/projects/brain_gwas/output/ipsc-bonus-tests`; do
	file=`ls -1 /users/mgloud/projects/brain_gwas/output/ipsc-bonus-tests/$f/*clpp* | head -n 1`
	cat $file | tail -n +2 >> /users/mgloud/projects/ipsc/tmp/full_ipsc_bonus_coloc_results.tmp

	cat /users/mgloud/projects/brain_gwas/output/ipsc-bonus-tests/$f/ERROR_variants.txt >> /users/mgloud/projects/ipsc/output/ipsc_bonus_tests_errors.txt 2> /dev/null
	cat /users/mgloud/projects/brain_gwas/output/ipsc-bonus-tests/$f/skipped_variants.txt >> /users/mgloud/projects/ipsc/output/ipsc_bonus_tests_skipped.txt 2> /dev/null
	file=`ls -1 /users/mgloud/projects/brain_gwas/output/ipsc-bonus-tests/$f/*clpp* | head -n 1`

	# Also copy the plots to a combined folder
	cp -r /users/mgloud/projects/brain_gwas/output/ipsc-bonus-tests/$f/plots/* /users/mgloud/projects/ipsc/output/bonus-plots 2> /dev/null
done

# Write header for sorted output file
cat $file | head -n 1 > /users/mgloud/projects/ipsc/output/full_ipsc_bonus_coloc_results.txt

# Sort tmp file and add to sorted output file
sort -k6,6gr /users/mgloud/projects/ipsc/tmp/full_ipsc_bonus_coloc_results.tmp >> /users/mgloud/projects/ipsc/output/full_ipsc_bonus_coloc_results.txt
rm /users/mgloud/projects/ipsc/tmp/full_ipsc_bonus_coloc_results.tmp

awk '{if ($5 > 50) print $0}' /users/mgloud/projects/ipsc/output/full_ipsc_bonus_coloc_results.txt > /users/mgloud/projects/ipsc/output/full_ipsc_bonus_coloc_results_snp_thresholded.txt


###########################################
# Coloc results for LocusCompare files
###########################################


# Concatenate all results to tmp file
rm /users/mgloud/projects/ipsc/output/ipsc_locuscompare_tests_errors.txt
rm /users/mgloud/projects/ipsc/output/ipsc_locuscompare_tests_skipped.txt
rm /users/mgloud/projects/ipsc/tmp/full_ipsc_locuscompare_coloc_results.tmp
mkdir /users/mgloud/projects/ipsc/output/locuscompare-plots
for f in `ls /users/mgloud/projects/brain_gwas/output/ipsc-locuscompare-tests`; do
	file=`ls -1 /users/mgloud/projects/brain_gwas/output/ipsc-locuscompare-tests/$f/*clpp* | head -n 1`
	cat $file | tail -n +2 >> /users/mgloud/projects/ipsc/tmp/full_ipsc_locuscompare_coloc_results.tmp

	cat /users/mgloud/projects/brain_gwas/output/ipsc-locuscompare-tests/$f/ERROR_variants.txt >> /users/mgloud/projects/ipsc/output/ipsc_locuscompare_tests_errors.txt 2> /dev/null
	cat /users/mgloud/projects/brain_gwas/output/ipsc-locuscompare-tests/$f/skipped_variants.txt >> /users/mgloud/projects/ipsc/output/ipsc_locuscompare_tests_skipped.txt 2> /dev/null
	file=`ls -1 /users/mgloud/projects/brain_gwas/output/ipsc-locuscompare-tests/$f/*clpp* | head -n 1`

	# Also copy the plots to a combined folder
	cp -r /users/mgloud/projects/brain_gwas/output/ipsc-locuscompare-tests/$f/plots/* /users/mgloud/projects/ipsc/output/locuscompare-plots 2> /dev/null
done

# Write header for sorted output file
cat $file | head -n 1 > /users/mgloud/projects/ipsc/output/full_ipsc_locuscompare_coloc_results.txt

# Sort tmp file and add to sorted output file
sort -k6,6gr /users/mgloud/projects/ipsc/tmp/full_ipsc_locuscompare_coloc_results.tmp >> /users/mgloud/projects/ipsc/output/full_ipsc_locuscompare_coloc_results.txt
rm /users/mgloud/projects/ipsc/tmp/full_ipsc_locuscompare_coloc_results.tmp

awk '{if ($5 > 50) print $0}' /users/mgloud/projects/ipsc/output/full_ipsc_locuscompare_coloc_results.txt > /users/mgloud/projects/ipsc/output/full_ipsc_locuscompare_coloc_results_snp_thresholded.txt

############################################
# Coloc results for UKBB files
###########################################

# Concatenate all results to tmp file
rm /users/mgloud/projects/ipsc/output/ipsc_ukbb_tests_errors.txt
rm /users/mgloud/projects/ipsc/output/ipsc_ukbb_tests_skipped.txt
rm /users/mgloud/projects/ipsc/tmp/full_ipsc_ukbb_coloc_results.tmp
mkdir /users/mgloud/projects/ipsc/output/ukbb-plots
for f in `ls /users/mgloud/projects/brain_gwas/output/ipsc-ukbb-tests`; do
	file=`ls -1 /users/mgloud/projects/brain_gwas/output/ipsc-ukbb-tests/$f/*clpp* | head -n 1`
	cat $file | tail -n +2 >> /users/mgloud/projects/ipsc/tmp/full_ipsc_ukbb_coloc_results.tmp

	cat /users/mgloud/projects/brain_gwas/output/ipsc-ukbb-tests/$f/ERROR_variants.txt >> /users/mgloud/projects/ipsc/output/ipsc_ukbb_tests_errors.txt 2> /dev/null
	cat /users/mgloud/projects/brain_gwas/output/ipsc-ukbb-tests/$f/skipped_variants.txt >> /users/mgloud/projects/ipsc/output/ipsc_ukbb_tests_skipped.txt 2> /dev/null
	file=`ls -1 /users/mgloud/projects/brain_gwas/output/ipsc-ukbb-tests/$f/*clpp* | head -n 1`

	# Also copy the plots to a combined folder
	cp -r /users/mgloud/projects/brain_gwas/output/ipsc-ukbb-tests/$f/plots/* /users/mgloud/projects/ipsc/output/ukbb-plots 2> /dev/null
done

# Write header for sorted output file
cat $file | head -n 1 > /users/mgloud/projects/ipsc/output/full_ipsc_ukbb_coloc_results.txt

# Sort tmp file and add to sorted output file
sort -k6,6gr /users/mgloud/projects/ipsc/tmp/full_ipsc_ukbb_coloc_results.tmp >> /users/mgloud/projects/ipsc/output/full_ipsc_ukbb_coloc_results.txt
rm /users/mgloud/projects/ipsc/tmp/full_ipsc_ukbb_coloc_results.tmp

awk '{if ($5 > 50) print $0}' /users/mgloud/projects/ipsc/output/full_ipsc_ukbb_coloc_results.txt > /users/mgloud/projects/ipsc/output/full_ipsc_ukbb_coloc_results_snp_thresholded.txt
