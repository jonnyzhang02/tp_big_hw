'''
Author: jonnyzhang02 71881972+jonnyzhang02@users.noreply.github.com
Date: 2023-06-01 14:43:44
LastEditors: jonnyzhang02 71881972+jonnyzhang02@users.noreply.github.com
LastEditTime: 2023-06-02 08:43:35
FilePath: /tp_big_hw/neo4j_db.py
Description: coded by ZhangYang@BUPT, my email is zhangynag0207@bupt.edu.cn
'''
from neo4j import GraphDatabase
import pandas as pd

uri = "bolt://localhost:7687" # Neo4j数据库地址
driver = GraphDatabase.driver(uri, auth=("neo4j", "12345678")) # 用户名和密码

df = pd.read_csv('./triplets.csv') # CSV文件路径

def add_data(tx, entity1, relation, entity2):
    tx.run("MERGE (e1:Entity { name: $entity1 }) "
           "MERGE (e2:Entity { name: $entity2 }) "
           "MERGE (e1)-[r:RELATIONSHIP { name: $relation }]->(e2)",
           entity1=entity1, relation=relation, entity2=entity2)

with driver.session() as session:
    for index, row in df.iterrows():
        session.execute_write(add_data, row['subject'], row['relation'], row['object'])

driver.close()


