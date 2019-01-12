#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: sunyueqing
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: sunyueqinghit@163.com
@File : train.py
@Time : 2018/12/23 15:14
@Site : 
@Software: PyCharm
'''

import numpy as np

np.seterr(divide='ignore', invalid='ignore')
import pickle
import re
from os import path
import time

'''
实现了从原始的语料数据中计算HMM模型的参数
'''


class Trainer(object):
    def __init__(self):
        self.total_hanzi = 10000
        self.total_pinyin = 450
        self.encode_hanzi = {}  # 将拼音字符串编码成数字
        self.encode_pinyin = {}  # 将汉字编码成数字
        self.decode_hanzi = {}
        self.decode_pinyin = {}
        self.trans_mat = np.ones((self.total_hanzi, self.total_hanzi))  # 汉字与汉字之间的转移概率矩阵
        self.gen_mat = np.zeros((self.total_hanzi, self.total_pinyin))  # 汉字生成某个拼音的矩阵
        self.hanzi_fre = np.zeros(self.total_hanzi)  # 某个汉字的出现的频率（次数）
        self.pinyin2hanzi = {}  # 某个拼音对应的所有可能汉字
        # print(self.trans_mat)

    def __read_pinyin(self, path):
        count = 0

        with open(path, encoding="utf-8") as f:
            count += 1
            print('Loading pinyin data. Line: ', count)
            idx_hanzi = 0
            idx_pinyin = 0
            for line in f.readlines():
                pinyin = line.split(":")[0]
                self.encode_pinyin.update({pinyin: idx_pinyin})
                idx_pinyin = idx_pinyin + 1

                hanzis = line.split(":")[1].replace("\n", "")

                for hanzi in hanzis:
                    if self.encode_hanzi.get(hanzi) is None:
                        self.encode_hanzi.update({hanzi: idx_hanzi})
                        idx_hanzi = idx_hanzi + 1
                    tmp_idx_pinyin = self.encode_pinyin[pinyin]
                    tmp_idx_hanzi = self.encode_hanzi[hanzi]
                    self.gen_mat[tmp_idx_hanzi, tmp_idx_pinyin] = self.gen_mat[tmp_idx_hanzi, tmp_idx_pinyin] + 1
                    if self.pinyin2hanzi.get(tmp_idx_pinyin) is None:
                        self.pinyin2hanzi.update({tmp_idx_pinyin: [tmp_idx_hanzi]})
                    else:
                        self.pinyin2hanzi[tmp_idx_pinyin].append(tmp_idx_hanzi)

        # Crop the matrix
        self.total_hanzi = idx_hanzi
        self.total_pinyin = idx_pinyin
        self.trans_mat = self.trans_mat[0:self.total_hanzi, 0:self.total_hanzi]
        self.gen_mat = self.gen_mat[0:self.total_hanzi, 0:self.total_pinyin]

        # Normalize
        self.gen_mat /= np.sum(self.gen_mat, axis=1).reshape((-1, 1))

    def __read_trans(self, path):
        with open(path, encoding="GB18030") as f:
            count = 0

            for line in f.readlines():
                count += 1
                print("Loading train data. Line: ", count)
                line = line.strip()
                lamps = re.split(r"。|（|）|，|：|”|“|、|《|》", line)
                # print("lamps: ", lamps)
                for lamp in lamps:
                    if lamp == '' or len(lamp) == 1:
                        continue

                    # print("lamp: ", lamp)
                    words_last = [x for x in lamp]
                    # print("words_last", words_last)
                    # words_last.pop(-1)
                    words = words_last[1:]
                    # print("words", words)
                    words_last.pop(-1)
                    # assert (len(words_last) == len(words))
                    # print(words_last)
                    for i in range(len(words_last)):
                        idx_last = self.encode_hanzi.get(words_last[i])
                        idx_now = self.encode_hanzi.get(words[i])
                        if idx_last is None or idx_now is None:
                            continue
                        self.trans_mat[idx_last, idx_now] = self.trans_mat[idx_last, idx_now] + 1
                        self.hanzi_fre[idx_now] = self.hanzi_fre[idx_now] + 1
            '''
            平滑
            '''

            print(self.trans_mat)
            # Normalize
            self.trans_mat /= np.sum(self.trans_mat, axis=1).transpose()
            print(self.trans_mat)
            self.hanzi_fre /= np.sum(self.hanzi_fre)

            # construct decode hash table
            for k, v in self.encode_hanzi.items():
                self.decode_hanzi.update({v: k})
            for k, v in self.encode_pinyin.items():
                self.decode_pinyin.update({v: k})

    def train(self, ma_biao, yu_liao):
        self.__read_pinyin(ma_biao)
        self.__read_trans(yu_liao)

    def save_model(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)


if __name__ == '__main__':
    print("正在计时...\n")
    t0 = time.time()
    my_trainer = Trainer()
    my_trainer.train("data/pinyin.txt", "data/Hanzi_train.txt")
    my_trainer.save_model("data/HMM.pkl")
    print("总耗时: ", time.time() - t0, " 秒")
