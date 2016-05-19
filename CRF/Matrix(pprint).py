import pprint
import sys
lst = []
infile = open(sys.argv[1])
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
pprint.pprint(matrix)
#with open(sys.argv[1]+'_matrix','w') as f:
#	for x in matrix:
#
	
