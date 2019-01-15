cat /users/mgloud/projects/brain_gwas/output/ipsc-tests/*/*clpp* | head -n 1 > /users/mgloud/projects/ipsc/output/full_ipsc_coloc_results.txt
cat /users/mgloud/projects/brain_gwas/output/ipsc-tests/*/*clpp* | sort -k6,6gr | grep -v feature >> /users/mgloud/projects/ipsc/output/full_ipsc_coloc_results.txt

cat /users/mgloud/projects/brain_gwas/output/ipsc-ukbb-tests/*/*clpp* | head -n 1 > /users/mgloud/projects/ipsc/output/full_ukbb_ipsc_coloc_results.txt
cat /users/mgloud/projects/brain_gwas/output/ipsc-ukbb-tests/*/*clpp* | sort -k6,6gr | grep -v feature >> /users/mgloud/projects/ipsc/output/full_ukbb_ipsc_coloc_results.txt

cp -r /users/mgloud/projects/brain_gwas/output/ipsc-tests/*/plots/* /users/mgloud/projects/ipsc/output/plots
cp -r /users/mgloud/projects/brain_gwas/output/ipsc-ukbb-tests/*/plots/* /users/mgloud/projects/ipsc/output/ukbb-plots
