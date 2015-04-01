#!/usr/bin/python
# encoding: utf-8

import sys

##########################
# results为list，list成员格式如下
# [key, args, instruction, link]
##########################
def print_result(results):
    print '''<?xml version="1.0"?>'''
    print "<items>"
    for item in results:
        if len(item) != 4:
            continue
        key = item[0].strip()
        args = item[1].strip()
        instruction = item[2].strip()
        link = item[3].strip()
        print "    <item uid=\"test\" autocomplete=\"\" arg=\"" + link + "\">"
        print "        <title>" + key + " " + args + "</title>"
        print "        <subtitle>" + instruction + "</subtitle>"
        print "        <icon>/Users/zhangmenghan/Library/Application Support/Alfred 2/Alfred.alfredpreferences/workflows/user.workflow.3E712875-F425-40A6-B534-2F99BEDB9FFA/redis.png</icon>"
        print "    </item>"
    print "</items>"

#########################
# 读取辞典，生成两个map，一个为class to item, 即key位类型，value为输出结果集合，类型为list
# 另一个为command to item，即key为redis的命令，value为对应的结果，类型为list
#########################
def read_dict(file_path):
    class2item_dict = {}
    cmd2item_dict = {}
    for line in open(file_path):
        #print "readline:" + line
        f = line.strip('\n').split('#')
        if len(f) != 5:
            continue
        class_type = f[0].strip().lower()
        cmd = f[2].strip().lower()
        item = [f[2], f[3], f[4], f[1]]
        #print "item:"
        #print item
        if class2item_dict.has_key(class_type):
            value = class2item_dict[class_type]
            #print class_type + " value before append:"
            #print value
            value.append(item)
            class2item_dict[class_type] = value
        else:
            class2item_dict[class_type] = [item]
        #print class_type + " value:"
        #print class2item_dict[class_type]
        if cmd2item_dict.has_key(cmd):
            value = cmd2item_dict[cmd]
            value.append(item)
            cmd2item_dict[cmd] = value
        else:
            cmd2item_dict[cmd] = [item]

    return class2item_dict, cmd2item_dict


def search(query):

    class2item_dict, cmd2item_dict = read_dict("./redis_commands_disk.txt")
    results = []
    
    query = query.lower()

    ## 如果完全匹配，则只显示完全匹配的条目
    if class2item_dict.has_key(query):
        results = class2item_dict[query]
        print_result(results)
        return 

    if cmd2item_dict.has_key(query):
        results = cmd2item_dict[query]
        print_result(results)
        return 
    
    ## 前缀匹配，如果数量达到一定值则直接返回
    ## 保存已经匹配到的cmd
    cmd_set = set()
    for key, value in class2item_dict.iteritems():
        #print "query:" + query + " key:" + key
        if key[:len(query)] == query:
            results += value
            cmd_set.add(key)
    for key, value in cmd2item_dict.iteritems():
        #print "query:" + query + " key:" + key
        if key[:len(query)] == query:
            results += value
            cmd_set.add(key)

    if len(results) > 10:
        print_result(results)
        return 

    ## 打印所有包含query的条目，此时可能结果里有重复的，需要去重
    for key, value in class2item_dict.iteritems():
        if query in key:
            if key not in cmd_set:
                results += value
                cmd_set.add(key)
    for key, value in cmd2item_dict.iteritems():
        if query in key:
            if key not in cmd_set:
                results += value
                cmd_set.add(key)
    print_result(results)
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "usage:" + sys.argv[0] + " query"
        sys.exit(1)
    search(sys.argv[1])
