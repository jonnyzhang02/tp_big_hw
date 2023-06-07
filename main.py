'''
Author: jonnyzhang02 71881972+jonnyzhang02@users.noreply.github.com
Date: 2023-06-01 08:27:12
LastEditors: jonnyzhang02 71881972+jonnyzhang02@users.noreply.github.com
LastEditTime: 2023-06-07 18:55:58
FilePath: /tp_big_hw/main.py
Description: coded by ZhangYang@BUPT, my email is zhangynag0207@bupt.edu.cn
'''
import os
import re

def process_text(raw_text, pattern, B_label, I_label, disallowed_chars):
    raw_text = raw_text.replace('\n', '')  # 1. 删除换行符
    chars = list(raw_text)  # 转换为字符列表
    tags = ['O'] * len(chars)  # 创建等长标签列表

    # 2. 匹配实体并赋值标签
    # pattern = r' ([^ ]+)/LOC '
    for match in re.finditer(pattern, raw_text):
        entity_start = match.start() + 1  # 去除空格
        if B_label == "B-LOCATION":
            entity_end = match.end() - 5
        else:
            entity_end = match.end() - 4
        tags[entity_start] = B_label
        for i in range(entity_start + 1, entity_end):
            tags[i] = I_label

    # disallowed_chars  = []

    # 3. 删除人工标注的数据，并删去它对应的标签
    filtered_chars = []
    filtered_tags = []

    for char, tag in zip(chars, tags):
        if char not in disallowed_chars:
            filtered_chars.append(char)
            filtered_tags.append(tag)

    chars, tags = filtered_chars, filtered_tags

    # 4. 删除空格及其对应的标签
    chars, tags = zip(*[(char, tag) for char, tag in zip(chars, tags) if char != ' '])

    assert len(chars) == len(tags)

    return (list(chars), list(tags))

def transform_data(folder_path, regex, B_label, I_label, disallowed_chars):
    data = []  # 一个文件夹的数据
    files = os.listdir(folder_path) # 获取文件夹下所有文件 
    for file in files: # 遍历文件夹
        with open(folder_path + "/" + file, 'r', encoding='utf-8') as f: 
            text = f.read() # 读取文件
            data.append(process_text(text, regex, B_label, I_label, disallowed_chars)) # 处理数据
    return data, files

data_loaction, title_loc = transform_data("./data/location", r' ([^ ]+)/LOC ', "B-LOCATION", "I-LOCATION", ["/", "L", "O", "C"])
data_time, title_time = transform_data("./data/time", r' ([^ ]+)/[DT][SO] ', "B-TIME", "I-TIME", ["/", "D", "T", "S", "O"])
data_lost, title_lost = transform_data("./data/lost", r' ([^ ]+)/DB ', "B-LOST", "I-LOST",["/", "D", "B"])
data_person, title_person = transform_data("./data/person", r' ([^ ]+)/(AE|AImP|ADP|AMP|AInP|AIAC|ATAC|AHC|AIAC2) ', "B-PERSON", "I-PERSON", ["/", "A", "E", "P", "I", "M", "T", "H", "C"])




def extract_info_with_title(data, B_label, I_label, titles):
    def extract_info(data, B_label, I_label):
        results = []
        for i in range(len(data)):
            result = []
            # print(data[i])
            for index in range(len(data[i][1])):
                if data[i][1][index] == B_label:
                    result.append(data[i][0][index])
                elif data[i][1][index] == I_label:
                    result[-1] += data[i][0][index]

            # print(result)
            results.append(result)
        return results

    results = extract_info(data, B_label, I_label)
    results_with_title = []
    for i in range(len(results)):
        results_with_title.append((results[i], titles[i]))
    return results_with_title


locations_with_title = extract_info_with_title(data_loaction, "B-LOCATION", "I-LOCATION", title_loc)
print(locations_with_title[0])

times_with_title = extract_info_with_title(data_time, "B-TIME", "I-TIME", title_time)
print(times_with_title[0])

losts_with_title = extract_info_with_title(data_lost, "B-LOST", "I-LOST", title_lost)
print(losts_with_title[0])

persons_with_title = extract_info_with_title(data_person, "B-PERSON", "I-PERSON", title_person)
print(persons_with_title[0])

def process_entity_list(entity_list, entity_index, title_dict):
    for entities, title in entity_list:
        if title not in title_dict:
            title_dict[title] = ([], [], [], [], title)
        current_tuple = title_dict[title]
        current_tuple = current_tuple[:entity_index] + (entities,) + current_tuple[entity_index+1:]
        title_dict[title] = current_tuple
    return title_dict

def remove_duplicates(entity_list):
    return list(dict.fromkeys(entity_list))

# 初始化一个空的字典来存储四元组
title_dict = {}

# 处理地点、时间和损失列表
title_dict = process_entity_list(locations_with_title, 0, title_dict)
title_dict = process_entity_list(times_with_title, 1, title_dict)
title_dict = process_entity_list(losts_with_title, 2, title_dict)
title_dict = process_entity_list(persons_with_title, 3, title_dict)


# 将字典转化为列表，其中每一个元素是一个五元组
tuple_list = list(title_dict.values())

# 对四元组列表中的每个元素去重
for i in range(len(tuple_list)):
    locations, times, losts, persons, title = tuple_list[i]
    locations = remove_duplicates(locations)
    times = remove_duplicates(times)
    losts = remove_duplicates(losts)
    persons = remove_duplicates(persons)
    tuple_list[i] = (locations, times, losts, persons, title)


print(tuple_list[150])

def generate_tuples(tuple_list):
    # 初始化一个空列表来存储生成的三元组
    triplets = []

    for locations, times, losts, persons, title in tuple_list:
        title = "<"+ title[:-4] + '>'
        title = '暴雨洪涝'
        for location in locations:
            #triplets.append((title, "发生于", location))
            for lost in losts:
                triplets.append((location, title + "承载于", lost))
            for person in persons:
                triplets.append((location, title + "造成了", person))
        for time in times:
            for location in locations:
                triplets.append((time, title + "发生于", location))
            for lost in losts:
                triplets.append((time, title + "承载于", lost))
            for person in persons:
                triplets.append((time, title + "造成了", person))

    return triplets

triplets = generate_tuples(tuple_list)
print(triplets[150])

import csv

# 创建一个csv文件并写入三元组列表
with open('triplets.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["subject", "relation", "object"])  # 写入列名
    for triplet in triplets:
        writer.writerow(triplet)

# 创建一个空集合来存储实体
entities = set()

# 遍历三元组
for triplet in triplets:
    subject, _, object = triplet
    # 将主语和宾语添加到实体集合中
    entities.add(subject)
    entities.add(object)

# 计算并打印实体数量
num_entities = len(entities)
print(f"共出现了 {num_entities} 个不同的实体。")
# 共出现了 3134 个不同的实体。






# 现在对这个四元组列表中的每一个单独的元素，清除地点实体、时间实体和损失实体中的重复项

# times = (extract_info(data_time, "B-TIME", "I-TIME"), title_time)
# print(times[0])

# losts = (extract_info(data_lost, "B-LOST", "I-LOST"), title_lost)
# print(losts[0])




# for i in range(len(data_loaction)):
#     print(len(data_loaction[i][0]),"\t", len(data_time[i][0]),"\t", len(data_lost[i][0]))

    
# print(data_loaction[0])
# print(data_time[0])
# print(data_lost[0])

# print(len(data_loaction))
# print(len(data_time))
# print(len(data_lost))


# 将数据写入文件
# json.dump(data_loaction, open("./data/location.json", "w", encoding="utf-8"), ensure_ascii=False)
# json.dump(data_time, open("./data/time.json", "w", encoding="utf-8"), ensure_ascii=False)
# json.dump(data_lost, open("./data/lost.json", "w", encoding="utf-8"), ensure_ascii=False)
