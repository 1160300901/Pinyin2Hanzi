#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: sunyueqing
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: sunyueqinghit@163.com
@File : Score.py
@Time : 2018/12/26 12:47
@Site : 
@Software: PyCharm
'''


def Score(result, test):
    count = 0
    sum = 0
    with open(result, 'r') as f1:
        with open(test, 'r') as f2:
            for x, y in zip(f1.readlines(), f2.readlines()):
                x = x.strip()
                y = y.strip()
                # print(x)
                # print(y)
                for i in range(len(x)):
                    sum += 1
                    if x[i] == y[i]:
                        count += 1
    # print(count)
    # print(sum)
    return count, sum


if __name__ == '__main__':
    count, sum = Score('result.txt', 'data/test_hanzi.txt')
    print('转换正确字数：', count)
    print('总字数：', sum)
    print('准确率：', count / sum)
