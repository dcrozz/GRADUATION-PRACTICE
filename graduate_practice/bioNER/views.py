#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
#from .forms import AddForm
import nltk
import re

def index(request):
    return render(request, 'home.html')

def process(request):
#实现分词
    NERtext = request.GET['NERtext2']
    sens = nltk.sent_tokenize(NERtext)
    words = []
    for sent in sens:
        words+=nltk.word_tokenize(sent)
    #  dct= {itm:0 for itm in words}
    output = featureExtract(words)
    rna_result = featureSelect(output)
    return JsonResponse(rna_result,safe=False)

def featureExtract(lst):
    POSTagsList = getPOSTags(lst)
    outlst = []
    i = 0
    for token in lst:
        tempList =[]
	tempList.append(token)
	tempList.append(POSTagsList[i])
	tempList.append(getRegExBool ("\-", token))			#Hyphen in token
	tempList.append(getRegExBool (",", token))			#Comma in token
	tempList.append(getRegExBool ("[A-Z]", token))			#Cap letter in token
	tempList.append(getRegExBool ("[0-9]", token))			#Number in token
	tempList.append(getRegExBool ('\\\\', token))			#Backslash in token
	tempList.append(getRegExBool (":", token))			#Colon in token
	tempList.append(getRegExBool (";", token))			#Semicolon in token
	tempList.append(getRegExBool ('\[', token))			#Bracket in token (note I assume that if left bracket occurs then right bracket also occurs)
	tempList.append(getRegExBool ('\(', token))			#Parenthese in token (note I assume that if left Paren occurs then right Paren also occurs)
	tempList.append(getWordShape(token))
	tempList.append(getRegExNoCaseBool ('alpha|beta|gamma|delta|epsilon|zeta|theta|kappa|lambda', token))			#GreekLetter in token
	tempList.append(getRegExNoCaseBool ('rna', token))																#RNA in token
	tempList.append(getRegExNoCaseBool ('cell', token))																#Cell letter in token
	tempList.append(getRegExNoCaseBool ('gene', token))																#Gene in token
	tempList.append(getRegExNoCaseBool ('jurkat', token))															#Jurkat in token
	tempList.append(getRegExNoCaseBool ('transcript', token))														#Transcript in token
	tempList.append(getRegExNoCaseBool ('factor', token))															#Factor in token
	tempList.append(getRegExNoCaseBool ('prot|mono|nucle|integr|macro|il\-', token))								#Common string associated with RNA, DNA, etc
	tempList.append(getRegExNoCaseBool ('alpha|beta|gamma|delta|epsilon|zeta|theta|kappa|lambda|rna|cell|gene|jurkat|transcript|factor|prot|mono|nucle|integr|macro|il\-' , token))			#Any above mentioned Lexical features
	tempList.append(getCapLetterByselfBool(token))
        outlst.append(tempList)
    return outlst

def getPOSTags(token):
	POSTagsTuple = nltk.pos_tag(token)			
	POSTagsList = []
	for item in POSTagsTuple:
		POSTagsList.append(item[1])
	return POSTagsList							
###### Generic RegEx test and return 0 or 1 to print to file ####
def getRegExBool (regex, token):
	return int(bool(re.search(regex,token)))

###### Generic "Ignore case" of letters RegEx test and return 0 or 1 to print to file ####
def getRegExNoCaseBool (regex, token):
	return int(bool(re.search(regex, token, flags = re.IGNORECASE)))
	
def getWordShape(token):
	wordShape = re.sub('[A-Z]', 'A', token, flags=0)
	wordShape = re.sub('[a-z]', 'a', wordShape, flags=0)	
	wordShape = re.sub('aaaa+', 'aaa', wordShape, flags=0)	
	wordShape = re.sub('[0-9]', 'd', wordShape, flags=0)
	wordShape = re.sub('\W', '_', wordShape, flags=0)

	return wordShape
#####  IS Capital Letter by itself?   #####
def getCapLetterByselfBool(token):
	#returns bool 1 for true if token is an individual capital letter
	if len(token) == 1 and re.match( '[A-Z]' , token , flags = 0):
		return 1
	else:
		return 0

def loadFeatures(file_name):
    dct = {}
    with open(file_name) as f:
        for line in f.readlines():
            cur_line = line.strip().split('\t')
            dct[cur_line[0]] = cur_line[1]
    return dct

def featureSelect(lst):
    featuresdct = loadFeatures('bioNER/static/totalfeatures.txt')
    new_lst = changePOSandWS(lst,featuresdct)
    rnafeaturedct = loadFeatures('bioNER/static/selectedfeatures-20-RNA-protein.txt')
    dnafeaturedct = loadFeatures('bioNER/static/selectedfeatures-20-DNA-protein.txt')
    cellfeaturedct = loadFeatures('bioNER/static/selectedfeatures-20-DNA-protein.txt')
    rna_lst =[]
    dna_lst =[]
    cell_lst =[]
    for itm in new_lst:
        tmp =[]
        tmp.append(itm[0])
        for index in rnafeaturedct.itervalues():
            tmp.append(itm[int(index)])
        rna_lst.append(tmp)
    for itm in new_lst:
        tmp =[]
        tmp.append(itm[0])
        for index in dnafeaturedct.itervalues():
            tmp.append(itm[int(index)])
        dna_lst.append(tmp)
    for itm in new_lst:
        tmp =[]
        tmp.append(itm[0])
        for index in cellfeaturedct.itervalues():
            tmp.append(itm[int(index)])
        cell_lst.append(tmp)
    dnamodel = 'bioNER/static/model-5-20-DNA-protein'
    rnamodel = 'bioNER/static/model-5-20-RNA-protein'
    cellmodel = 'bioNER/static/model-5-20-cell-cell'
    rnatag = crfTest(rna_lst,rnamodel)
    rnaresult = []
    for i in range(len(rna_lst)):
        tmp = [ rna_lst[i][0],rnatag[i] ]
        rnaresult.append(tmp)
    return rnaresult
   
def changePOSandWS(lst,featuredct):
	new_lst = []
	for x in lst:
                pos = x[1]
                ws = x[11]
                x = x[:1] + [0 for i in range(44)] + x[2:11] + [0 for j in range(1589)] + x[12:]
		try:
			tmp = featuredct[x[1]]
			x[tmp] = '1'
		except KeyError:
			pass
		try:
			tmp = featuredct[x[11]]
			x[tmp] = '1'
		except KeyError:
                        pass
		# ipdb.set_trace()
		new_lst.append(x)
	return new_lst
import CRFPP
def crfTest(lst,model):
    tagger = CRFPP.Tagger("-m" + model)
    #tagger = CRFPP.Tagger("-m model-5-20-RNA-protein")
    for line in lst:
        tagger.add('\t'.join(map(str,line)))
    tagger.parse()
    ysize = tagger.ysize()
    size = tagger.size()
    xsize = tagger.xsize()
    taglst = [tagger.y2(i) for i in range(len(lst))]
    return taglst

