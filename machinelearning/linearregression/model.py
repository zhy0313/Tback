# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from data.dbaccess import normalize
from data.db import get_db_session, Pinkunhu2015


class LinearRegressionModel(object):
    """ 使用线性回归预测下一年人均年收入 """
        # 提取的属性
    features = [
        'tv', 'washing_machine', 'fridge',
        'reason', 'is_danger_house', 'is_back_poor', 'is_debt', 'standard',
        'arable_land', 'debt_total', 'living_space', 'member_count',
        'person_year_total_income', 'year_total_income',
        'subsidy_total', 'wood_land', 'xin_nong_he_total', 'xin_yang_lao_total',
        'call_number', 'bank_name', 'bank_number', 'help_plan'
    ]
    # 验证的目标
    target = 'ny_person_income'
    # 虚拟标量
    dummy_features = [
        'tv', 'washing_machine', 'fridge',
        'reason', 'is_danger_house', 'is_back_poor',  'is_debt', 'standard',
        'call_number', 'bank_name', 'bank_number', 'help_plan'
    ]

    def run(self):
        """ 运行 """
        # 获取数据
        X, Y = self._fetch_data()
        clf = self.get_classifier(X, Y)
        print X.columns
        print 'Best Coefficients:', clf.coef_
        x_columns = X.columns
        # 测试
        # 补齐X缺失的哑变量
        X, Y = self._fetch_test_data()
        lost_columns = list(set(x_columns) - set(X.columns))
        lost_arr = np.zeros((X.shape[0], len(lost_columns)))
        lost_df = pd.DataFrame(lost_arr, columns=lost_columns)
        X = X.join(lost_df)

        res = []
        for item in range(11):
            hit_ratio = self.predict(clf, X, Y, item * 0.1)
            res.append([item * 0.1 * 100, hit_ratio * 100])

        # 绘制误差与命中率的线性关系图
        arr = np.array(res)
        plt.plot(arr[:, 0], arr[:, 1])        # 绘制线
        plt.plot(arr[:, 0], arr[:, 1], 'ro')  # 绘制点
        plt.xlabel('误差率(%)')
        plt.ylabel('命中率(%)')
        plt.title('使用线性回归预测下一年人均年收入效果图')
        plt.show()

    def get_classifier(self, X, Y):
        """ 构建线性回归模型
        :param X: 训练数据
        :param Y: 训练数据结果
        :return: 模型
        """
        clf = LinearRegression()
        clf.fit(X, Y)
        return clf

    def predict(self, clf, X, Y, deviation=0.1):
        """ 用当前的模型预测
        :param clf: 模型
        :param X: 测试数据
        :param Y: 测试数据结果
        :param deviation: 允许误差率
        :return: 命中率
        """
        Y2 = clf.predict(X)
        total, hit = len(Y), 0
        for idx, v in enumerate(Y2):
            if math.fabs(Y[idx] - v) <= math.fabs(Y[idx] * deviation):  # 误差小于deviation，则认为预测准确
                hit += 1

        print 'Deviation: %d%%, Total: %d, Hit: %d, Precision: %.2f%%' % (100 * deviation, total, hit, 100.0*hit/total)
        # 用 A县 的模型去预测 B县 的结果
        # Deviation: 0%, Total: 40820, Hit: 0, Precision: 0.00%
        # Deviation: 10%, Total: 40820, Hit: 24418, Precision: 59.82%
        # Deviation: 20%, Total: 40820, Hit: 32935, Precision: 80.68%
        # Deviation: 30%, Total: 40820, Hit: 36211, Precision: 88.71%
        # Deviation: 40%, Total: 40820, Hit: 37367, Precision: 91.54%
        # Deviation: 50%, Total: 40820, Hit: 38041, Precision: 93.19%
        # Deviation: 60%, Total: 40820, Hit: 38502, Precision: 94.32%
        # Deviation: 70%, Total: 40820, Hit: 38816, Precision: 95.09%
        # Deviation: 80%, Total: 40820, Hit: 39071, Precision: 95.72%
        # Deviation: 90%, Total: 40820, Hit: 39282, Precision: 96.23%
        # Deviation: 100%, Total: 40820, Hit: 39432, Precision: 96.60%

        return hit * 1.0 / total

    def _fetch_data(self):
        """ 获取建模数据 """
        session = get_db_session()
        objs = session.query(Pinkunhu2015).filter(
                Pinkunhu2015.county == 'A县', Pinkunhu2015.ny_person_income != -1,
                Pinkunhu2015.person_year_total_income > 0, Pinkunhu2015.person_year_total_income < 7000,
                Pinkunhu2015.ny_person_income > 0, Pinkunhu2015.ny_person_income < 7000,
        ).all()
        X, Y = [], []
        for item in objs:
            col_list = []
            for col in self.features:
                normalized_value = normalize(col, getattr(item, col))
                col_list.append(normalized_value)
            X.append(col_list)
            normalized_value = normalize(self.target, getattr(item, self.target))
            Y.append(normalized_value)

        # # 筛掉可能有错误的数据
        # 人均年收入除以100后，查看分布，少于5次的不纳入模型, 效果不佳，废弃
        # df = pd.DataFrame(X, columns=self.features)
        # print '#df.shape:', df.shape
        # df['person_year_total_income'] = df['person_year_total_income'] / 100
        # df['person_year_total_income'] = df['person_year_total_income'].astype(int)
        # df['person_year_total_income'] = df['person_year_total_income'] * 100
        # df = df.groupby('person_year_total_income').filter(lambda x: len(x) > 5)
        # print '#df.shape:', df.shape
        # X, Y = df.loc[:, self.features[:-1]], df.loc[:, self.target]
        # 设置虚拟变量
        df = pd.DataFrame(X, columns=self.features)
        for item in self.dummy_features:
            dummies = pd.get_dummies(df[item], prefix=item)
            df = df.join(dummies)
        # 删除已设置虚拟变量的原变量
        df = df.drop(self.dummy_features, axis=1)
        X = df.loc[:]

        return X, Y

    def _fetch_test_data(self):
        """ 获取测试数据 """
        session = get_db_session()
        objs = session.query(Pinkunhu2015).filter(
                Pinkunhu2015.county == 'B县', Pinkunhu2015.ny_person_income != -1,
                Pinkunhu2015.person_year_total_income > 0, Pinkunhu2015.person_year_total_income < 7000,
                Pinkunhu2015.ny_person_income > 0, Pinkunhu2015.ny_person_income < 7000,
        ).all()
        X, Y = [], []
        for item in objs:
            col_list = []
            for col in self.features:
                normalized_value = normalize(col, getattr(item, col))
                col_list.append(normalized_value)
            X.append(col_list)
            normalized_value = normalize(self.target, getattr(item, self.target))
            Y.append(normalized_value)

        # 设置虚拟变量
        df = pd.DataFrame(X, columns=self.features)
        for item in self.dummy_features:
            dummies = pd.get_dummies(df[item], prefix=item)
            df = df.join(dummies)
        # 删除已设置虚拟变量的原变量
        df = df.drop(self.dummy_features, axis=1)
        X = df.loc[:]

        return X, Y


if __name__ == '__main__':
    m = LinearRegressionModel()
    m.run()
