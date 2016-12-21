# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float
from settings import DATABASE


DB_SESSION = None
Base = declarative_base()


def get_db_session():
    """
    获取数据库连接
    """
    global DB_SESSION
    if not DB_SESSION:
        # 初始化数据库连接:
        engine = create_engine('mysql+mysqlconnector://%s:%s@%s:%s/%s' % (
            DATABASE.get('USER'), DATABASE.get('PASSWORD'), DATABASE.get('HOST'),
            DATABASE.get('PORT', 3306), DATABASE.get('NAME'))
        )
        # 创建DBSession类型:
        DB_SESSION = sessionmaker(bind=engine)()
    return DB_SESSION


####################################################################
###### 数据库表 start

class PinkunhuBase(object):
    """ 贫困户表的父类 """
    id = Column(String(20), primary_key=True)
    # 住址
    province = Column(String(36 ))
    city = Column(String(36 ))
    county = Column(String(36 ))
    town = Column(String(36 ))
    village = Column(String(36 ))
    group = Column(String(36 ))
    # 基本情况
    name = Column(String(36 ))
    card_number = Column(String(36 ))
    call_number = Column(String(36 ))

    member_count = Column(Integer())
    bank_name = Column(String(36 ))
    bank_number = Column(String(36 ))
    standard = Column(String(36 ))
    reason = Column(String(36 ))
    other_reason = Column(String(36 ))
    is_back_poor = Column(String(36 ))
    poor_status = Column(String(36 ))
    # 生产生活条件
    arable_land = Column(Float())
    wood_land = Column(Float())
    living_space = Column(Float())
    is_danger_house = Column(String(50 ))
    is_debt = Column(String(50 ))
    debt_total = Column(Float())
    year_total_income = Column(Float())
    person_year_total_income = Column(Float())
    subsidy_total = Column(Float())
    xin_nong_he_total = Column(Float())
    xin_yang_lao_total = Column(Float())
    # 帮扶计划
    help_plan = Column(Text())
    # 五查无看
    tv = Column(String(50 ))
    washing_machine = Column(String(50))
    fridge = Column(String(50))

    ny_is_poor = Column(Integer()) # 下一年是否贫困, 1表示是，0表示否
    ny_total_income = Column(Float()) # 下一年年收入
    ny_person_income = Column(Float()) # 下一年人均年收入


class Pinkunhu2014(PinkunhuBase, Base):
    """ 2014年贫困户表 """
    __tablename__ = 'yunnan_all_pinkunhu_2014'


class Pinkunhu2015(PinkunhuBase, Base):
    """ 2015年贫困户表 """
    __tablename__ = 'yunnan_all_pinkunhu_2015'


class Pinkunhu2016(PinkunhuBase, Base):
    """ 2016年贫困户表 """
    __tablename__ = 'yunnan_all_pinkunhu_2016'

###### 数据库表 end
####################################################################




