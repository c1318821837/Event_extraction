#_*_ coding:utf-8 -*-
from fastHan import FastHan
import re
from py2neo import Graph,Node,Relationship
model=FastHan()

#实现文章的切分，将文章切分为句子存储
def eassy_cut(content):
	sentences = re.split(r'(\.|\!|\?|。|！|？|\.{6})', content)
	for item in sentences[:]:
		if item=='。':
			sentences.remove(item)
	return sentences

#识别时间时间
def event_time(content):
	answer=model(content,target="Parsing")
	an=answer[0]
	eventtime=''
	for item in an:
		if item[3]=='NT':
			if '年'in item[0]:
				eventtime=eventtime+item[0]
			if '月' in item[0]:
				eventtime = eventtime + item[0]
			if '日' in item[0]:
				eventtime = eventtime + item[0]
	return eventtime

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
#未找到主语就进行主语插入，插入位置为root前
def insert_subject(answer):
	an = answer[0]
	i=0
	for item in an:
		if item[2]=='root':
			an.insert(i,['雷军',2,'nsubj','NR'])
			break
		i=i
	return an

#找到宾语（当前只记录直接宾语）
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

#识别实体，记录主语和直接宾语，i为主语位置使用find_subject查找
def entity_recogition(answer):
	entity=[]
	re=find_answer(answer)
	print('re为')
	print(re)
	if re:
		an=re[0]
	else:
		entity.append(None)
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

#如果实体寻找错误，就更正实体
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

#删除不需要的实体和事件
def del_falsesubject(answer,i):
	an=answer[0]
	for index in range(i):
		an.pop(0)
	if an:
		an.pop(0)
	return an

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



content='受《硅谷之火》中创业故事影响，在大学四年级的时候，雷军开始和同学王全国、李儒雄等人创办三色公司。当时的产品是一种仿制金山汉卡，可是随后出现一家规模比他们更大的公司，把他们的产品盗版了，而且这家公司可以把同类的产品做得量更大，价格也更低。三色公司度日维艰，不要说公司运营，即使他们生活上也面临着等无米下锅的局面。半年以后，三色公司决定解散。清点公司资产时，雷军和王全国分到了一台286电脑和打印机，李儒雄分到了一台386电脑。在三色公司工作期间，雷军与王全国合作编写了雷军的第一个正式作品BITLOK 加密软件并组建了黄玫瑰小组；除此还用PASCAL编写免疫90，此产品获得了湖北省大学生科技成果一等奖。'
content=content.replace('他','雷军')
sentences = eassy_cut(content)
del(sentences[-1])
print(sentences)
knowg=[]
for item in sentences:
	answer=model(item,target="Parsing")
	print(answer)
	an = answer[0]
	ann = entity_recogition(answer)
	knowg.append(ann)
print(knowg)


