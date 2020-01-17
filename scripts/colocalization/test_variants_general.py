import operator
import subprocess
import json
import sys
import time
import datetime
import glob


def main():

    # Get user-specified parameters
    results_base_dir = sys.argv[1]
    # "output/colocalization/raw_results/"
    results_specific_dir = sys.argv[2]
    # "ipsc-bonus-finemap-results/"
    old_results_new_dir = sys.argv[3]
    # "output/colocalization/old_raw_results/"
    snp_overlap_list = sys.argv[4]
    # "output/test-snps/ipsc_marcs_extra_*_gwas-pval*_eqtl-pval*_gwas-window*_eqtl-window*_coloc-tests.txt"
    max_threads = int(sys.argv[5])
    # 3
 
    results_dir = results_base_dir + "/" + results_specific_dir

    old_results_dir = old_results_new_dir + "/" + results_specific_dir
    
    # Move old results to a new, time-stamped directory, so we're not mixing results
    # TODO: Make it possible to override this step if explicitly
    # specified
    old_results_dir = "{0}/{1}".format(old_results_dir, timestamp)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
    # Directory we're moving the old results to
    subprocess_check_call("mkdir -p {0}".format(old_results_dir)
    subprocess.check_call("mv {1}/* {0}".format(old_results_dir, results_output_dir), shell=True)

    # TODO: Move the following block to a separate function
    # Get list of SNPs to test, output from gwas-download overlap module
    kept_data = []
    for g in glob.glob(snp_overlap_list):
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
        # TODO: Standardize this, at least the tmp dir part
        temp["snp_list_file"] = "tmp/snp_list{0}.txt".format(i)
        temp["out_dir"] = results_dir

        # Add locus to SNP list...but only once for each gene
        with open("tmp/snp_list{0}.txt".format(i), "w") as w:
            w.write("{0}\t{1}\t{2}\n".format(test[0], test[1], test[7]))
               
        # Add corresponding gwas experiment to the list, if not already present
        # TODO: Allow option of user-specified pval_only vs. effect_size for GWAS
        temp["gwas_experiments"][test[2]] = {"ref": "1kgenomes", "gwas_format": "pval_only"}
        if test[2] != test[4]:
            temp["gwas_experiments"][test[2]]["traits"] = [test[4]]

        # Add corresponding eQTL tissue to the list
        temp["eqtl_experiments"][test[3]] = {"ref": "1kgenomes", "eqtl_format": "effect_size"}

        # TODO: Make this a user-specified OR constant directory
        # Write config file to the appropriate directory
        with open("tmp/ipsc_config{0}.config".format(i), "w") as w:
            json.dump(temp, w)

        # Run the test
        subprocess.call("python bin/colocalization_pipeline/dispatch.py tmp/ipsc_config{0}.config 1 &".format(i), shell=True)

        while int(subprocess.check_output('''ps -ef | grep "python bin/colocalization_pipeline/dispatch.py tmp/ipsc_config" | wc -l''', shell=True)) > max_threads:
            time.sleep(5)

# TODO: Come up with a better clean-up scheme for cleaning the tmp directory -- perhaps a time-stamped folder that
# can be deleted as a whole once this runs, independently of other runs

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
