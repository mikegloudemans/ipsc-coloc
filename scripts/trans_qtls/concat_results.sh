###########################################
# Coloc results for stuff from Marc
###########################################


# Concatenate all results to tmp file
rm /users/mgloud/projects/ipsc/output/ipsc_trans_tests_errors.txt
rm /users/mgloud/projects/ipsc/output/ipsc_trans_tests_skipped.txt
rm /users/mgloud/projects/ipsc/tmp/full_ipsc_trans_coloc_results.tmp
mkdir /users/mgloud/projects/ipsc/output/trans-plots
for f in `ls /users/mgloud/projects/brain_gwas/output/ipsc-trans-tests`; do
	file=`ls -1 /users/mgloud/projects/brain_gwas/output/ipsc-trans-tests/$f/*clpp* | head -n 1`
	cat $file | tail -n +2 >> /users/mgloud/projects/ipsc/tmp/full_ipsc_trans_coloc_results.tmp

	cat /users/mgloud/projects/brain_gwas/output/ipsc-trans-tests/$f/ERROR_variants.txt >> /users/mgloud/projects/ipsc/output/ipsc_trans_tests_errors.txt 2> /dev/null
	cat /users/mgloud/projects/brain_gwas/output/ipsc-trans-tests/$f/skipped_variants.txt >> /users/mgloud/projects/ipsc/output/ipsc_trans_tests_skipped.txt 2> /dev/null

	# Also copy the plots to a combined folder
	cp -r /users/mgloud/projects/brain_gwas/output/ipsc-trans-tests/$f/plots/* /users/mgloud/projects/ipsc/output/trans-plots 2> /dev/null
done

# Write header for sorted output file
cat $file | head -n 1 > /users/mgloud/projects/ipsc/output/full_ipsc_trans_coloc_results.txt

# Sort tmp file and add to sorted output file
sort -k6,6gr /users/mgloud/projects/ipsc/tmp/full_ipsc_trans_coloc_results.tmp >> /users/mgloud/projects/ipsc/output/full_ipsc_trans_coloc_results.txt
rm /users/mgloud/projects/ipsc/tmp/full_ipsc_trans_coloc_results.tmp

awk '{if ($5 > 50) print $0}' /users/mgloud/projects/ipsc/output/full_ipsc_trans_coloc_results.txt > /users/mgloud/projects/ipsc/output/full_ipsc_trans_coloc_results_snp_thresholded.txt
awk '{if (($5 > 50) && ($7 >= 5)) print $0}' /users/mgloud/projects/ipsc/output/full_ipsc_trans_coloc_results.txt > /users/mgloud/projects/ipsc/output/full_ipsc_trans_coloc_results_snp_and_gwas_thresholded.txt
awk '{if ($7 >= 5) print $0}' /users/mgloud/projects/ipsc/output/full_ipsc_trans_coloc_results.txt > /users/mgloud/projects/ipsc/output/full_ipsc_trans_coloc_results_gwas_threshold.txt
