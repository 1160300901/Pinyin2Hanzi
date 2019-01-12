#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: sunyueqing
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: sunyueqinghit@163.com
@File : viterbi.py
@Time : 2018/12/23 15:13
@Site : 
@Software: PyCharm
'''

# encoding=utf-8

import numpy as np
from collections import deque
from train import Trainer
import math


class Node(object):
    def __init__(self, hanzi_code):
        self.hanzi_code = hanzi_code
        self.prob = 0
        self.previous = None


def viterbi_algo(params, observations):
    layers = []

    for ob in observations:

        ob = params.encode_pinyin[ob]  # 拼音的键值
        # print("ob:",ob)
        hanzis_code = params.pinyin2hanzi[ob]  # 每个拼音对应的汉字的键值列表
        # print("hanzi_code:", hanzis_code)
        tmp = []
        for hanzi_code in hanzis_code:
            tmp.append(Node(hanzi_code))
        # print(tmp)
        layers.append((tmp, ob))

    if len(observations) == 1:
        x = [(params.decode_hanzi[hanzi.hanzi_code], params.hanzi_fre[hanzi.hanzi_code]) for hanzi in layers[0][0]]
        x.sort(key=lambda s: (s[1], s[0]), reverse=True)
        # sorted(x, key=lambda s: s[1], reverse=True)
        return x

    first_layer = layers[0][0]
    for hanzi in first_layer:
        hanzi.prob = params.hanzi_fre[hanzi.hanzi_code]  # 初始状态概率

    previous_layer = first_layer
    for layer in layers[1:]:  # 遍历1之后的拼音序列
        for hanzi in layer[0]:  # 遍历当前拼音对应的每个汉字
            for previous_hanzi in previous_layer:  # 前一个拼音对应的每个汉字
                # 前一个汉字的概率*前一个汉字到当前汉字的转移概率
                t = previous_hanzi.prob * params.trans_mat[previous_hanzi.hanzi_code, hanzi.hanzi_code]
                if t > hanzi.prob:  # 取最大的值
                    hanzi.prob = t
                    hanzi.previous = previous_hanzi
            hanzi.prob *= params.gen_mat[hanzi.hanzi_code, layer[1]]  # 乘以汉字生成某个拼音的发射概率
        previous_layer = layer[0]

    x = max(layers[-1][0], key=lambda s: s.prob)  # 概率最大的一条路径
    prob = x.prob
    hanzi_seq = str("")
    while x is not None:
        hanzi_seq += params.decode_hanzi[x.hanzi_code]
        # print(hanzi_seq)
        x = x.previous
    hanzi_seq = hanzi_seq[::-1]
    ans = []
    ans.append((hanzi_seq, prob))
    return ans
