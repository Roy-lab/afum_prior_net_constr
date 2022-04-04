#!/bin/bash

## Usage:
## bash merge_tf_to_gene_maps.sh <CisBp_tf_to_gene_map_file> <Keller_tf_to_gene_map_file> <output_file>
##
## Examples:
## bash merge_tf_to_gene_maps.sh MotifScanResults/CisBp/U10_D1/tf_to_gene_map_CisBp_U10_D1.txt MotifScanResults/Keller/P90_U10_D1/tf_to_gene_map_Keller_P90_U10_D1.txt MotifScanResults/Merged/tf_to_gene_map_Merged_P90_U10_D1.txt
##
## Goal:
## Given the gene to TF map files of CIS-BP and Keller, merge them into a single file.

CISBP_FILE=$1
KELLER_FILE=$2
OUT_FILE=$3

cat ${CISBP_FILE} > ${OUT_FILE}
cat ${KELLER_FILE} >> ${OUT_FILE}


