from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
import csv

# 创建一个命名空间，所有实体都将在这个命名空间下
n = Namespace("http://zy2020212185.org/people/")

# 创建一个空的图
g = Graph()

# 读取CSV文件并转换为RDF数据
with open('triplets.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过列名
    for row in csv_reader:
        subject, relation, object = row
        # 使用命名空间和实体创建URI
        subject_uri = n[subject]
        object_uri = n[object]
        # 根据关系创建谓词
        relation_uri = URIRef("http://zy2020212185.org/relation/" + relation)
        # 添加三元组到图中
        g.add((subject_uri, relation_uri, object_uri))

# 将图序列化为RDF/XML数据格式并写入文件
g.serialize(destination='output.rdf', format='xml')
