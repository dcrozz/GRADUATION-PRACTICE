ver_A = []
ver_B = []
ver_C = []
ver_D = []
#把result读到lst里
#x[4]是正确值，x[5]是计算值
# tmp1 = [x[-2] for x in lst]
tmp1 = []
tmp2 = []
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
test_cal = reduce(list.__add__,tmp1)
test_tes = reduce(list.__add__,tmp2)
vallst = map(evaluate,tmp1,tmp2)
recall = vallst.count('A')*1.0/(vallst.count('A')+vallst.count('C'))
accuracy = vallst.count('A')*1.0/(vallst.count('A')+vallst.count('B'))
