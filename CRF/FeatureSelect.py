"""
Feature Selection by Chi measure that can control numbers of labels
example:
py filename feature_number label1 label2


To be done (any amount of label)
"""
#coding:utf-8
def getFile(filename,label1,label2):
	lst = []	
	with open(filename) as f:
		#for test modify the line to 10
		for line in f.readlines():
			cur_line = line.strip().split('\t')
			try:
				cur_line[2]	
				if cur_line[-1] != label1 and cur_line[-1] != label2:
					cur_line.pop()
					cur_line.append('0')
					lst.append(cur_line)
				else:
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
	try:
		dnacol = reduce(listAdd,dnalst)
	except TypeError:
		dnacol = []
	try:
		rnacol = reduce(listAdd,rnalst)
	except TypeError:
		rnacol = []
	try:
		linecol = reduce(listAdd,linelst)
	except TypeError:
		linecol = []
	try:
		typecol = reduce(listAdd,typelst)
	except TypeError:
		typecol = []
	try:
		procol = reduce(listAdd,prolst)
	except TypeError:
		procol = []
	feacol = reduce(listAdd,[dnacol,rnacol,linecol,typecol,procol])
	return dnacol,rnacol,linecol,typecol,procol,feacol

def listAdd(a,b):
	if a==[] or b==[]:
		if a==[]:
			return b
		else:
			return a
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
	fealen = max([len(i) for i in matrix])
	for j in range(fealen):
		Sigma = 0
		for i in matrix:
			if len(i) < fealen:
				continue
			else:
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
		new = [line[0]] + [line[a+1] for a in indexlst] + [line[-1]]
		newlst.append(new)
	return newlst

def outFile(lst,filename):
	with open(filename,'a') as f:
		for line in lst:
			# try:
			f.write('\t'.join(map(str,line)) + '\n')
			# except TypeError:
				# pass

def outSeq(wsdct,posdct,filename):
	'''create a file that indicates the index of each feature'''
	lenws = len(wsdct)
	lenpos = len(posdct)
	defaultdct = {
'___token':0,
'___pos':1,
'___\-':2,
'___,':3,
'___[A-Z]':4,
'___[0-9]':5,
'___\\\\':6,
'___:':7,
'___;':8,
'___\[':9 ,
'___\(':10,
'___word_shape':11,
'___alpha|beta|':12,
'___rna':13,
'___cell':14,
'___gene':15,
'___jurkat':16,
'___transcript':17,
'___factor':18,
'___prot|mono|nucle|integr|il\-':19,
'___alpha|beta|...|il\-':20,
'___indivdualCapLetter':21,
'___Label':22,
	}
	for itm in defaultdct.keys():
		if defaultdct[itm]>=2 and defaultdct[itm] <11:
			defaultdct[itm] += lenpos -1 
		elif defaultdct[itm]>11:
			defaultdct[itm] += lenpos + lenws -1 
	totaldct = dict(defaultdct.items()+wsdct.items()+posdct.items())
	totaldct.pop('___pos')
	totaldct.pop('___word_shape')
	outlst = sorted(totaldct.items(),key=lambda d: d[1])
	with open(filename,'a') as f:
		for itm in outlst:
			f.write(itm[0] + '\t' + str(itm[1]) + '\n')
	return dict(outlst)
def outFea(feaIndex,totalfea,filename):
	with open(filename,'a') as f:
		for index in feaIndex:
			for feature in totalfea.keys():
				if totalfea[feature]+1 == index:
					f.write(feature +'\t'+str(totalfea[feature])+'\n')

if __name__ == "__main__":
	import sys
	import time 
	import ipdb
	starttime = time.time()
	trainlst = getFile('GENIA-CRF-TRAIN-5.txt',sys.argv[2],sys.argv[3])
	testlst = getFile('GENIA-CRF-TEST-5.txt',sys.argv[2],sys.argv[3])
	#trainlst = getFile('GENIA-CRF-TRAIN-5.txt','DNA','protein')
	#testlst = getFile('GENIA-CRF-TEST-5.txt','DNA','protein')

	nedct={}
	ne = set([x[-1] for x in trainlst])
	nedct = {x for x in ne}
	posdct={}
#mod is used to set the feature dict
	pos = set(x[1] for x in trainlst)
	posdctmod = {x:y for x,y in zip(pos,range(1,len(pos)+1))}  
	posdct = {x:y for x,y in zip(pos,range(len(pos)))}  
	ws = set([x[11] for x in trainlst])
	wsdctmod = {x:y for x,y in zip(ws,range(len(pos)+10,len(ws)+10+len(pos)))} 
	wsdct = {x:y for x,y in zip(ws,range(len(ws)))}
	
	totalfeadct = outSeq(wsdctmod,posdctmod,'totalfeatures'+'-'+sys.argv[2]+'-'+sys.argv[3]+'.txt')
	#totalfeadct = outSeq(wsdctmod,posdctmod,'totalfeatures')
	pw_trainlst = changePOSandWS(trainlst,posdct,wsdct)
	pw_testlst = changePOSandWS(testlst,posdct,wsdct)
	dnacol,rnacol,linecol,typecol,procol,feacol = featureSelect(pw_trainlst)
	#add the colname
	matrix = [dnacol,rnacol,linecol,typecol,procol]
#the feature dict with chi value
	featuredct = calFeature(matrix,feacol)
	#get top 15
	featureIndex = getTop(featuredct,int(sys.argv[1])) # the index of feature finally selected
	new_trainlst = selectIndex(pw_trainlst,featureIndex)
	outFea(featureIndex,totalfeadct,'selectedfeatures'+'-'+sys.argv[1]+'-'+sys.argv[2]+'-'+sys.argv[3]+'.txt')
	outFile(new_trainlst,'GENIA-CRF-TRAIN-5-' + sys.argv[1] + '-' + sys.argv[2] + '-' + sys.argv[3]  +'.txt')

	new_testlst = selectIndex(pw_testlst,featureIndex)
	outFile(new_testlst,'GENIA-CRF-TEST-5-' + sys.argv[1] + '-' + sys.argv[2] + '-' + sys.argv[3]  +'.txt')
	endtime = time.time()
	print endtime-starttime
