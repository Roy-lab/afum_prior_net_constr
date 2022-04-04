#!/bin/bash

## Usage:
## bash write_motifs.sh > write_motifs.out 2>&1
##

ORIG_DIR=`pwd`
SCRIPT_DIR="/mnt/dv/wid/projects2/Roy-common/programs/scripts/motif_finding_pipeline_example"
OUT_DIR=${ORIG_DIR}/"MotifScanResults"

## Local R lib location
R_LIB_LOC="/mnt/ws/home/spyne/R/x86_64-conda_cos6-linux-gnu-library/3.5"

## Number of motifs in afumPFM.txt
NUM_MOTIF=628

## Loads R-3.5.3
module load anaconda3-2020.02

## Install package "BSgenome.Afum.ASM265v1_1.0.0" in the given local lib
# R CMD INSTALL -l ${R_LIB_LOC} ${ORIG_DIR}/BSgenome.Afum.ASM265v1_1.0.0.tar.gz ## install package

## Go to PIQ code dir
cd ${SCRIPT_DIR}

for motif_idx in $(seq 1 ${NUM_MOTIF})
do
        Rscript writeMot2.R ${OUT_DIR}/${motif_idx}
done

## Return to the original dir
cd ${ORIG_DIR}
