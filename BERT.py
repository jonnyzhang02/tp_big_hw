'''
Author: jonnyzhang02 71881972+jonnyzhang02@users.noreply.github.com
Date: 2023-06-02 14:44:24
LastEditors: jonnyzhang02 71881972+jonnyzhang02@users.noreply.github.com
LastEditTime: 2023-06-07 16:20:58
FilePath: /tp_big_hw/BERT.py
Description: coded by ZhangYang@BUPT, my email is zhangynag0207@bupt.edu.cn
'''
import torch
from scipy.spatial.distance import cosine
from tqdm import tqdm   
import random

from transformers import BertModel, BertTokenizer
# 加载预训练的BERT模型和分词器
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# 将实体转换为BERT输入的形式
def get_bert_input(entity):
    inputs = tokenizer(entity, return_tensors="pt", max_length=20, truncation=True)
    return inputs

# 获取实体的BERT向量表示
def get_entity_embedding(entity, model):
    inputs = get_bert_input(entity)
    with torch.no_grad():
        outputs = model(**inputs)
    # 我们使用最后一层的[CLS]标记的隐藏状态作为实体的向量表示
    embeddings = outputs.last_hidden_state[:, 0, :].numpy()
    return embeddings.squeeze()  # 添加这行代码将2D张量转换为1D向量

# 计算两个实体的相似度
def calculate_similarity(entity1, entity2, model):
    embedding1 = get_entity_embedding(entity1, model)
    embedding2 = get_entity_embedding(entity2, model)
    # 计算余弦相似度
    similarity = 1 - cosine(embedding1, embedding2)
    return similarity

# 使用这个函数来计算实体的相似度
entity1 = "Apple"
entity2 = "苹果"
similarity = calculate_similarity(entity1, entity2, model)
print(f"The similarity between '{entity1}' and '{entity2}' is {similarity}.")


import pandas as pd

# 加载CSV文件
df = pd.read_csv('triplets.csv')

# 创建一个集合来存储所有的唯一实体
unique_entities = set(df['subject']).union(set(df['object']))

print("唯一实体的数量：",len(unique_entities))

unique_entities = random.sample(unique_entities, 1000)

# 创建一个字典来存储相似的实体
merged_entities = {}

def generate_entity_pairs(unique_entities):
    # 初始化一个空列表来存储实体对
    entity_pairs = []
    
    # 将集合转换为列表以便我们可以使用索引
    unique_entities_list = list(unique_entities)

    # 遍历每一个唯一实体
    for i in range(len(unique_entities_list)):
        for j in range(i + 1, len(unique_entities_list)):
            # 生成实体对，并添加到列表中
            entity_pairs.append((unique_entities_list[i], unique_entities_list[j]))
    
    return entity_pairs

entity_pairs = generate_entity_pairs(unique_entities)
print("实体对数量:",len(entity_pairs))

for pair in tqdm(entity_pairs):
    if pair[0] in  pair[1]:
        merged_entities[pair[1]] = pair[0]
    elif pair[1] in pair[0]:
        merged_entities[pair[0]] = pair[1]
    elif calculate_similarity(pair[0],pair[1],model) > 0.7:
        merged_entities[pair[1]] = pair[0]



new_df = df.copy()
for index, row in new_df.iterrows():
    if row['subject'] in merged_entities.keys():
        new_df.at[index,'subject'] = merged_entities[row['subject']]
    if row['object'] in merged_entities.keys():
        new_df.at[index,'object'] = merged_entities[row['object']]


unique_entities = set(new_df['subject']).union(set(new_df['object']))

print("唯一实体的数量：",len(unique_entities))
        

# 保存新的CSV文件
new_df.to_csv('merged_triplets.csv', index=False)




# 现在已经有了一个列表，其中每个元素形如(['贵州', '重庆', '福建', '浙江'], '暴雨洪涝_2014年以来全国因洪涝灾害死亡377人 失踪94人.txt')的元组格式，元组中第一个元素是实体的列表，
# # 1.遍历所有的元组，提取出所有唯一的实体
# # 2.遍历所有实体，找出所有相似的实体，已经有了计算实体相似度的函数calculate_similarity(entity1, entity2, model)，model已经有了
# # 3.将原来列表中所有相似的实体合并为一个，并仍保持原来的格式
# # 4.将上述步骤封装为一个函数，输入为一个列表，输出为一个列表
# from transformers import BertModel, BertTokenizer
# import torch
# from scipy.spatial.distance import cosine
# from tqdm import tqdm   


# # 加载预训练的BERT模型和分词器
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# model = BertModel.from_pretrained('bert-base-uncased')

# # 将实体转换为BERT输入的形式
# def get_bert_input(entity):
#     inputs = tokenizer(entity, return_tensors="pt", max_length=20, truncation=True)
#     return inputs

# # 获取实体的BERT向量表示
# def get_entity_embedding(entity, model):
#     inputs = get_bert_input(entity)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     # 我们使用最后一层的[CLS]标记的隐藏状态作为实体的向量表示
#     embeddings = outputs.last_hidden_state[:, 0, :].numpy()
#     return embeddings.squeeze()  # 添加这行代码将2D张量转换为1D向量

# # 计算两个实体的相似度
# def calculate_similarity(entity1, entity2, model):
#     embedding1 = get_entity_embedding(entity1, model)
#     embedding2 = get_entity_embedding(entity2, model)
#     # 计算余弦相似度
#     similarity = 1 - cosine(embedding1, embedding2)
#     return similarity

# def process_tuples(input_list, model):
#     entity_set = set()
#     similar_entity_dict = {}
#     result_list = []

#     # 遍历所有的元组，提取出所有唯一的实体
#     for item in input_list:
#         entity_list = item[0]
#         for entity in entity_list:
#             entity_set.add(entity)

#     print("实体对齐前，实体数量为：", len(entity_set))
#     # 遍历所有实体，找出所有相似的实体
#     entity_list = list(entity_set)
#     for i in tqdm(range(len(entity_list))):
#         for j in range(i + 1, len(entity_list)):
#             print(i, j)
#             if calculate_similarity(entity_list[i], entity_list[j], model) > 0.5: # 这里我假设相似度大于0.5的实体就是相似的，你可以根据实际情况调整这个阈值
#                 if entity_list[i] not in similar_entity_dict:
#                     similar_entity_dict[entity_list[i]] = [entity_list[j]]
#                 else:
#                     similar_entity_dict[entity_list[i]].append(entity_list[j])
#                 if entity_list[j] not in similar_entity_dict:
#                     similar_entity_dict[entity_list[j]] = [entity_list[i]]
#                 else:
#                     similar_entity_dict[entity_list[j]].append(entity_list[i])

#     # 遍历原始列表，将相似的实体替换为一个
#     for item in input_list:
#         entity_list = item[0]
#         text = item[1]
#         new_entity_list = []
#         for entity in entity_list:
#             if entity in similar_entity_dict:
#                 new_entity_list.append(similar_entity_dict[entity][0]) # 将相似的实体替换为第一个实体
#             else:
#                 new_entity_list.append(entity)
#         result_list.append((new_entity_list, text))

#     return result_list

# # locations_with_title = process_tuples(locations_with_title, model)
# # print(locations_with_title[0])

# times_with_title = process_tuples(times_with_title, model)
# print(times_with_title[0])

# losts_with_title = process_tuples(losts_with_title, model)
# print(losts_with_title[0])






