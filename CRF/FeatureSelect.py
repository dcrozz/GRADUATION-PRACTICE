"""
Feature Selection by Chi measure
"""
#coding:utf-8
import ipdb
def getFile(filename):
	lst = []	
	with open(filename) as f:
		for line in f.readlines():
			cur_line = line.strip().split('\t')
			try:
				cur_line[2]
				lst.append(cur_line)
			except IndexError:
				pass
	return lst

def featureSelect(lst):
	dnalst = []
	rnalst = []
	linelst = []
	typelst = []
	prolst = []
	for line in lst:	
		tmp = line[1:]
		if tmp[-1] == 'DNA':
			dnalst.append(map(int,tmp[:-1]))
		elif tmp[-1] == 'RNA':
			rnalst.append(map(int,tmp[:-1]))
		elif tmp[-1] == 'cell_line':
			linelst.append(map(int,tmp[:-1]))
		elif tmp[-1] == 'cell_type':
			typelst.append(map(int,tmp[:-1]))
		elif tmp[-1] == 'protein':
			prolst.append(map(int,tmp[:-1]))
	dnacol = reduce(listAdd,dnalst)
	rnacol = reduce(listAdd,rnalst)
	linecol = reduce(listAdd,linelst)
	typecol = reduce(listAdd,typelst)
	procol = reduce(listAdd,prolst)
	feacol = reduce(listAdd,[dnacol,rnacol,linecol,typecol,procol])
	return dnacol,rnacol,linecol,typecol,procol,feacol

def listAdd(a,b):
	tmp = []
	for x,y in zip(a,b):
		try:
			tmp.append(int(x)+int(y))
		except ValueError:
			tmp.append(-1)
	return tmp

def changePOSandWS(lst,posdct,wsdct):
	new_lst = []
	for x in lst:
		try:
			tmp = posdct[x[1]]
			x[1] = ['0' for itm in range(len(posdct))]
			x[1][tmp] = '1'
		except KeyError:
			x[1] = ['0' for itm in range(len(posdct))]
			pass
		try:
			tmp = wsdct[x[11]]
			x[11] = ['0' for itm in range(len(wsdct))]
			x[11][tmp] = '1'
		except KeyError:
			x[11] = ['0' for itm in range(len(wsdct))]
		# ipdb.set_trace()
		x = x[:1] + x[1] + x[2:11] + x[11] + x[12:]
		new_lst.append(x)
	return new_lst

def calFeature(matrix,feacol):
	featuredct = {}
	for j in range(len(dnacol)):
		Sigma = 0
		for i in matrix:
			Oij = i[j]
			Eij = sum(i)*feacol[j]
			try:
				Sigma += (Oij - Eij)*(Oij - Eij)*1.0/Eij
			except ZeroDivisionError:
				Sigma = -1
		featuredct[str(j)] = Sigma
	sorteddict= sorted(featuredct.iteritems(), key=lambda d:d[1], reverse = True)
	return sorteddict

def getTop(dct,num):
	newdctlst = []
	tmp = [int(x) for x,y in dct[:num]]
	return tmp

def selectIndex(lst,indexlst):
	newlst = []
	for line in lst:
		new = [line[0]] + [line[a] for a in indexlst] + [line[-1]]
		newlst.append(new)
	return newlst

def outFile(lst,filename):
	with open(filename,'a') as f:
		for line in lst:
			# try:
			f.write('\t'.join(map(str,line)) + '\n')
			# except TypeError:
				# pass

def outSeq(dct,filename):
	with open(filename,'w') as f:
	    for i in range(len(dct)):
	        for x in dct:
	            if dct[x] == i:
	                f.write(x + '\t' + str(dct[x]) + '\n')


if __name__ == "__main__":
	import sys
	import time 
	starttime = time.time()
	trainlst = getFile('GENIA-CRF-TRAIN-5.txt')
	testlst = getFile('GENIA-CRF-TEST-5.txt')

	nedct={}
	ne = set([x[-1] for x in trainlst])
	nedct = {x for x in ne}
	posdct={}
	pos = set(x[1] for x in trainlst)
	posdct = {x:y for x,y in zip(pos,range(len(pos)))}  
	ws = set([x[11] for x in trainlst])
	wsdct = {x:y for x,y in zip(ws,range(len(ws)))} 

	outSeq(wsdct,'wsdct')
	outSeq(posdct,'posdct')

	pw_trainlst = changePOSandWS(trainlst,posdct,wsdct)
	pw_testlst = changePOSandWS(testlst,posdct,wsdct)

	dnacol,rnacol,linecol,typecol,procol,feacol = featureSelect(pw_trainlst)
	
	matrix = [dnacol,rnacol,linecol,typecol,procol]
	featuredct = calFeature(matrix,feacol)
	#get top 15
	featureIndex = getTop(featuredct,int(sys.argv[1]))
	new_trainlst = selectIndex(pw_trainlst,featureIndex)
	outFile(new_trainlst,'GENIA-CRF-TRAIN-5-' +sys.argv[1] +'.txt')

	new_testlst = selectIndex(pw_testlst,featureIndex)
	outFile(new_testlst,'GENIA-CRF-TEST-5-' +sys.argv[1] +'.txt')
	endtime = time.time()
	print endtime-starttime
