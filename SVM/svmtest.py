# import 
infile = open('GENIA-CRF-TRAIN.txt')
testfile = open('GENIA-CRF-TEST.txt')
# infile = open('/Users/alex/Documents/Semester7/毕设/毕业设计/test')
trainlst = []
testlst = []
labellst = []
testlabellst = []
posdct = {}
# blockdct = {}

def word2asc(word):
    asclst = map(ord,word)
    tmp = map(str,asclst)
    return int(''.join(tmp))
i = 0
j = 0


for line in infile.readlines():
	cur_line = line.strip().split('\t')
	try:
		cur_line[2] + ''
		trainlst.append([word2asc(cur_line[0])])
		if cur_line[1] in posdct:
			trainlst[-1].append(posdct[cur_line[1]])
		else:
			posdct[cur_line[1]] = i
			trainlst[-1].append(i)
			i += 1
		trainlst[-1].extend(map(int,cur_line[2:11]))
		trainlst[-1].append(word2asc(cur_line[11]))
		trainlst[-1].extend(map(int,cur_line[12:-1]))
		labellst.append(cur_line[-1])


		# if cur_line[3] in blockdct:
		# 	datalst[-1].append(blockdct[cur_line[3]])
		# else:
		# 	blockdct[cur_line[3]] = i
		# 	datalst[-1].append(j)
		# 	j += 1
	except IndexError:
		pass

i = 0
j = 0


for line in testfile.readlines():
	cur_line = line.strip().split('\t')
	try:
		cur_line[2] + ''
		testlst.append([word2asc(cur_line[0])])
		if cur_line[1] in posdct:
			testlst[-1].append(posdct[cur_line[1]])
		else:
			posdct[cur_line[1]] = i
			datalst[-1].append(i)
			i += 1
		testlst[-1].extend(map(int,cur_line[2:11]))
		testlst[-1].append(word2asc(cur_line[11]))
		testlst[-1].extend(map(int,cur_line[12:-1]))
		testlabellst.append(cur_line[-1])
	except IndexError:
		pass


from sklearn.svm import SVC
clf = SVC()
clf.fit(trainlst, labellst)

testout = clf.predict(testlst)



ver_A = []
ver_B = []
ver_C = []
ver_D = []
#把result读到lst里
#x[4]是正确值，x[5]是计算值
# tmp1 = [x[-2] for x in lst]
def evaluate(a,b):
	#return map(lambda x,y: x == y ,a,b)
	if a != 'O' and a == b:
		return 'A'
	elif a == 'O' and a == b:
		ver_B.append([a,b])
		return 'B'
	elif a != 'O' and a != b:
		ver_C.append([a,b])
		return 'C'
	elif a == 'O' and a !=b:
		return 'D'
vallst = map(evaluate,testlabellst,testout)

recall = vallst.count('A')*1.0/(vallst.count('A')+vallst.count('C'))
accuracy = vallst.count('A')*1.0/(vallst.count('A')+vallst.count('B'))

# recall = 0.395322
# 92039
