# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from collections import OrderedDict
from data.db import get_db_session, Pinkunhu2015

MAPPINGS = {
  "tv": {
    "null": 1,
    "黑白": 2,
    "彩色": 3
  },
  "washing_machine": {
    "null": 1,
    "半自": 2,
    "全自": 3
  },
  "fridge": {
    "null": 1,
    "单门": 2,
    "双门": 3
  },
  "reason": {
    "缺技术": 1,
    "缺劳动力": 2,
    "缺资金": 3,
    "因残": 4,
    "因灾": 5,
    "因病": 6,
    "缺水": 7,
    "缺土地": 8,
    "交通条件落后": 9,
    "自身发展动力不足": 10,
    "因学": 11,
    "其它": 12,
    "null": 13
  },
  "is_danger_house": {
    "是": 1,
    "null": 2,
    "否": 3
  },
  "is_back_poor": {
    "否": 1,
    "是": 0
  },
  "is_debt": {
    "null": 1,
    "无": 2,
    "有": 3
  },
  "poor_status": {
    "已脱贫": 1,
    "预脱贫": 2,
    "贫困": 3,
    "null": 4
  },
  "standard": {
    "国家标准": 1,
    "省定标准": 2,
    "市定标准": 3,
    "null": 4
  }
}


def get_normalize():
    """ 根据数据库列值自动生成标量的map
        文件头部的 MAPPINGS 就是用该方法生成的
    """
    session = get_db_session()
    # 字符串标量 转化成数字标量
    res = OrderedDict()
    for col in ['reason', 'is_danger_house', 'is_back_poor', 'is_danger_house', 'is_debt',
                'poor_status', 'standard']:
        data = OrderedDict()
        idx = 1
        for item, in session.query(getattr(Pinkunhu2015, col)).distinct():
            data[item] = idx
            idx += 1
        res[col] = data
    print json.dumps(res, ensure_ascii=False, indent=2)


def normalize(key, value):
    """
    将数据库对应列的值转化成数字标量或者数值
    :param key: 数据库列名
    :param value: 数据库列值
    :return: 数字标量或者数值
    """
    # 个别字段特殊处理
    if key in ['tv', 'washing_machine', 'fridge']:
        value = "null" if value is None else value[:2]
    # 字符串标量 转化成数字标量
    global MAPPINGS
    if key in ['tv', 'washing_machine', 'fridge',
               'reason', 'is_danger_house', 'is_back_poor', 'is_danger_house', 'is_debt', 'standard',
               'poor_status']:
        value = "null" if value is None else value
        return MAPPINGS[key][value]
    # 数值
    if key in ['arable_land', 'debt_total', 'living_space', 'member_count', 'person_year_total_income',
               'year_total_income', 'subsidy_total', 'wood_land', 'xin_nong_he_total', 'xin_yang_lao_total',
               'ny_is_poor', 'ny_total_income', 'ny_person_income']:
        return value or 0
    # 布尔
    if key in ['call_number', 'bank_name', 'bank_number', 'help_plan']:
        return 1 if value else 0


def get_normalized_data():
    """ 获取格式化后的数据 """
    session = get_db_session()
    objs = session.query(Pinkunhu2015).filter(Pinkunhu2015.county == 'A县').all()
    X, Y = [], []
    for item in objs:
        col_list = []
        for col in [
            'tv', 'washing_machine', 'fridge',
            'reason', 'is_danger_house', 'is_back_poor',  'is_debt', 'standard',
            'arable_land', 'debt_total', 'living_space', 'member_count', 'person_year_total_income',
            'year_total_income', 'subsidy_total', 'wood_land', 'xin_nong_he_total', 'xin_yang_lao_total',
            'call_number', 'bank_name', 'bank_number', 'help_plan'
        ]:

            normalized_value = normalize(col, getattr(item, col))
            col_list.append(normalized_value)
        X.append(col_list)
        normalized_value = normalize('poor_status', getattr(item, 'poor_status'))
        Y.append(normalized_value)

    return X, Y


def get_test_normalized_data():
    """ 获取格式化后的数据 """
    session = get_db_session()
    objs = session.query(Pinkunhu2015).filter(Pinkunhu2015.county == 'B县').all()
    X, Y = [], []
    for item in objs:
        col_list = []
        for col in [
            'tv', 'washing_machine', 'fridge',
            'reason', 'is_danger_house', 'is_back_poor',  'is_debt', 'standard',
            'arable_land', 'debt_total', 'living_space', 'member_count', 'person_year_total_income',
            'year_total_income', 'subsidy_total', 'wood_land', 'xin_nong_he_total', 'xin_yang_lao_total',
            'call_number', 'bank_name', 'bank_number', 'help_plan'
        ]:

            normalized_value = normalize(col, getattr(item, col))
            col_list.append(normalized_value)
        X.append(col_list)
        normalized_value = normalize('poor_status', getattr(item, 'poor_status'))
        Y.append(normalized_value)

    return X, Y


if __name__ == "__main__":
    # get_data()
    # update_zhengxiong_2015()
    get_normalize()
