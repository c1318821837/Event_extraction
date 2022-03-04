from py2neo import Graph,Node,Relationship
# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph('http://localhost:7474',auth=('neo4j','xx1314'))
a = Node('Person',name='bubu')
graph.create(a)
b = Node('Person',name='kaka')
graph.create(b)
r = Relationship(a,'KNOWS',b)
graph.create(r)