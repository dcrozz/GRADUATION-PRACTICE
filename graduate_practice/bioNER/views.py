#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
#from .forms import AddForm
import nltk
import re

def index(request):
#    if request.method == 'POST':# 当提交表单时
#        form = AddForm(request.POST) # form 包含提交的数据
#         
#        if form.is_valid():# 如果提交的数据合法
#            a = form.cleaned_data['a']
#            b = form.cleaned_data['b']
#            return HttpResponse(str(int(a) + int(b)))
#     
#    else:# 当正常访问时
#        form = AddForm()
    return render(request, 'home.html')

def add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a+b))

def process(request):
#实现分词
    NERtext = request.GET['NERtext2']
    sens = nltk.sent_tokenize(NERtext)
    words = []
    for sent in sens:
        words+=nltk.word_tokenize(sent)
    #  dct= {itm:0 for itm in words}
    output = featureExtract(words)
    rna_lst,dna_lst,cell_lst = featureSelect(output)
    return JsonResponse(rna_lst,safe=False)

def ajax_list(request):
    a = range(100)
    return JsonResponse(a,safe=False)
def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return JsonResponse(name_dict)


def featureExtract(lst):
    POSTagsList = getPOSTags(lst)
    outlst = []
    i = 0
    for token in lst:
        tempList =[]

	#append token and POSTags
	tempList.append(token)
	tempList.append(POSTagsList[i])

	#append orographic features
	#These features were extracted by almost all research groups in the shared task project
	#very straightforward.  I use regular expressions to test
	tempList.append(getRegExBool ("\-", token))			#Hyphen in token
	tempList.append(getRegExBool (",", token))			#Comma in token
	tempList.append(getRegExBool ("[A-Z]", token))			#Cap letter in token
	tempList.append(getRegExBool ("[0-9]", token))			#Number in token
	tempList.append(getRegExBool ('\\\\', token))			#Backslash in token
	tempList.append(getRegExBool (":", token))			#Colon in token
	tempList.append(getRegExBool (";", token))			#Semicolon in token
	tempList.append(getRegExBool ('\[', token))			#Bracket in token (note I assume that if left bracket occurs then right bracket also occurs)
	tempList.append(getRegExBool ('\(', token))			#Parenthese in token (note I assume that if left Paren occurs then right Paren also occurs)

	#append word shape features
	tempList.append(getWordShape(token))

	#append Lexical features
	#Based on review of the GENIA training and test data, as well as review of papers in the shared task...
	# I have added the following lexical binary features.  These words are strongly correlated with IOB tags
	# for instance RNA and transcript are frequently associated with and RNA tag
	tempList.append(getRegExNoCaseBool ('alpha|beta|gamma|delta|epsilon|zeta|theta|kappa|lambda', token))			#GreekLetter in token
	tempList.append(getRegExNoCaseBool ('rna', token))																#RNA in token
	tempList.append(getRegExNoCaseBool ('cell', token))																#Cell letter in token
	tempList.append(getRegExNoCaseBool ('gene', token))																#Gene in token
	tempList.append(getRegExNoCaseBool ('jurkat', token))															#Jurkat in token
	tempList.append(getRegExNoCaseBool ('transcript', token))														#Transcript in token
	tempList.append(getRegExNoCaseBool ('factor', token))															#Factor in token
	tempList.append(getRegExNoCaseBool ('prot|mono|nucle|integr|macro|il\-', token))								#Common string associated with RNA, DNA, etc
	tempList.append(getRegExNoCaseBool ('alpha|beta|gamma|delta|epsilon|zeta|theta|kappa|lambda|rna|cell|gene|jurkat|transcript|factor|prot|mono|nucle|integr|macro|il\-' , token))			#Any above mentioned Lexical features


	#other features
	tempList.append(getCapLetterByselfBool(token))
        outlst.append(tempList)
    return outlst
def getPOSTags(token):
	#tagger returns a tuple containing original sentence tokens and POS tags
	POSTagsTuple = nltk.pos_tag(token)			
	POSTagsList = []

	#here the POSTags are taken from the tuple and converted to list
	for item in POSTagsTuple:
		POSTagsList.append(item[1])

	return POSTagsList							

	
###### Generic RegEx test and return 0 or 1 to print to file ####
def getRegExBool (regex, token):
	return int(bool(re.search(regex,token)))

###### Generic "Ignore case" of letters RegEx test and return 0 or 1 to print to file ####
def getRegExNoCaseBool (regex, token):
	return int(bool(re.search(regex, token, flags = re.IGNORECASE)))
	
########	WORD SHAPE 	###############
#I have created a word shape field as a way to normalize the tokens
#Pretty straight forward. Any cap letter is converted to 'A', lower case letters converted to 'a'
#strings of greater than 3 lower case characters are converted to 'aaa'
#digits converted to 'd' and any other character converted to '_'
#This is feature that is frequently applied by multiple research groups in the shared task
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
    return rna_lst,dna_lst,cell_lst
   
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
