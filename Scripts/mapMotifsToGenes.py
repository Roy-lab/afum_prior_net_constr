## A pair of coordinates are mapped to a gene based on the following algorithm.
## If it is a + strand, then map when
## (coordinate start >= (gene start - upstream window)) && (coordinate end <= (gene start + downstream window)).
## If it is a - strand, then map when
## (coordinate start >= (gene end - downstream window)) && (coordinate end <= (gene end + upstream window)).
## Note: To produce the formula for - strand, replace {gene start, upstream window, downstream window} with 
## {gene end, downstream window, upstream window}, respectively, in the + strand formula.

import sys

#def readMot(inname):
#	cmap = {}
#	f = open(inname,'r')
#	for l in f:
#		#assumed input format of motif information
#		#chr1	3004298	3004313	+	8.830266
#		parts = l.strip().split('\t')
#		c  = parts[0]
#		p1 = int(float(parts[1]))
#		p2 = int(float(parts[2]))
#		ID=parts[3];
#		score = float(parts[4])
#		strand = parts[5]
#		t  = cmap.get(c,[])
#		t.append((p1,p2,score,strand,ID))
#		cmap[c] = t
#	f.close()
#	return cmap

def readMot(inname, ID):
        cmap = {}
        f = open(inname,'r')
        for l in f:
                #assumed input format of motif information
                #chr1   3004298 3004313 +       8.830266
                parts = l.strip().split('\t')
                c  = parts[0]
                p1 = int(float(parts[1]))
                p2 = int(float(parts[2]))
                # ID=parts[3];
                strand = parts[3]
                score = float(parts[4])
                t  = cmap.get(c,[])
                t.append((p1,p2,score,strand,ID))
                # t.append((p1,p2,score,strand))
                cmap[c] = t
        f.close()
        return cmap


def readGenes(inname):
	gmap = {}
	f = open(inname,'r')
	for l in f:
		#assummed input format of TSS information
		#ENSMUST00000166088	chr10	75032585	75032585
		parts = l.strip().split('\t')
		g  = parts[0]
		c  = parts[1]
		p1 = int(float(parts[2]))
		p2 = int(float(parts[3]))
		strand=parts[4]
		gs = gmap.get(c,[])
		gs.append((g,p1,p2,strand))
		gmap[c] = gs
	f.close()
	return gmap

# take second element for sort
def takeFirst(elem):
    return elem[0]

def takeWindow(elem,w_up,w_down):
	if elem[3] == '+':
    		return elem[1]-w_up
	else:
		return elem[2]-w_down

def writeTSS(ID,out_file,out_file_summary,cmap,gmap,w_up,w_down):
	f = open(out_file,'w')
	f2 = open(out_file_summary,'w')
	genecnt = {}
	for (c) in gmap:
		if (c) not in cmap:
                        continue
		#sort genes by starting edge of mapping window for this gene
		gs = gmap[c]
		gs.sort(key=lambda x:takeWindow(x,w_up,w_down))
		#sort by starting coordinate of motif.
		cs = cmap[c]
		cs.sort(key=takeFirst)
		start=0
		#loop over motif entries
		for (mp1,mp2,mScore,mStrand,ID) in cs:
			#loop over gene entries
			for gI in range(start,len(gs)):
				# print start
				#get gene information 
				(g,p1,p2,gstrand)=gs[gI]
				#if + strand gene check
				if gstrand == '+':
					if p1+w_down < mp1:
						start=gI
						continue
					if p1-w_up > mp2:
						break
					if mp1 >= p1-w_up and mp2 <= p1+w_down:
						# f.write('%s\t%i\t%i\t%s;%s\t%f\t%s\n' % (c,mp1,mp2,ID,g,mScore,mStrand));
						f.write('%s\t%i\t%i\t%i;%s\t%f\t%s\n' % (c,mp1,mp2,ID,g,mScore,mStrand));
						f2.write('%s\t%f\n' % (g,mScore));
				#if - strand gene check in slightly differnet way, determining the window coordinates differently 
				else:
					if p2+w_up < mp1:
						start=gI
						continue
					if p2-w_down > mp2:
						break
					if mp1 >= p2-w_down and mp2 <= p2+w_up:
						# f.write('%s\t%i\t%i\t%s;%s\t%f\t%s\n' % (c,mp1,mp2,ID,g,mScore,mStrand));
						f.write('%s\t%i\t%i\t%i;%s\t%f\t%s\n' % (c,mp1,mp2,ID,g,mScore,mStrand));
						f2.write('%s\t%f\n' % (g,mScore));
	f.close()
	f2.close()

if __name__ == '__main__':
        ID = int(sys.argv[1]) 
	print "Processing motif no. " + str(ID) + "..."

	cmap = readMot(sys.argv[2], ID)
	gmap = readGenes(sys.argv[3])
	w_up = int(sys.argv[4])
	w_down = int(sys.argv[5])
	out_file = sys.argv[6]
	out_file_summary = sys.argv[7]  
	net = writeTSS(ID,out_file,out_file_summary,cmap,gmap,w_up,w_down)
	print "Completed: Motif no. " + str(ID)
