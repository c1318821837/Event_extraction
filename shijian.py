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
#未找到主语就进行主语插入，插入位置为root前
def insert_subject(answer):
	an = answer[0]
	i=0
	for item in an:
		if item[2]=='root':
			an.insert(i,['杜甫',2,'nsubj','NR'])
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
	if re:
		an=re[0]
	else:
		entity.append(None)
	index=find_subject(re)
	if index==None:
		entity.append(None)
	else:
		entity.append(an[index][0])
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
	if index != None and rindex != None:
		for item in an:
			if i<index and i>rindex:
				if item[2]=='nn':
					connect.append(item[0])
			i=i+1
		connect.append(an[index][0])
	for item in connect:
		con=con+item
	return con



content='开元十九年（731年），十九岁的杜甫出游郇瑕（今山西临猗) 。二十岁时，杜甫漫游吴越，历时数年。开元二十三年（735年），杜甫回故乡参加“乡贡”。开元二十四年（736年），杜甫在洛阳参加进士考试，结果落第。杜甫的父亲时任兖州司马一职，杜甫于是赴兖州省亲，与苏源明等一起，到齐赵平原，作第二次漫游。大概这时他父亲正在兖州做司马，他在齐赵一带过了四五年“裘马轻狂”的“快意”生活，也留下了现存最早的几首诗：《登兖州城楼》，是省侍父亲于兖州时的作品；还有《画鹰》《房兵曹胡马》两首，以青年人的热情歌颂了雄鹰和骏马；还有一首《望岳》，更是其中的杰作，结尾的两句是流传千古的名句：“会当凌绝顶，一览众山小”，流露了诗人少年时代不平凡的抱负。天宝三载（744年）四月，杜甫在洛阳与被唐玄宗赐金放还的李白相遇，两人相约同游梁、宋（今河南开封、商丘一带）。会见了诗人高适，这是第三次漫游。之后，杜甫又到齐州（今山东济南）。天宝四载（745年），他在齐鲁又与李白相见，在饮酒赋诗之外，又讨论了炼丹求仙，而且共同访问了兖州城北的隐士范野人。'
content=content.replace('他','杜甫')
sentences = eassy_cut(content)
del(sentences[-1])
#print(sentences)
knowg=[]
graph = Graph('http://localhost:7474',auth=('neo4j','xx1314'))
a = Node('Person',name='杜甫')
graph.create(a)
for item in sentences:
	answer=model(item,target="Parsing")
	an = answer[0]
	ann = entity_recogition(answer)
	knowg.append(ann)
	b = Node('Entity', name=ann[2])
	graph.create(b)
	r = Relationship(a, ann[1], b)
	graph.create(r)

