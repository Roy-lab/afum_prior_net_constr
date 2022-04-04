#!/bin/bash

## Usage: bash PrepInfo_Afum.sh
##
## This script is a customized version of 
## /mnt/dv/wid/projects2/Roy-common/programs/scripts/motif_finding_pipeline_example/PrepInfo.sh .
## Please see https://elog.discovery.wisc.edu/Software/166 for details.

## Define an associative array "D"
declare -A D

## Assign values to array D
D[afum]=Motif_Afum_CisBp
# D[arabidopsis_thaliana]=Arabidopsis_thaliana_2018_05_01_1-00_pm
# D[medicago_truncatula]=Medicago_truncatula_2018_05_01_1-01_pm
# D[solanum_lycopersicum]=Solanum_lycopersicum_2018_05_01_2-37_pm

printf "Species/Directory|# TF's|# Motifs|# TF-motif pairs\n|-\n"

rm -rf meme_files
mkdir meme_files

##for i in medicago_truncatula
for i in afum
do
	## Create the file if does not exitst. 
	## Otherwise, it it already exists, empty its content.
	touch ${D[$i]}/info.txt
        truncate -s 0 ${D[$i]}/info.txt 
	
	touch ${D[$i]}/motifIDs.txt
        truncate -s 0 ${D[$i]}/motifIDs.txt
	
	touch ${D[$i]}/motifPWMs.txt
	truncate -s 0 ${D[$i]}/motifPWMs.txt

	cat ${D[$i]}/TF_Information_all_motifs.txt | awk '$4!="."{print}' | cut -f4,6,7,8,10 > ${D[$i]}/info.txt
	cut -f2,3 ${D[$i]}/info.txt | awk 'NR>1{print}'| sort -u -k2 > ${D[$i]}/names.txt 
	export NI=`cat ${D[$i]}/TF_Information_all_motifs.txt| wc -l`
	cut -f1 ${D[$i]}/info.txt | awk 'NR>1{print}' | sort -u > ${D[$i]}/motifIDs.txt
	export NTF=`cat ${D[$i]}/names.txt | wc -l`
	export NM=`cat ${D[$i]}/motifIDs.txt | wc -l`
	printf "${D[$i]}|$((NTF))|$((NM))|$((NI-1))\n|-\n"

	export n=0
	export n2=0
	export nlast=0
	f=0
	FILE=meme_files/Cis_BP_${i}_${f}.meme

	while (($n<${NM}))
	do
		#echo ${n}
		if (( $n2 % 40 == 0 || $n2 == 0 ))
		then
			if (( $n2 > 0 && $nlast < $n2 ))
			then
				#echo ${n}
				export  FILE=meme_files/Cis_BP_${i}_${f}.meme
				printf "MEME version 4.4\n\n" > ${FILE}
				printf "ALPHABET= ACGT\n\n" >> ${FILE}
				printf "strands: + -\n\n" >> ${FILE}
				printf "Background letter frequencies (from uniform background):\n" >> ${FILE}
				printf "A 0.25000 C 0.25000 G 0.25000 T 0.25000\n" >> ${FILE}
				printf "Touch ${n} ${n2} ${FILE} \n"
				export f=$((f+1))
				export nlast=$n2
			fi
		fi
		export n=$((n+1))	
		export M=`awk -v r=${n} 'NR==r{print $1}' ${D[$i]}/motifIDs.txt`
		export PWM=${D[$i]}/pwms_all_motifs/${M}.txt
		if [ `wc -l ${PWM} | awk '{print $1}'` -ge "2" ]
		then
			printf "${M}\n" >> ${D[$i]}/motifPWMs.txt
			printf "\nMOTIF ${M}\n\n" >> ${FILE}
			export w=`tail -n1 ${PWM} | awk '{print $1}'`
			printf "letter-probability matrix: alength= 4 w= ${w}\n" >> ${FILE}
			awk 'NR>1{printf("%f\t%f\t%f\t%f\n",$2,$3,$4,$5)}' ${PWM} >> ${FILE}
			n2=$((n2+1))
		fi

	done
done
