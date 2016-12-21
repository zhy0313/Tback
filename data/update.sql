-- 给原表增加 下一年是否贫困、下一年年收入、下一年人均年收入 字段
alter table `yunnan_all_pinkunhu_2014`
ADD COLUMN  `ny_is_poor` int(11) DEFAULT 0,
ADD COLUMN  `ny_total_income` double DEFAULT -1,
ADD COLUMN  `ny_person_income` double DEFAULT -1;

alter table `yunnan_all_pinkunhu_2015`
ADD COLUMN  `ny_is_poor` int(11) DEFAULT 0,
ADD COLUMN  `ny_total_income` double DEFAULT -1,
ADD COLUMN  `ny_person_income` double DEFAULT -1;


alter table `yunnan_all_pinkunhu_2016`
ADD COLUMN  `ny_is_poor` int(11) DEFAULT 0,
ADD COLUMN  `ny_total_income` double DEFAULT -1,
ADD COLUMN  `ny_person_income` double DEFAULT -1;

-- TODO: 执行 `PYTHONPATH=. python data/dbutil.py` 以更新上面3个字段的信息

-- 新建开源用的数据库

CREATE DATABASE `poormining` CHARACTER SET utf8;

---- 填充2个县的数据

-- 贫困户数据
CREATE TABLE poormining.yunnan_all_pinkunhu_2014
AS
SELECT * FROM data_fupin.yunnan_all_pinkunhu_2014 where county='镇雄县' or county ='彝良县';

CREATE TABLE poormining.yunnan_all_pinkunhu_2015
AS
SELECT * FROM data_fupin.yunnan_all_pinkunhu_2015 where county='镇雄县' or county ='彝良县';

CREATE TABLE poormining.yunnan_all_pinkunhu_2016
AS
SELECT * FROM data_fupin.yunnan_all_pinkunhu_2016 where county='镇雄县' or county ='彝良县';

-- 去除秘密字段
update `yunnan_all_pinkunhu_2014` set `name` = concat(left(`name`, 1), '**'), `bank_name`= concat(left(`bank_number`, 0), '******'), `bank_number` = concat(left(`bank_number`, 0), '******'),`bank_name`= concat(left(`bank_number`, 0), '******'), `bank_number` = concat(left(`bank_number`, 0), '******'),`call_number` = concat(left(`call_number`, 3), '********'),`card_number` = '', `province`='', `city`='', `town`='', `village`='', `group`='';
update `yunnan_all_pinkunhu_2015` set `name` = concat(left(`name`, 1), '**'), `bank_name`= concat(left(`bank_number`, 0), '******'), `bank_number` = concat(left(`bank_number`, 0), '******'),`call_number` = concat(left(`call_number`, 3), '********'),`card_number` = '', `province`='', `city`='', `town`='', `village`='', `group`='';
update `yunnan_all_pinkunhu_2016` set `name` = concat(left(`name`, 1), '**'), `bank_name`= concat(left(`bank_number`, 0), '******'), `bank_number` = concat(left(`bank_number`, 0), '******'),`call_number` = concat(left(`call_number`, 3), '********'),`card_number` = '', `province`='', `city`='', `town`='', `village`='', `group`='';

update `yunnan_all_pinkunhu_2014` set `county` = 'A县' where `county` = '镇雄县';
update `yunnan_all_pinkunhu_2015` set `county` = 'A县' where `county` = '镇雄县';
update `yunnan_all_pinkunhu_2016` set `county` = 'A县' where `county` = '镇雄县';

update `yunnan_all_pinkunhu_2014` set `county` = 'B县' where `county` = '彝良县';
update `yunnan_all_pinkunhu_2015` set `county` = 'B县' where `county` = '彝良县';
update `yunnan_all_pinkunhu_2016` set `county` = 'B县' where `county` = '彝良县';

-- 贫困家庭数据
CREATE TABLE poormining.yunnan_all_pinkunjiating_2014
AS
SELECT * FROM data_fupin.yunnan_all_pinkunjiating_2014 where county='镇雄县' or county ='彝良县';

CREATE TABLE poormining.yunnan_all_pinkunjiating_2015
AS
SELECT * FROM data_fupin.yunnan_all_pinkunjiating_2015 where county='镇雄县' or county ='彝良县';

CREATE TABLE poormining.yunnan_all_pinkunjiating_2016
AS
SELECT * FROM data_fupin.yunnan_all_pinkunjiating_2016 where county='镇雄县' or county ='彝良县';

-- 去除秘密字段
update `yunnan_all_pinkunjiating_2014` set `member_name` = concat(left(`member_name`, 1), '**'), `member_card_number` = '', `name` = concat(left(`name`, 1), '**'), `card_number` = '', `province`='', `city`='', `town`='', `village`='', `group`='';
update `yunnan_all_pinkunjiating_2015` set `member_name` = concat(left(`member_name`, 1), '**'), `member_card_number` = '', `name` = concat(left(`name`, 1), '**'), `card_number` = '', `province`='', `city`='', `town`='', `village`='', `group`='';
update `yunnan_all_pinkunjiating_2016` set `member_name` = concat(left(`member_name`, 1), '**'), `member_card_number` = '', `name` = concat(left(`name`, 1), '**'), `card_number` = '', `province`='', `city`='', `town`='', `village`='', `group`='';

update `yunnan_all_pinkunjiating_2014` set `county` = 'A县' where `county` = '镇雄县';
update `yunnan_all_pinkunjiating_2015` set `county` = 'A县' where `county` = '镇雄县';
update `yunnan_all_pinkunjiating_2016` set `county` = 'A县' where `county` = '镇雄县';

update `yunnan_all_pinkunjiating_2014` set `county` = 'B县' where `county` = '彝良县';
update `yunnan_all_pinkunjiating_2015` set `county` = 'B县' where `county` = '彝良县';
update `yunnan_all_pinkunjiating_2016` set `county` = 'B县' where `county` = '彝良县';

-- 帮扶人
CREATE TABLE poormining.yunnan_all_bangfuren_2014
AS
SELECT * FROM data_fupin.yunnan_all_bangfuren_2014 where county='镇雄县' or county ='彝良县';

CREATE TABLE poormining.yunnan_all_bangfuren_2015
AS
SELECT * FROM data_fupin.yunnan_all_bangfuren_2015 where county='镇雄县' or county ='彝良县';

CREATE TABLE poormining.yunnan_all_bangfuren_2016
AS
SELECT * FROM data_fupin.yunnan_all_bangfuren_2016 where county='镇雄县' or county ='彝良县';

-- 去除秘密字段
update `yunnan_all_bangfuren_2014` set `bangfu_name` = concat(left(`bangfu_name`, 1), '**'), `call_number` = concat(left(`call_number`, 1), '**'), `province`='', `city`='', `town`='', `village`='', `group`='', `company_name`='', `company_address`='';
update `yunnan_all_bangfuren_2015` set `bangfu_name` = concat(left(`bangfu_name`, 1), '**'), `call_number` = concat(left(`call_number`, 1), '**'), `province`='', `city`='', `town`='', `village`='', `group`='', `company_name`='', `company_address`='';
update `yunnan_all_bangfuren_2016` set `bangfu_name` = concat(left(`bangfu_name`, 1), '**'), `call_number` = concat(left(`call_number`, 1), '**'), `province`='', `city`='', `town`='', `village`='', `group`='', `company_name`='', `company_address`='';


update `yunnan_all_bangfuren_2014` set `county` = 'A县' where `county` = '镇雄县';
update `yunnan_all_bangfuren_2015` set `county` = 'A县' where `county` = '镇雄县';
update `yunnan_all_bangfuren_2016` set `county` = 'A县' where `county` = '镇雄县';

update `yunnan_all_bangfuren_2014` set `county` = 'B县' where `county` = '彝良县';
update `yunnan_all_bangfuren_2015` set `county` = 'B县' where `county` = '彝良县';
update `yunnan_all_bangfuren_2016` set `county` = 'B县' where `county` = '彝良县';
