## Usage:
## module load anaconda3-2020.11 ## Load Python 3.7.6
## python subset_priorNet_for_common_genes.py <prior_net_file> <common_genes_file> <output_file>
##
## Example:
## python subset_priorNet_for_common_genes.py MotifScanResults/Merged/tf_to_gene_map_Merged_P90_U10_D1_pRanked_sorted.txt /mnt/dv/wid/projects5/Roy-Aspergillus/Data/common_genes.txt MotifScanResults/Merged/tf_to_gene_map_Merged_P90_U10_D1_pRanked_sorted_common_genes.txt
##
## Goal:
## This script takes two files as input:
## (a) a prior net file where each line is an edge in format "<TF> \t <target> \t <confidence_score>",
## (b) a list of common genes (between RNA-Seq and microarray; must have a column header saying "Genes").
## Then finds edges where both the TF and target gene belong to the list of common genes, and writes to <output_file>.
##

import sys
import pandas as pd

def writeValidEdges(prior_edges, common_genes, out_file):

	num_edges = prior_edges.shape[0]

	f_out = open(out_file,"w")
	for edge_idx in range(num_edges):

		print(edge_idx)

		TF = prior_edges.iloc[edge_idx, 0]
		tgt = prior_edges.iloc[edge_idx, 1]
		conf_score = prior_edges.iloc[edge_idx, 2]

		if ((TF in common_genes) and (tgt in common_genes)):
			f_out.write("%s\t%s\t%.8f\n" % (TF, tgt, conf_score));
		# else:
			# print(TF + tgt)
	f_out.close()

if __name__ == "__main__":

	prior_net_file = sys.argv[1]
	prior_edges = pd.read_csv(prior_net_file, sep = "\t", header = None)

	common_genes_file = sys.argv[2]
	common_genes = pd.read_csv(common_genes_file, header = 0)
	common_genes = set(common_genes.loc[:, "Genes"])

	out_file = sys.argv[3]

	writeValidEdges(prior_edges, common_genes, out_file)
