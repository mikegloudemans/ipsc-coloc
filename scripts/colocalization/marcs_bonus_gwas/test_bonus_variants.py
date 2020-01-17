import operator
import subprocess
import json
import sys
import time
import datetime
import glob

def main():

    results_output_dir = "output/colocalization/raw_results/ipsc-bonus-finemap-results/"

    # Move old results to a new, time-stamped directory, so we're not mixing results
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
    # Directory we're moving the old results to
    old_results_dir = "output/colocalization/old_raw_results/ipsc-bonus-finemap-results/{0}".format(timestamp)
    subprocess_check_call("mkdir -p {0}".format(old_results_dir)
    subprocess.check_call("mv {1}/* {0}".format(old_results_dir, results_output_dir), shell=True)

    kept_data = []
    for g in glob.glob("output/test-snps/ipsc_marcs_extra_*_gwas-pval*_eqtl-pval*_gwas-window*_eqtl-window*_coloc-tests.txt"):
        with open(g) as f:
            f.readline()
            for line in f:
                data = line.strip().split()
                kept_data.append(data)

    kept_data = sorted(kept_data, key=operator.itemgetter(2))

    # Then for every locus in the "kept data"...
    for i in range(len(kept_data)):

        test = kept_data[i]
        print test
        
        temp = json.loads(template)
        temp["snp_list_file"] = "tmp/snp_list{0}.txt".format(i)
        temp["out_dir"] = results_output_dir

        # Add locus to SNP list...but only once for each gene
        with open("tmp/snp_list{0}.txt".format(i), "w") as w:
            w.write("{0}\t{1}\t{2}\n".format(test[0], test[1], test[7]))
               
        # Add corresponding gwas experiment to the list, if not already present
        temp["gwas_experiments"][test[2]] = {"ref": "1kgenomes", "gwas_format": "effect_size"}
        if test[2] != test[4]:
            temp["gwas_experiments"][test[2]]["traits"] = [test[4]]

        # Add corresponding eQTL tissue to the list
        temp["eqtl_experiments"][test[3]] = {"ref": "1kgenomes", "eqtl_format": "effect_size"}

        # Write config file to the appropriate directory
        with open("tmp/ipsc_config{0}.config".format(i), "w") as w:
            json.dump(temp, w)

        # Run the test
        subprocess.call("python bin/colocalization_pipeline/dispatch.py tmp/ipsc_config{0}.config 1 &".format(i), shell=True)

        while int(subprocess.check_output('''ps -ef | grep "python bin/colocalization_pipeline/dispatch.py tmp/ipsc_config" | wc -l''', shell=True)) > 3:
            time.sleep(5)

# All other settings and parameters will be added at runtime
template = '''
{
	"eqtl_threshold": 
		1,

	"selection_basis": 
		"snps_from_list",

	"methods": 
	{
		"finemap":{}
	},

        "ref_genomes": 
	{
		"1kgenomes": 
		{
			"file": 
				"data/1KG/ALL.chr{0}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",

                	"af_attribute": 
				"AF",

                        "N": 
				2504
	        }
        }
}
'''

if __name__ == "__main__":
    main()
