lst = []
infile = open('result_file2')
for line in infile:
	try:
		cur_line = line.strip().split('\t')
		cur_line[2] + ''
		lst.append(cur_line[-2:])
	except IndexError:
		pass


matrix = {}
ne = set([x[-1]for x in lst])
for itm in ne:
	matrix[itm] = {x:0 for x in  ne}



for itm in lst:
	matrix[itm[0]][itm[1]] += 1

# to excel draw a pic
for itm in matrix:
	sum =  reduce()


