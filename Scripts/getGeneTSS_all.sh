#!/bin/bash
##
## Usage:
## bash getGeneTSS_all.sh
##
## Goal:
## Given a genome assembly .gff3 file, extract TSS information for genes and other elements, such as pseudogenes.
##

INFILE="/mnt/dv/wid/projects5/Roy-Aspergillus/Data/GenomeAssembly/Aspergillus_fumigatus.ASM265v1.49.gff3"
OUTFILE="geneTSS_all.txt"

## The range of chromosome IDs in the .gff3 file, e.g., [1, 8]
CHR_ID_MIN=1
CHR_ID_MAX=8

## F = Input field separator.
## NR = number of rows. Skip the first 16 rows.
## OFS = Output field separator.
awk \
-F "\t" 'NR>16 { 
if (substr($9,1,8) == "ID=gene:")
{ gsub("ID=gene:","",$9); gsub(";.*","",$9); print $9,$1,$4,$5,$7 }
}' OFS="\t" ${INFILE} > ${OUTFILE}

