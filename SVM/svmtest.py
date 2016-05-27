#coding:utf-8
import sys
# infile = open('GENIA-CRF-TRAIN.txt')
# testfile = open('GENIA-CRF-TEST.txt')


def inFile(filename):
	lst = []	
	with open(filename) as f:
		for line in f.readlines():
			cur_line = line.strip().split('\t')
			try:
				cur_line[2]
				lst.append(cur_line[1:])
			except IndexError:
				pass
	return lst
def outFile(lst,filename):
	with open(filename,'a') as f:
		for line in lst:
			# try:
			f.write('\t'.join(map(str,line)) + '\n')

trainlst = inFile(sys.argv[1])
testlst = inFile(sys.argv[2])
labellst = [x[-1] for x in trainlst]

from sklearn.svm import SVC
clf = SVC()
clf.fit([x[:-1] for x in trainlst], labellst)

testout = clf.predict(testlst)
testlst = [ x+[y] for x,y in zip(testlst,testout)]
outFile(testlst,sys.argv[3])