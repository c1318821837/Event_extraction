#_*_ coding:utf-8 -*-
from array import *
import numpy
import numpy as np
from fastHan import FastHan
model=FastHan()
sentence="受《硅谷之火》中创业故事影响，在大学四年级的时候，雷军开始和同学王全国、李儒雄等人创办三色公司。"
def exchang_entinty(content):
	content.replace('杜甫','他')
	return content



#找到主语所在位置，如果找不到主语就进行主语补充
def find_subject(answer):
	an = answer[0]
	i=0
	for item in an:
		if item[2]=='nsubj':
			if an[i][0]=='雷军':
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
			if an[i][0]=='雷军':
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
			an.insert(i,['雷军',2,'nsubj','NR'])
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
	if re:
		an=re[0]
	else:
		entity=None
		return entity
	index=find_subject(re)
	if index==None:
		entity.append(None)
	else:
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
		if an[i][3] == 'NR':
			entity.append(an[i][0])
		else:
			entity.append(identify_nn(answer))
	return entity


def identify_nn(answer):
	an=answer[0]
	i=0
	con=""
	index=find_obj(answer)
	rindex=find_start(answer)
	connect=[]
	for item in an:
		if i<index and i>rindex:
			if item[2]=='nn':
				connect.append(item[0])
		i=i+1
	connect.append(an[index][0])
	for item in connect:
		con=con+item
	return con

answer=model(sentence,target="Parsing")
#print(answer)
an=answer[0]
sentence.replace('他','雷军')
print(answer)
print(identify_nn(answer))
print(entity_recogition(answer))
