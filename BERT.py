'''
Author: jonnyzhang02 71881972+jonnyzhang02@users.noreply.github.com
Date: 2023-06-02 14:44:24
LastEditors: jonnyzhang02 71881972+jonnyzhang02@users.noreply.github.com
LastEditTime: 2023-06-02 15:12:09
FilePath: /tp_big_hw/BERT.py
Description: coded by ZhangYang@BUPT, my email is zhangynag0207@bupt.edu.cn
'''
from transformers import BertModel, BertTokenizer
import torch
from scipy.spatial.distance import cosine

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
entity1 = "Apple Inc."
entity2 = "苹果公司"
similarity = calculate_similarity(entity1, entity2, model)
print(f"The similarity between '{entity1}' and '{entity2}' is {similarity}.")


# 创建一个空的字典来存储实体的嵌入
entity_embeddings = {}




