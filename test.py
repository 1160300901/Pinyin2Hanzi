#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: sunyueqing
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: sunyueqinghit@163.com
@File : test.py
@Time : 2018/12/23 21:53
@Site : 
@Software: PyCharm
'''

import re


def rm_punctuation(file, rmfile):
    punc = "。，、‘：；“”,’？?！（）＋－×……《》【】『』()"
    f1 = open(file, "r", encoding='GB18030')
    f2 = open(rmfile, "w", encoding='GB18030')
    for line in f1.readlines():
        line_rmpunc = re.sub("[%s]+" % punc, "\n", line)
        f2.write(line_rmpunc)
    f1.close()
    f2.close()


def handle_dictfile(rawfile, resultfile):
    f_raw = open(rawfile, "r", encoding="GB18030")
    f_result = open(resultfile, "w", encoding="GB18030")
    for line in f_raw.readlines():
        line = line.strip()
        if re.match("(\d+)", line):  # 删去数字
            continue
        p = re.compile(r"[■〈〉?±％／ＭＩＣＲＯＮＡＳＤＥＹｏｕａｒｅｗｌｃｍＴ—Ｋ·ＦｄｈＵｎｉｖｓｔｙ．ｐＪＢｇＰＨ５０１ＸＧ８ｋｂ９ＶＺ７ｚ２３４６1234567890]+")
        if p.findall(line):
            continue
        if len(line) == 1 or len(line) == 0 or len(line) == 2 or len(line) == 3:
            continue
        f_result.write(line.strip("[").strip("]") + "\n")


def extract(rawfile, resultfile):
    '''
    提取分词标准文件，作为计算准确率的参照
    :param rawfile: 2004_corpus.txt,2004年人民日报带词性标注的语料
    :param resultfile: 2004_seg.txt,从预料库删去词性，得到分词标准文件
    :return:
    '''
    f_raw = open(rawfile, "r", encoding="utf-8")
    f_result = open(resultfile, "w", encoding="GB18030")

    for line in f_raw.readlines():
        if len(line.strip()) == 0:
            continue
        line = re.sub("[/a-zA-Z]+", "/", line)
        line = re.sub("/1", "/", line)
        line = re.sub("（）", "", line)
        line = re.sub("]/", "", line)
        line = re.sub("\[", "", line)
        line = re.sub("（/ / ）/ ", "", line)
        line = line.replace("1", "１")
        line = line.replace("2", "２")
        line = line.replace("3", "３")
        line = line.replace("4", "４")
        line = line.replace("5", "５")
        line = line.replace("6", "６")
        line = line.replace("7", "７")
        line = line.replace("8", "８")
        line = line.replace("9", "９")
        line = line.replace("0", "０")
        line = line.replace("%", "％")

        f_result.write(line)
    f_result.close()
    f_raw.close()


def extract2(rawfile, resultfile):
    '''
    生成用于分词的生文本
    :param rawfile: 2004_seg.txt,分词标准文件
    :param resultfile: 2004_sentence.txt,去除分词，得到即将分词的句子
    :return:
    '''
    f_raw = open(rawfile, "r", encoding="GB18030")
    f_result = open(resultfile, "w", encoding="GB18030")

    for line in f_raw.readlines():
        line = re.sub("/ ", "", line)
        f_result.write(line)
    f_result.close()
    f_raw.close()


def countHanzi():
    with open('data/pinyin2hanzi.txt', encoding="utf-8") as f:
        idx_hanzi = 0
        idx_pinyin = 0
        for line in f.readlines():
            idx_pinyin = idx_pinyin + 1
            hanzis = line.split("=")[1].replace("\n", "")
            idx_hanzi += len(hanzis)
    print(idx_hanzi)
    print(idx_pinyin)

def countTrainData():
    with open('data/Hanzi_train.txt') as f:
        idx_hanzi = 0
        for line in f.readlines():
            hanzis = line.replace("\n", "")
            idx_hanzi += len(hanzis)
    print(idx_hanzi)

def main():
    # extract("0121.txt", "seg.txt")
    # extract2("seg.txt", "data/0121meicixing.txt")
    # rm_punctuation("data/0121meicixing.txt", "data/none_punctuation.txt")
    # handle_dictfile("data/none_punctuation.txt", "data/0121train.txt")
    # countHanzi()
    countTrainData()
    # import os
    # # 获取目标文件夹的路径
    # filedir = os.getcwd() + "/0123"
    # # 获取当前文件夹中的文件名称列表
    # filenames = os.listdir(filedir)
    # # 打开当前目录下的result.txt文件，如果没有则创建
    # f = open('0123.txt', 'w', encoding="utf-8")
    # # 先遍历文件名
    # for filename in filenames:
    #     filepath = filedir + '/' + filename
    #     # 遍历单个文件，读取行数
    #     for line in open(filepath, encoding="utf-8"):
    #         f.writelines(line)
    #     # f.write('\n')
    # # 关闭文件
    # f.close()


if __name__ == '__main__':
    main()
