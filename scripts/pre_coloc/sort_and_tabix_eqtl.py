import gzip
import subprocess
import operator
from scipy import stats

types = ["ApaLevel", "ExonLevel", "SplicingLevel", "TranscriptRatio"]

for typ in types:
    subprocess.call("rm -f data/Input/{0}/full_qtl_results_formatted.txt".format(typ), shell=True)

    for i in range(1, 23):
        with gzip.open("data/Input/{1}/full_qtl_results_{0}.Pval-rescaled.txt.gz".format(i, typ)) as f:
            with open("data/Input/{1}/full_qtl_results_formatted.txt".format(i, typ), "a") as a:
                if i == 1:
                    a.write(f.readline())
                else:
                    f.readline()
                all_sites = []
                for line in f:
                    data = line.strip().split()
                    data[1] = int(data[1])
                    all_sites.append(data)

                all_sites = sorted(all_sites, key=operator.itemgetter(1))

                for site in all_sites:
                    a.write("\t".join([str(s) for s in site]) + "\n")

    subprocess.check_call("bgzip -f data/Input/{0}/full_qtl_results_formatted.txt".format(typ), shell=True)
    subprocess.check_call("tabix -f -S 1 -s 3 -b 2 -e 2 data/Input/{0}/full_qtl_results_formatted.txt.gz".format(typ), shell=True)

for typ in ["GeneLevel"]:
    subprocess.call("rm -f data/Input/{0}/full_qtl_results_formatted.txt".format(typ), shell=True)

    for i in range(1, 23):
        with gzip.open("data/Input/{1}/full_qtl_results_{0}.txt.gz".format(i, typ)) as f:
            with open("data/Input/{1}/full_qtl_results_formatted.txt".format(i, typ), "a") as a:
                if i == 1:
                    a.write(f.readline())
                else:
                    f.readline()
                all_sites = []
                for line in f:
                    data = line.strip().split()
                    data[1] = int(data[1])
                    all_sites.append(data)

                all_sites = sorted(all_sites, key=operator.itemgetter(1))

                for site in all_sites:
                    a.write("\t".join([str(s) for s in site]) + "\n")

    subprocess.check_call("bgzip -f data/Input/{0}/full_qtl_results_formatted.txt".format(typ), shell=True)
    subprocess.check_call("tabix -f -S 1 -s 3 -b 2 -e 2 data/Input/{0}/full_qtl_results_formatted.txt.gz".format(typ), shell=True)
