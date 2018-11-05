import gzip
import subprocess
import operator
from scipy import stats

subprocess.call("rm -f /users/mgloud/projects/ipsc/data/GeneLevel_20181015/full_qtl_results_formatted.txt", shell=True)

for i in range(1, 23):
    with gzip.open("/users/mgloud/projects/ipsc/data/GeneLevel_20181015/full_qtl_results_{0}.txt.gz".format(i)) as f:
        with open("/users/mgloud/projects/ipsc/data/GeneLevel_20181015/full_qtl_results_formatted.txt".format(i), "a") as a:
            if i == 1:
                a.write(f.readline().strip())
                a.write("\tpvalue\n")
            else:
                f.readline()
            all_sites = []
            for line in f:
                data = line.strip().split()
                data[1] = int(data[1])
                data.insert(2, str(i))
                data.append(2*stats.norm.sf(abs(float(data[3]) / float(data[4]))))
                all_sites.append(data)

            all_sites = sorted(all_sites, key=operator.itemgetter(1))

            for site in all_sites:
                a.write("\t".join([str(s) for s in site]) + "\n")

subprocess.check_call("bgzip -f /users/mgloud/projects/ipsc/data/GeneLevel_20181015/full_qtl_results_formatted.txt".format(i), shell=True)
subprocess.check_call("tabix -f -S 1 -s 3 -b 2 -e 2 /users/mgloud/projects/ipsc/data/GeneLevel_20181015/full_qtl_results_formatted.txt.gz".format(i), shell=True)
