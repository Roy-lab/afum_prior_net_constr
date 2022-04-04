#!/bin/bash

## Usage:
## bash map_motifs_to_genes.sh
##
## Goal:
## This is a driver script for mapMotifsToGenes.py, which
## maps gene coordinates to gene names.
##
## Requires:
## mapMotifsToGenes.py
##

IN_DIR="MotifScanResults"
OUT_DIR=${IN_DIR}

# GENE_TSS_FILE="geneTSS.txt"
GENE_TSS_FILE="geneTSS_all.txt"

## Upstream window from gene TSS
UP_WIN=10000

## Downstream window from gene TSS
DOWN_WIN=1000

## Load Python 2.7.15.
## Requires Python 2, throws error with Python 3.
module load anaconda2-2018.12

## The input file names are expected to be <motif_id>.all.motifs.txt, e.g., 100.all.motifs.txt.
for IN_FILE in `ls ${IN_DIR}/*.all.motifs.txt`; 
do 
   ## If input filename is 100.all.motifs.txt, then motif sl. no. is 100.
   ## Note: The value of IN_FILE is "MotifScanResults/100.all.motifs.txt", not "100.all.motifs.txt"".
   MOTIF_SL_NO="${IN_FILE#${IN_DIR}/}"
   MOTIF_SL_NO="${MOTIF_SL_NO/.*/}"

   ## If input filename is 100.all.motifs.txt,
   ## then output filenames would be 100.mapped.genes.txt and 100.mapped.genes.summary.txt.
   OUT_FILE="${MOTIF_SL_NO}.mapped.genes.txt"
   OUT_FILE_SUMMARY="${MOTIF_SL_NO}.mapped.genes.summary.txt"

   ## Map input coordinates to gene names
   python mapMotifsToGenes.py ${MOTIF_SL_NO} ${IN_FILE} ${GENE_TSS_FILE} ${UP_WIN} ${DOWN_WIN} ${OUT_DIR}/${OUT_FILE} ${OUT_DIR}/${OUT_FILE_SUMMARY}
done

