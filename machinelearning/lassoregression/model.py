# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from data.dbaccess import normalize
from data.db import get_db_session, Pinkunhu2015


class LassoModel(object):
    """ 使用Lasso预测下一年人均年收入 """
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
    target = self.target

    def run(self):
        """ 运行 """
        # 获取数据
        X, Y = self._fetch_data()
        clf = self.get_classifier(X, Y)
        # 测试
        X, Y = self._fetch_test_data()
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
        plt.title('使用Lasso预测下一年人均年收入效果图')
        plt.show()

    def get_classifier(self, X, Y):
        """ 构建Lasso模型
        :param X: 训练数据
        :param Y: 训练数据结果
        :return: 模型
        """
        clf = Lasso()
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
        # Deviation: 10%, Total: 40820, Hit: 24513, Precision: 60.05%
        # Deviation: 20%, Total: 40820, Hit: 33011, Precision: 80.87%
        # Deviation: 30%, Total: 40820, Hit: 36230, Precision: 88.76%
        # Deviation: 40%, Total: 40820, Hit: 37379, Precision: 91.57%
        # Deviation: 50%, Total: 40820, Hit: 38048, Precision: 93.21%
        # Deviation: 60%, Total: 40820, Hit: 38511, Precision: 94.34%
        # Deviation: 70%, Total: 40820, Hit: 38830, Precision: 95.12%
        # Deviation: 80%, Total: 40820, Hit: 39077, Precision: 95.73%
        # Deviation: 90%, Total: 40820, Hit: 39282, Precision: 96.23%
        # Deviation: 100%, Total: 40820, Hit: 39429, Precision: 96.59%

        return hit * 1.0 / total

    def _fetch_data(self):
        """ 获取建模数据 """
        session = get_db_session()
        objs = session.query(Pinkunhu2015).filter(
                Pinkunhu2015.county == 'A县', Pinkunhu2015.ny_person_income != -1,
                Pinkunhu2015.person_year_total_income > 0, Pinkunhu2015.person_year_total_income < 7000,
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

        return X, Y

    def _fetch_test_data(self):
        """ 获取测试数据 """
        session = get_db_session()
        objs = session.query(Pinkunhu2015).filter(
                Pinkunhu2015.county == 'B县', Pinkunhu2015.ny_person_income != -1,
                Pinkunhu2015.person_year_total_income > 0, Pinkunhu2015.person_year_total_income < 7000,
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

        return X, Y


if __name__ == '__main__':
    m = LassoModel()
    m.run()
