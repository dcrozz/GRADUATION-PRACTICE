def getFile(filename):
	lst = []	
	with open(filename) as f:
		#for test modify the line to 10
		for line in f.readlines():
			cur_line = line.strip().split('\t')
			try:
				cur_line[2]	
				lst.append([cur_line[0]] + cur_line[-2:])
			except IndexError:
				pass
	return lst

def mergeClassifier(lst):
	newlst = []
	for itm in lst:
		tmp = []
		if itm[0][-2] == '0' and itm[1][-2] == '0' and itm[2][-2] == '0':
			tmp= itm[0]
		elif itm[0][-2] != '0':
			tmp = itm[0]
		elif itm[1][-2] != '0':
			tmp = itm[1]
		elif itm[2][-2] != '0':
			tmp = itm[2]

		if itm[0][-1] == '0' and itm[1][-1] == '0' and itm[2][-1] == '0':
			pass
		elif itm[0][-1] != '0':
			tmp[1]=itm[0][-1]
		elif itm[1][-1] != '0':
			tmp[1]=itm[1][-1]
		elif itm[2][-1] != '0':
			tmp[2]=itm[2][-1]
		newlst.append(tmp)
	return newlst
		


def outFile(lst,filename):
	with open(filename,'a') as f:
		for line in lst:
			# try:
			f.write('\t'.join(map(str,line)) + '\n')

rna_pro = getFile('result_file_RNA-protein')
cell = getFile('result_file-5-20-cell_type-cell_line')
dna_pro =getFile('result_file-20-DNA-protein')
mergelst = zip(rna_pro,cell,dna_pro)
newlst = mergeClassifier(mergelst)
outFile(newlst,'result_file_merged')
