#!/bin/bash
##
## Usage:
## bash map_MotifSlNo_to_TFs.sh
##
## Goal:
## Map Motif Sl. No. to TF names.
##
## Requires:
## mapMotifSlNoToTFs.py
##

IN_FILE="afumPFM.txt"
TMP_FILE="mapMotifSlNoToTFs_tmp.txt"
OUT_FILE="motif_to_TF_map.txt"

## Extract the lines with Motif ID and TF names i.e.
## the lines starting with ">M"
grep -E "^>M" ${IN_FILE} > ${TMP_FILE}

## Load Python 2.7.15.
## Requires Python 2, throws error with Python 3.
module load anaconda2-2018.12

## Map Motif Sl. No. to TF names
python mapMotifSlNoToTFs.py ${TMP_FILE} ${OUT_FILE}

rm ${TMP_FILE}

