## Goal: Map TF names to target gene names
##

import sys
import pandas as pd

import os.path
from os import path

if __name__ == '__main__':
	motif_to_tf_map_file = sys.argv[1]

	in_out_dir = sys.argv[2]
	in_file_suffix = sys.argv[3]

	# out_dir = in_dir
	out_file = sys.argv[4]
	out_file = in_out_dir + "/" + out_file

	f = open(out_file,"w")

	## Expected format:
	## 584     M01390_2.00     AFUA_5G11070::AFUA_5G12930::AFUA_5G02800
	motif_to_tf_map = pd.read_csv(motif_to_tf_map_file, sep= "\t", header = None)

	num_motifs = motif_to_tf_map.shape[0]

	for loop_idx in range(num_motifs):
		motif_sl_no = motif_to_tf_map.iloc[loop_idx, 0]
		in_filename = str(motif_sl_no) + in_file_suffix
		in_file = in_out_dir + "/" + in_filename

		## If the input file does not exist, skip to the next motif
		if not path.exists(in_file):
			continue

		motif_to_gene_map = pd.read_csv(in_file,sep="\t",header=None)

		num_genes = motif_to_gene_map.shape[0]

		## TF names are separated by "::" if more than one
		tf_names = motif_to_tf_map.iloc[loop_idx, 2]
		tf_names = tf_names.split("::")

		for tf_idx in range(len(tf_names)):
			curr_tf = tf_names[tf_idx]

			for gene_idx in range(num_genes):
				gene_name = motif_to_gene_map.iloc[gene_idx, 0]

				## Confidence score of the motif to gene mapping
				score = motif_to_gene_map.iloc[gene_idx, 1]

				f.write("%s\t%s\t%f\n" % (curr_tf, gene_name, score));

	f.close()

