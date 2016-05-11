f = open('GENIA-CRF-TEST.txt')
lst = []
for line in f.readlines():
	cur_line = line.strip().split('\t')
	try:
		cur_line[2]
		lst.append(cur_line)
	except IndexError:
		pass

def labelChange(lst):
	for x in lst:
		tmp = x.pop()
		if tmp == 'B-DNA' or tmp == 'I-DNA':
			x.append('DNA')
		elif tmp == 'B-RNA' or tmp == 'I-RNA':
			x.append('RNA')
		elif tmp == 'B-cell_line' or tmp == 'I-cell_line':
			x.append('cell_line')
		elif tmp == 'B-cell_type' or tmp == 'I-cell_type':
			x.append('cell_type')
		elif tmp == 'B-protein' or tmp == 'I-protein':
			x.append('protein')
		elif tmp == 'O':
			x.append('0')
	return lst

lst = labelChange(lst)
with open('GENIA-CRF-TEST-5.txt','a') as f:
	for x in lst:
		f.write('\t'.join(x) + '\n')