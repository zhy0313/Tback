# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy.sql import func
from data.db import get_db_session, Pinkunhu2014, Pinkunhu2015, Pinkunhu2016


def update_next_year():
    """ 更新下一年是否脱贫以及下一年收入数据 """
    step = 100 # 一次取100条数据
    session = get_db_session()
    # 2016年数据
    mappings2016 = {}
    min_id, max_id = session.query(func.min(Pinkunhu2016.id), func.max(Pinkunhu2016.id)).one()
    while min_id <= max_id:
        objs = session.query(Pinkunhu2016).filter(Pinkunhu2016.id >= min_id, Pinkunhu2016.id <= min_id + step).all()
        for item in objs:
            mappings2016[item.card_number] = True
            mappings2016[item.card_number+'year_total_income'] = item.year_total_income
            mappings2016[item.card_number+'person_year_total_income'] = item.person_year_total_income

        min_id += step
        print 'min_id:%s' % min_id

    # 2015年数据
    mappings2015 = {}
    min_id, max_id = session.query(func.min(Pinkunhu2015.id), func.max(Pinkunhu2015.id)).one()
    while min_id <= max_id:
        objs = session.query(Pinkunhu2015).filter(Pinkunhu2015.id >= min_id, Pinkunhu2015.id <= min_id + step).all()
        for item in objs:
            # 存取2015年数据
            mappings2015[item.card_number] = True
            mappings2015[item.card_number+'year_total_income'] = item.year_total_income
            mappings2015[item.card_number+'person_year_total_income'] = item.person_year_total_income

            # 设置下一年数据
            if mappings2016.get(item.card_number):
                item.ny_is_poor = 1
                item.ny_total_income = mappings2016[item.card_number+'year_total_income']
                item.ny_person_income = mappings2016[item.card_number+'person_year_total_income']
            else:
                print item.id, '不存在'

        min_id += step
        print 'min_id:%s' % min_id

    # 2014年数据
    min_id, max_id = session.query(func.min(Pinkunhu2014.id), func.max(Pinkunhu2014.id)).one()
    while min_id <= max_id:
        objs = session.query(Pinkunhu2014).filter(Pinkunhu2014.id >= min_id, Pinkunhu2014.id <= min_id + step).all()
        for item in objs:
            # 设置下一年数据
            if mappings2015.get(item.card_number):
                item.ny_is_poor = 1
                item.ny_total_income = mappings2015[item.card_number+'year_total_income']
                item.ny_person_income = mappings2015[item.card_number+'person_year_total_income']
            else:
                print item.id, '不存在'

        min_id += step
        print 'min_id:%s' % min_id

    session.flush()
    session.commit()


if __name__ == "__main__":
    update_next_year()
