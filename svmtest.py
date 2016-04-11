# import 
infile = open('/Users/alex/Documents/Semester7/毕设/毕业设计/word tag pos')
# infile = open('/Users/alex/Documents/Semester7/毕设/毕业设计/test')
datalst = []
labellst = []
posdct = {}
blockdct = {}

def word2asc(word):
    asclst = map(ord,word)
    tmp = map(str,asclst)
    return int(''.join(tmp))
i = 0
j = 0
for line in infile.readlines():
	cur_line = line.strip().split('\t')
	labellst.append(cur_line[-1])
	datalst.append([word2asc(cur_line[0]),word2asc(cur_line[1])])
	if cur_line[2] in posdct:
		datalst[-1].append(posdct[cur_line[2]])
	else:
		posdct[cur_line[2]] = i
		datalst[-1].append(i)
		i += 1
	if cur_line[3] in blockdct:
		datalst[-1].append(blockdct[cur_line[3]])
	else:
		blockdct[cur_line[3]] = i
		datalst[-1].append(j)
		j += 1

trainlst = datalst[:9000]
testlst = datalst[9000:]

from sklearn.svm import SVC
clf = SVC()
clf.fit(trainlst, labellst[:9000])

testout = clf.predict(testlst)

def matchlst(itm1,itm2):
	if itm1 == itm2:
		return 0
	else:
		return 1
output = map(matchlst,testout,labellst[9000:])


# 92039
