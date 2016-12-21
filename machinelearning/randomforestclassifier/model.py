# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from data.dbaccess import normalize
from data.db import get_db_session, Pinkunhu2015


class RandomForestModel(object):
    """ 使用随机森林模型预测是否脱贫 """
    # 提取的属性
    features = [
        'tv', 'washing_machine', 'fridge',
        'reason', 'is_danger_house', 'is_back_poor', 'is_debt', 'standard',
        'arable_land', 'debt_total', 'living_space', 'member_count',
        # 'person_year_total_income', 'year_total_income',
        'subsidy_total', 'wood_land', 'xin_nong_he_total', 'xin_yang_lao_total',
        'call_number', 'bank_number', 'help_plan'
    ]
    # 验证的目标
    target = 'poor_status'

    def run(self):
        """ 运行 """
        # 获取数据
        X, Y = self._fetch_data()
        clf = self.get_classifier(X, Y)
        # 测试
        X, Y = self._fetch_test_data()
        self.predict(clf, X, Y)
        # 绘制 feature importance
        self.plot(clf, self.features)

    def get_classifier(self, X, Y):
        """ 构建随机森林模型
        :param X: 训练数据
        :param Y: 训练数据结果
        :return: 模型
        """
        clf = RandomForestClassifier(n_estimators=10)
        clf.fit(X, Y)
        return clf

    def predict(self, clf, X, Y):
        """ 用当前的模型预测
        :param clf: 模型
        :param X: 测试数据
        :param Y: 测试数据结果
        :return: 命中率
        """
        Y2 = clf.predict(X)
        total, hit = 0, 0
        for idx, v in enumerate(Y2):
            if v == 1:
                total += 1
                if Y[idx] == v:
                    hit += 1

        print 'Total: %d, Hit: %d, Precision: %.2f%%' % (total, hit, 100.0*hit/total)
        # 用 A县 的模型去预测 B县 的结果
        # Total: 6769, Hit: 5295, Precision: 78.22%

        return hit * 1.0 / total

    def plot(self, clf, features):
        """
        绘制 feature importance
        :param clf: 已构建的分类模型
        :param features: 所有的属性列表
        :return:
        """
        features_len = len(features)
        importances = clf.feature_importances_
        std = np.std([tree.feature_importances_ for tree in clf.estimators_], axis=0)
        indices = np.argsort(importances)[::-1]

        # 打印 feature ranking
        print("\nFeature ranking:")
        for f in range(features_len):
            print("%d. %s (%f)" % (f + 1, features[indices[f]], importances[indices[f]]))

        # 绘制 feature importances 柱状图
        plt.figure()
        plt.title("Feature importances")
        plt.bar(range(features_len), importances[indices], color="r", yerr=std[indices], align="center")
        plt.xticks(range(features_len), np.array(features)[indices], rotation=-90)
        plt.xlim([-1, features_len])
        plt.show()

    def _fetch_data(self):
        """ 获取建模数据 """
        session = get_db_session()
        objs = session.query(Pinkunhu2015).filter(Pinkunhu2015.county == 'A县').all()
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
        objs = session.query(Pinkunhu2015).filter(Pinkunhu2015.county == 'B县').all()
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
    m = RandomForestModel()
    m.run()
