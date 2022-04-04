import sys

def readMotifs (infile):
	mot_map = {}

        ## Initialize motif sl. no.
        motif_sl_no = 1

	f = open(infile,'r')
	for l in f:
		# Expected input format:
                # >M01669_2.00;AFUA_5G03430
                # >M00008_2.00;AFUA_4G08590::AFUA_5G05990
                # >M...
		parts = l.strip().split(';')

		motif_id = parts[0]
                motif_id = motif_id.replace(">", "")


		tf_names = parts[1]

                mlist = mot_map.get(motif_sl_no,[])

		mlist.append((motif_id,tf_names))

                
		mot_map[motif_sl_no] = mlist

                motif_sl_no += 1
	f.close()
	return mot_map

def writeMotToTfMap(mot_map, outfile):
	f = open(outfile,'w')
	for (motif_sl_no) in mot_map:
		mlist = mot_map[motif_sl_no]

		#loop over motif entries
                for (motif_id,tf_names) in mlist:
                	f.write('%i\t%s\t%s\n' % (motif_sl_no,motif_id,tf_names));
	f.close()

if __name__ == '__main__':
        infile = sys.argv[1]
	outfile = sys.argv[2]

	mot_map = readMotifs(infile)

	mot_to_TF_map = writeMotToTfMap(mot_map, outfile)
