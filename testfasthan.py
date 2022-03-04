#_*_ coding:utf-8 -*-
from array import *
import numpy
import numpy as np
from fastHan import FastHan
model=FastHan()
sentence="大概这时他父亲正在兖州做司马"
def exchang_entinty(content):
	content.replace('杜甫','他')
	return content



#找到主语所在位置，如果找不到主语就进行主语补充
def find_subject(answer):
	an = answer[0]
	i=0
	for item in an:
		if item[2]=='nsubj':
			if an[i][0]=='杜甫':
				return i
			else:
				index=find_falsesubject(answer,i)
				an=del_falsesubject(answer,index)
				sentence1 = ''
				for item in an:
					sentence1 = sentence1 + item[0]
				reanswer=model(sentence1,target="Parsing")
				i=find_subject(reanswer)
				return i
		i=i+1
		if i==len(an):
			an=insert_subject(answer)
			i=find_subject([an])
			return i
			break

def find_answer(answer):
	an = answer[0]
	i=0
	for item in an:
		if item[2]=='nsubj':
			if an[i][0]=='杜甫':
				return [an]
			else:
				index=find_falsesubject(answer,i)
				an=del_falsesubject(answer,index)
				sentence1 = ''
				for item in an:
					sentence1 = sentence1 + item[0]
				reanswer=model(sentence1,target="Parsing")
				i=find_subject(reanswer)
				return [an]
		i=i+1
		if i==len(an):
			an=insert_subject(answer)
			i=find_subject([an])
			return [an]
			break

def insert_subject(answer):
	#answer = model(content, target="Parsing")
	an = answer[0]
	i=0
	for item in an:
		if item[2]=='root':
			an.insert(i,['杜甫',2,'nsubj','NR'])
			break
		i=i+1
	return an

def find_falsesubject(answer,i):
	an=answer[0]
	exit_flag= False
	index=i
	for item in an[i:len(an)]:
		if index<=len(an) and item[2]=='punct':
			exit_flag=True
			break
		else:
			index = index + 1
		if exit_flag:
			break
	return index

def del_falsesubject(answer,i):
	an=answer[0]
	for index in range(i):
		an.pop(0)
	an.pop(0)
	return an


def find_obj(answer):
	an=answer[0]
	i=0
	for item in an:
		if item[2]=='dobj':
			return i
			break
		i=i+1


def find_start(answer):
	an=answer[0]
	i=0
	for item in an:
		if item[2]=='root':
			return i
			break
		i=i+1


def entity_recogition(answer):
	entity=[]
	re=find_answer(answer)
	print('re为')
	print(re)
	an=re[0]
	print(an)
	index=find_subject(answer)
	entity.append(an[index][0])
	print(index)
	sindex = find_start(re)
	if sindex==None:
		print(sindex)
		entity.append(None)
	else:
		entity.append(an[sindex][0])
	i=find_obj(re)
	if i == None:
		entity.append(None)
	else:
		entity.append(an[i][0])
	return entity

def event_re(answer):
	an=answer[0]
	event=[]



answer=model(sentence,target="Parsing")
#print(answer)
an=answer[0]
#sentence.replace('他','杜甫')
#con=exchang_entinty(sentence)
print(sentence.replace('他','杜甫'))

