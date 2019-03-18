# Justify using first 100 characters of exon names, by showing that the first exon (comma-separated) is unique

mgloud@durga:/users/mgloud/projects/ipsc/output$ cut -f8,8 snps_to_test_locuscompare_fdr05_window10000.txt | grep ENSE | sort | uniq | wc -l
13249
mgloud@durga:/users/mgloud/projects/ipsc/output$ cut -f8,8 snps_to_test_locuscompare_fdr05_window10000.txt | grep ENSE | cut -f1,1 -d"," | sort | uniq | wc -l
13249

