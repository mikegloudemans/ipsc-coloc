import operator
import subprocess
import json
import sys
import time

def main():
    # Reset things fresh on each run, so we're not mixing results
    subprocess.call("rm -rf /users/mgloud/projects/brain_gwas/output/ipsc-rerun-bonus-tests/*", shell=True)

    kept_data = []
    with open("/users/mgloud/projects/ipsc/output/snps_to_test_marcs_bonus_fdr05_window10000.txt") as f:
        all_data = []
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
        temp["snp_list_file"] = "/users/mgloud/projects/ipsc/tmp/snp_list{0}.txt".format(i)

        # Add locus to SNP list...but only once for each gene
        with open("/users/mgloud/projects/ipsc/tmp/snp_list{0}.txt".format(i), "w") as w:
            w.write("{0}\t{1}\t{2}\n".format(test[0], test[1], test[7]))
               
        # Add corresponding gwas experiment to the list, if not already present
        temp["gwas_experiments"][test[2]] = {"ref": "1kgenomes", "gwas_format": "effect_size"}
        if test[2] != test[4]:
            temp["gwas_experiments"][test[2]]["traits"] = [test[4]]

        # Add corresponding eQTL tissue to the list
        temp["eqtl_experiments"][test[3]] = {"ref": "1kgenomes", "eqtl_format": "effect_size"}

        # Write config file to the appropriate directory
        with open("/users/mgloud/projects/ipsc/tmp/ipsc_config{0}.config".format(i), "w") as w:
            json.dump(temp, w)

        # Run the test
        subprocess.call("python /users/mgloud/projects/static_coloc_pipeline/scripts/dispatch.py /users/mgloud/projects/ipsc/tmp/ipsc_config{0}.config 1 &".format(i), shell=True)

        while int(subprocess.check_output('''ps -ef | grep "python /users/mgloud/projects/static_coloc_pipeline/scripts/dispatch.py /users/mgloud/projects/ipsc/tmp/ipsc_config" | wc -l''', shell=True)) > 3:
            time.sleep(5)

template = '''
{
        "out_dir_group": "ipsc-rerun-bonus-tests",

       "gwas_experiments": 
	{
	},
	
	"eqtl_experiments":	
	{
	},

	"eqtl_threshold": 
		1,

	"selection_basis": 
		"snps_from_list",

	"snp_list_file":
                "/users/mgloud/projects/ipsc/tmp/snp_list.txt",

	"methods": 
	{
		"finemap":{}
	},

        "ref_genomes": 
	{
		"1kgenomes": 
		{
			"file": 
				"/mnt/lab_data/montgomery/shared/1KG/ALL.chr{0}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",

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
