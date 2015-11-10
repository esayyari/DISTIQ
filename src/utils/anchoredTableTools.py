import dendropy
import itertools
import sys
import os
import tableManipulationTools as tbs
import printTools as pr
import toolsTreeTaxa as tstt
import numpy as np
def anchoredDistance(**kwargs):
	readFromTable=False
	for k,v in kwargs.iteritems():
		if k == "qfile":
			qfile=v
			readFromTable = True
		elif k == "achs":
			achs = sorted(v)
		elif k == "gt":
			trees = v
		elif k == "outfile":
			outfile = v
		elif k == "wrkPath":
			out = v
		elif k == "taxa":
			taxa = v
	if(readFromTable):
		frq=tbs.readQuartetTable(qfile)	
		D = anchoredDistanceFromFrq(frq,achs)
	else:
		D = findAnchoredDistanceTable(achs,trees,taxa,out)	
	keyDict = sorted(list(np.unique((" ".join(D.keys())).split(" "))));
	#print keyDict 
	pr.printDistanceTableToFile(D,keyDict,outfile)
	return 
def anchoredDistanceFromFrq(frq,achs):
	D = dict()
	for k,v in frq.iteritems():
		kt = sorted(k.split("/"))
		if ((achs[0] in kt ) and( achs[1] in kt)):
			s = sorted(list(set(kt)-{achs[0],achs[1]}))
			key1 = s[0]+" "+s[1]
			key2 = s[1]+" "+s[0]
			if s[0]<achs[0]:
				D[key1]=-np.log(frq[k][s[1]])
				D[key2]=D[key1]	
			elif s[0]>achs[0]:
				D[key1]=-np.log(frq[k][achs[1]])	
				D[key2]=D[key1]
	return D
def buildEmptyQuartets(anch,taxa,n):
	taxa = set(taxa)-set(anch)
	Q = dict()
	for pair in chooseTaxa(taxa):
		p1 = sorted(list(pair))
		p2 = sorted(anch)
		p = "/".join(sorted(p1+p2))
		Q[p] = [0.5,n+1.5]
	return Q

def chooseTaxa(taxa):
	return set(itertools.combinations(taxa, 2))
def genKey(p1,p2):
	if p1[0]<p2[0]:
        	p = p1[0]+' '+p1[1]+' | '+p2[0]+' '+p2[1]
       	else:
        	p = p2[0]+' '+p2[1]+' | '+p1[0]+' '+p1[1]
	return p
def findAnchoredQuartets(anch,trees,taxa,out):
	anch = sorted(anch)
	n = len(trees)
	Q = buildEmptyQuartets(anch,taxa,n)
	Q2 = list()
	for tree in trees:
		rerooted=reroot(tree,anch)
		node = rerooted[0]
		root = rerooted[1]
		while(node.parent_node.label!=root.label):
			node_pre = node
			node = node.parent_node
			chs = node.child_nodes()
			chs_n = len(chs)
			if len(chs)>2:
				for i in range(0,chs_n):
					ch = chs[i]
					if (ch == node_pre):
						continue
					else:
						listTaxa = list(ch.leaf_nodes())
						Q= addQuartets(ch, listTaxa,Q,Q2,anch)
					for j in range(i+1,chs_n):
						if (chs[i] == chs[j]):
							continue
						else:
							listTaxatmp = [listTaxa,list(chs[j].leaf_nodes())]
							Q=removeFromQuartetsLentreesh(Q,listTaxatmp,anch)
			else:
				for ch in chs:
					if (ch==node_pre):
						continue
					else:
						listTaxa = list(ch.leaf_nodes())
						Q= addQuartets(ch, listTaxa,Q,Q2,anch)
#		a = out+'/quartets_'+anch[0]+anch[1]+'.q'
#		f = open(a,'a')
#		f.write("\n".join(Q2))
#		f.close()
	return Q
def reroot(tree,anch):
	tstt.labelNodes(tree)
	filter = lambda taxon: True if taxon.label==anch[0] else False
	root = tree.find_node_with_taxon(filter)
	filter = lambda taxon: True if taxon.label==anch[1] else False
	node = tree.find_node_with_taxon(filter)
	tree.reroot_at_node(root, update_bipartitions=True, suppress_unifurcations=False)
	return [node,root]
def findAllChildrenPairs(listTaxa):
	listTaxaLabels = list()
	for t in listTaxa:
		listTaxaLabels.append(t.label)
	pairs = chooseTaxa(listTaxaLabels)
	return pairs
def addQuartets( ch, listTaxa,Q,Q2,anch):
	pairs = findAllChildrenPairs(listTaxa)
	for p in pairs:
		key=genKey(list(p),anch)
		t = sorted(list(p)+anch)
		Q2.append(key)
		Q["/".join(t)][0] += 1
	return Q
def removeFromQuartetLentreesh(Q,listTaxa,anch):
	x = list()
	for et in listTaxa:
		T = list()
		for t in et:
			T.append(t.label)	 
		x.append(T)
	keySet=[p for p in itertools.product(*x)]
	for p in keySet:
		key = sorted(list(p) + anch)
		Q["/".join(key)][1] -= 1
	return Q
def findAnchoredDistanceTable(achs,trees,taxa,out):
	frq=findAnchoredQuartets(achs,trees,taxa,out) 
        D = dict()
        for k,v in frq.iteritems():
                kt = sorted(k.split("/"))
                if ((achs[0] in kt ) and( achs[1] in kt)):
                        s = sorted(list(set(kt)-{achs[0],achs[1]}))
                        key1 = s[0]+" "+s[1]
                        key2 = s[1]+" "+s[0]
                       	D[key1]=-np.log(frq[k][0]/float(frq[k][1]))
                        D[key2]=D[key1]
        return D
	
