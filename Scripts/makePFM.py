## Usage: python makePFM.py --motifdir Motif_Afum_CisBp/pwms_all_motifs --tfinfo Motif_Afum_CisBp/TF_Information_all_motifs.txt --motifnames Motif_Afum_CisBp/info.txt --outname afumPFM.txt
##
## This script is a customized version of
## /mnt/dv/wid/projects2/Roy-common/programs/scripts/motif_finding_pipeline_example/makePFM.py .
## Please see https://elog.discovery.wisc.edu/Software/166 for details.

import sys
import argparse

parser = argparse.ArgumentParser(description='Convert CIS-BP PWMs to JASPAR format PFM.')
parser.add_argument('--motifdir', metavar='IN', type=str, nargs=1,help='motif directory',required=True)
parser.add_argument('--motifnames', metavar='IN', type=str, nargs=1,help='list of motifs in directory',required=True)
parser.add_argument('--tfinfo', metavar='IN', type=str, nargs=1,help='motif to TF information',required=True)
parser.add_argument('--outname', metavar='OUT', type=str, nargs=1,help='output file',required=True)
args = parser.parse_args()

def readTFInfo(inname):
	motifs = {}
	f = open(inname,'r')
	for l in f:
		#T149479_1.02	F253_1.02	TS19_1.02	M6505_1.02	MS18_1.02	ENSG00000121068	TBX2	Homo_sapiens	I	T-box	T-box	10.6	TBX5_si	HocoMoco	HocoMoco	HocoMoco	Kulakovskiy	2013	23175603	July 2014	Ensembl	http://www.ensembl.org/	2011	Oct	26
		parts = l.strip().split('\t')
		motif = parts[3]
		tf    = parts[6]
		t     = motifs.get(motif,set([]))
		t.add(tf)
		motifs[motif] = t
	f.close()
	return motifs

def readOneMotif(inname):
	pwm = {}
	f = open(inname,'r')
	cnt = 0
	fixth = 1000000
	for l in f:
		parts = l.strip().split('\t')
		print(parts)
		cnt += 1
		if cnt == 1:
			header = parts[1:]
			for h in header:
				pwm[h] = []
			continue
		valsf = map(float,parts[1:])
		valsi = [int(round(fixth*v)) for v in valsf]
		for i in range(len(header)):
			pwm[header[i]].append(valsi[i])
	f.close()
	print(pwm)
	if cnt == 1:
		return {}
	for i in range(cnt-1):
		print(i)
		v = sum([pwm[h][i] for h in header])
		if v != fixth:
			print(inname,i,v)
		if v < fixth:
			if fixth - v == 1000:
				j=0
				while v<fixth:
					print(i,j)
					if pwm[header[j]][i]>0:
						v += 250
						pwm[header[j]][i]+=250
					print(v)
					j += 1
			if fixth - v < 5 :
				for j in range(fixth-v):
					pwm[header[j]][i]+=1
		if v > fixth:
			if v - fixth == 1:
				j = 0
				while v>fixth:	
					print(i,j)
					if pwm[header[j]][i]>0:
						v -= 1
						pwm[header[j]][i]-=1
					j += 1
			if v - fixth == 1000:
				j = 0
				while v>fixth:
					print(i,j)
					if pwm[header[j]][i]>0:
						v -= 250
						pwm[header[j]][i]-=250
					print(v)
					j += 1
	print(pwm)
	return pwm

def writePFMs(outname,motifmap,motifpwms):
	header = ['A','C','G','T']
	f = open(outname,'w')
	for mot in motifpwms:
		if mot not in motifmap:
			print('motif not in map: ',mot)
			continue
		names = list(motifmap[mot])
		f.write('>%s;%s\n' % (mot,'::'.join(names)))
		for h in header:
			f.write('%s [ %s ]\n' % (h,' '.join(map(str,motifpwms[mot][h]))))
	f.close()

if __name__ == '__main__':
	motifs = readTFInfo(args.tfinfo[0])
	allpwms = {}
	f = open(args.motifnames[0],'r')
	first=True
	for l in f:
		if first:
			first=False
			continue
		mot = l.strip().split('\t')[0] #remove .txt
		inname = '%s/%s.txt' % (args.motifdir[0],mot)
		pwm = readOneMotif(inname)
		print(pwm)
		if len(pwm) == 0:
			continue
		allpwms[mot] = pwm
	f.close()
	writePFMs(args.outname[0],motifs,allpwms)
