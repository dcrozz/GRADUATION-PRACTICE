def getWord():
	with open('mod.txt') as raw:
		iob2lst = []
		states = {}
		transition_prob = {}
		emission_prob = {}
		lines = raw.readlines()
		for line in lines:
			cur_line = line.strip().split('\t')
			ne = cur_line[-2]
			nextne = cur_line[-1]
			word = cur_line[0].lower()
			states[ne] = states.get(ne,0) + 1
			if(transition_prob.has_key(ne)):
				transition_prob[ne][nextne] = transition_prob[ne].get(nextne,0) + 1
			else:
				transition_prob[ne] = {} 	
			if(emission_prob.has_key(ne)):
				emission_prob[ne][word] = emission_prob[ne].get(word,0) +1
			else:
				emission_prob[ne] = {}

		for itm in transition_prob:
			for state in states:
				if transition_prob[itm].has_key(state):
					pass
				else:
					transition_prob[itm][state]=0

	start_prob = {}
	with open('ori.txt') as raw:
		tmp = []
		lines = raw.readlines()
		for line in lines:
			cur_line = line.strip().split('\t')
			tmp.append(cur_line)
	i = 0
	for line in tmp[:-2]:
		if line == ['']:
			start_prob[tmp[i+1][-1]] = start_prob.get(tmp[i+1][-1],0) + 1
		i += 1
	start_prob[tmp[0][-1]] = start_prob.get(tmp[0][-1]) +1

	caldct(start_prob)
	for state in states:
		if start_prob.has_key(state) == False:
			start_prob[state] = 0

	for item in transition_prob.iterkeys():
		caldct(transition_prob[item])
	for item in emission_prob.iterkeys():
		caldct(emission_prob[item])
	return states, start_prob, transition_prob, emission_prob

def caldct(dct):
	sum = 0
	for item in dct.itervalues():
		sum = sum + item
	for item in dct.iterkeys():
		dct[item] = dct.get(item) *1.0 / sum

def print_dptable(V):
    print "    ",
    for i in range(len(V)): print "%7d" % i,
    print

    for y in V[0].keys():
        print "%.5s: " % y,
        for t in range(len(V)):
            print "%.7s" % ("%f" % V[t][y]),
        print

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
    obs = map(str.lower,obs)

    # Initialize base cases (t == 0)
    for y in states:
        if emit_p[y].has_key(obs[0]):
            # pdb.set_trace()
            V[0][y] = start_p[y] * emit_p[y][obs[0]]
            path[y] = [y]
        else:
            V[0][y] = 0
            path[y] = [y]
    # pdb.set_trace()

    # Run Viterbi for t > 0
    for t in range(1,len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (prob, state) = max([ (0,y0) if emit_p[y].has_key(obs[t]) == False else (V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0)  for y0 in states])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        # Don't need to remember the old paths
        path = newpath
        # pdb.set_trace()

    # print_dptable(V)
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

def input():
	with open('Genia4EReval1.iob2') as raw:
		testword = [[]]
		testne = [[]]
		lines = raw.readlines()
		for line in lines:
			cur_line = line.strip().split('\t')
			if cur_line == ['']:
				testword.append([])
				testne.append([])
			else:
				testword[-1].append(cur_line[0].lower())
				testne[-1].append(cur_line[-1])
		return testword,testne


# def example():
observation, testne = input()
calne = [[]]
states, start_prob, transition_prob, emission_prob = getWord()
for obs in observation:
	calne[-1] = viterbi(obs,states,start_prob,transition_prob,emission_prob)[-1]
	calne.append([])
calne.pop()

###########################################
#compare calne & testne


# for itm in f.readlines():
# 	cur_line = itm.strip().split('\t')
# 	lst.append(itm)


ver_A = []
ver_B = []
ver_C = []
ver_D = []
#把result读到lst里
#x[4]是正确值，x[5]是计算值
# tmp1 = [x[-2] for x in lst]
# tmp1 = []
# tmp2 = []
for x in lst:
	try:
		tmp1.append(x[-2])
	except IndexError:
		pass
# tmp2 = [x[-1] for x in lst]
for x in lst:
	try:
		if x[2]:
			tmp2.append(x[-1])
	except IndexError:
		pass
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
test_cal = reduce(list.__add__,calne)
test_tes = reduce(list.__add__,testne)
vallst = map(evaluate,test_tes,test_cal)
recall = vallst.count('A')*1.0/(vallst.count('A')+vallst.count('C'))
accuracy = vallst.count('A')*1.0/(vallst.count('A')+vallst.count('B'))
# test_cal = reduce(list.__add__,calne)
# test_tes = reduce(list.__add__,testne)
# vallst = map(evaluate,test_tes,test_cal)
# recall = vallst.count('A')*1.0/(vallst.count('A')+vallst.count('C'))
# accuracy = vallst.count('A')*1.0/(vallst.count('A')+vallst.count('B'))
# set([x[0] for x in ver_C])
# count_lst = {}
# for itm in set([x[0] for x in ver_C]):
#     count_lst[itm] = [x[0] for x in ver_C].count(itm)
matrix = {}
ne = set(test_cal)
for itm in ne:
	matrix[itm] = {x:0 for x in  ne}
lst = zip(test_tes,test_cal)

for itm in lst:
	matrix[itm[0]][itm[1]] += 1

# # to excel draw a pic
# for itm in matrix:
# 	sum =  reduce()

#
#count_lst = {}
#for itm in set(test_cal):
    # count_lst[itm] = test_cal.count(itm)
"""
recall 41.15%


 '''
 result 1 
 67.51%

 result 2
 66.6%
'''