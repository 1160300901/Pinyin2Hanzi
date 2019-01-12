#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: sunyueqing
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: sunyueqinghit@163.com
@File : predict.py
@Time : 2018/12/23 15:15
@Site : 
@Software: PyCharm
'''

# encoding=utf-8
import pickle
from os import path
from viterbi import viterbi_algo
from train import Trainer
import time


class MySolver(object):
    def __init__(self, filename=r"data/HMM.pkl"):
        self.candidate = []
        self.candidate_page = 0
        self.candidate_per_page = 5

        self.loaded = False
        if path.exists(filename):
            self.loaded = True
            with open(filename, "rb") as f:
                x = Trainer()
                x = pickle.load(f)
                # print(x)
            self.params = x

            # print(self.params.trans_mat)

    def solve(self, input_str):
        if not self.loaded:
            return []
        obs = input_str.split(" ")
        tmp_ob = []
        for i in obs:
            if self.params.encode_pinyin.get(i) is None:
                break
            else:
                tmp_ob.append(i)
        obs = tmp_ob
        ans = []
        # print(obs)

        if len(obs) > 1:
            tmp_candidate = self.__solve(obs)
            if tmp_candidate is not None:
                ans = ans + tmp_candidate
            # for i in obs:
            #     print(i)
            #     tmp_candidate = self.__solve([i])
            #     if tmp_candidate is not None:
            #         ans = ans + tmp_candidate
        elif len(obs) == 1:
            tmp_candidate = self.__solve(obs)
            if tmp_candidate is not None:
                ans = ans + tmp_candidate

        return ans

    def __solve(self, obs):

        x = viterbi_algo(self.params, observations=obs)
        return x

    def check_change(self, mystr):
        self.candidate = self.solve(mystr)
        self.candidate_page = 0
        final_str = self.set_string()
        return final_str
        # print(final_str)

    def set_string(self):
        final_str = ""
        if len(self.candidate) < self.candidate_per_page * (1 + self.candidate_page):
            for i in range(len(self.candidate) - self.candidate_per_page * self.candidate_page):
                # final_str += str(i + 1) + ". "
                final_str += self.candidate[self.candidate_page * self.candidate_per_page + i][0]
        else:
            for i in range(self.candidate_per_page):
                # final_str += str(i + 1) + ". "
                final_str += self.candidate[self.candidate_page * self.candidate_per_page + i][0]
        return final_str

    def predict(self, pinyin, hanzi):
        count = 0
        f_pinyin = open(pinyin, "r")
        f_hanzi = open(hanzi, "w")
        for line in f_pinyin.readlines():
            count += 1
            print('Loading test data. Line: ', count)
            f_hanzi.write(self.check_change(line))
            f_hanzi.write("\n")
        f_hanzi.close()
        f_pinyin.close()


if __name__ == '__main__':
    print("正在计时...\n")
    t0 = time.time()
    solve = MySolver()
    solve.predict('data/test_pinyin.txt', 'result.txt')
    # print(solve.check_change("yi hang bai lu shang qing tian"))
    print("总耗时: ", time.time() - t0, " 秒")
