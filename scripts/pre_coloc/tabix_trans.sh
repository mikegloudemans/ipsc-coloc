echo -e "gene\tsnp_pos\tchr\tbeta\tse\tref\talt\tpvalue" > data/trans_eqtl/full/ipsc_trans_eqtl_sorted.txt

for f in `ls data/trans_eqtl/*.txt`; do
	echo $f
	tail -n +2 $f >> data/trans_eqtl/full/ipsc_trans_eqtl_combined.txt

	bgzip -f $f
	tabix -f -S 1 -s 3 -b 2 -e 2 $f.gz
done


sort -k3,3 -k2,2n data/trans_eqtl/full/ipsc_trans_eqtl_combined.txt | uniq >> data/trans_eqtl/full/ipsc_trans_eqtl_sorted.txt
bgzip -f data/trans_eqtl/full/ipsc_trans_eqtl_sorted.txt
tabix -f -S 1 -s 3 -b 2 -e 2 data/trans_eqtl/full/ipsc_trans_eqtl_sorted.txt.gz
rm data/trans_eqtl/full/ipsc_trans_eqtl_combined.txt
