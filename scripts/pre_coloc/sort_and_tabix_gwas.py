# Author: Mike Gloudemans
# Date: 1/9/2019
# Tabix and sort Marc's additional GWAS results

import glob
import subprocess

# Make output directories just in case they're not made yet
subprocess.call("mkdir -p data/marcs_gwas_files/reformatted", shell=True)
subprocess.call("mkdir -p data/marcs_gwas_files/reformatted/PhenomeScanner", shell=True)
subprocess.call("mkdir -p data/marcs_gwas_files/reformatted/GWAS_Catalog", shell=True)

# Do the PhenomeScanner ones first
for gwas in glob.glob("data/marcs_gwas_files/tmp_gwas_files/PhenomeScanner/*"):
    base_gwas = gwas.split("/")[-1].replace(".gz", "")
    print base_gwas
    subprocess.check_call("zcat {0} | head -n 1 > data/marcs_gwas_files/reformatted/PhenomeScanner/{1}".format(gwas, base_gwas), shell=True)
    subprocess.check_call("zcat {0} | tail -n +2 | sort -k1,1n -k2,2n >> data/marcs_gwas_files/reformatted/PhenomeScanner/{1}".format(gwas, base_gwas), shell=True)
    subprocess.check_call("bgzip -f data/marcs_gwas_files/reformatted/PhenomeScanner/{0}".format(base_gwas), shell=True)
    subprocess.check_call("tabix -f -S 1 -s 1 -b 2 -e 2 data/marcs_gwas_files/reformatted/PhenomeScanner/{0}.gz".format(base_gwas), shell=True)


# Then do the GWAS Catalog ones
for gwas in glob.glob("data/marcs_gwas_files/tmp_gwas_files/GWAS_Catalog/*"):
    base_gwas = gwas.split("/")[-1].replace(".gz", "")
    print base_gwas
    # These ones aren't sorted yet
    subprocess.check_call("zcat {0} | head -n 1 > data/marcs_gwas_files/reformatted/GWAS_Catalog/{1}".format(gwas, base_gwas), shell=True)
    subprocess.check_call("zcat {0} | tail -n +2 | sort -k1,1 -k2,2n >> data/marcs_gwas_files/reformatted/GWAS_Catalog/{1}".format(gwas, base_gwas), shell=True)
    subprocess.check_call("bgzip -f data/marcs_gwas_files/reformatted/GWAS_Catalog/{0}".format(base_gwas), shell=True)
    subprocess.check_call("tabix -f -S 1 -s 1 -b 2 -e 2 data/marcs_gwas_files/reformatted/GWAS_Catalog/{0}.gz".format(base_gwas), shell=True)


