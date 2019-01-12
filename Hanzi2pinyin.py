#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: sunyueqing
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: sunyueqinghit@163.com
@File : Hanzi2pinyin.py
@Time : 2018/12/23 20:57
@Site : 
@Software: PyCharm
'''

import pypinyin
from pypinyin import pinyin, lazy_pinyin

f_pinyin = open('data/test_pinyin.txt', 'w')

for line in open('data/test_hanzi.txt', 'r'):
    for i in lazy_pinyin(line.strip()):
        f_pinyin.write(i+" ")
    f_pinyin.write("\n")

f_pinyin.close()
