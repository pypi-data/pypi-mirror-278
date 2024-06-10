#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import database2text.tool as dbtt
from database2text.tool import *

__all__=["connect","readdata"]

class mssql(object):
    def ana_TABLE(otype):
        字段类型={}
        dbdata["sql"]["TABLE"]={}
        dbdata["exp"]["TABLE"]=[]
        for 类型id,名称 in db.exec("select system_type_id,name from sys.types"):
            字段类型[类型id]=名称
        sql="SELECT table_catalog,table_schema,table_name FROM INFORMATION_SCHEMA.TABLES where table_type='BASE TABLE'"
        if 目录:
            sql=f"{sql} and table_catalog='{目录}'"
        if 集合:
            sql=f"{sql} and table_schema='{集合}'"
        for catalog,schema,表名 in db.exec(sql).fetchall():
            表id=db.res1(f"select object_id('{catalog}.{schema}.{表名}')")
            注释=db.res1(f"select value from sys.extended_properties where major_id={表id} and class=1 and name='MS_Description'")
            原始信息=[]
            md=[]
            for i in db.exec2(f"select * from sys.columns where object_id={表id} order by column_id"):
                原始信息.append(i)
                md.append({"name": i["name"],"desc": '',"type": 字段类型[i["system_type_id"]], "size":i["max_length"],"null":i["is_nullable"], "default":""})
            dbdata["sql"]["TABLE"][表名]=[]   #暂不处理
            dbdata["exp"]["TABLE"].append({"tname":表名,"tdesc":注释,"ori":原始信息,"c":[],"md":md})

def readdata(arg):
    global 读参数,目录,集合
    目录=arg.get("目录","") or arg.get("catalog","")
    集合=arg.get("集合","") or arg.get("schema","")
    读参数=arg
    dbdata["sql"]={}
    dbdata["exp"]={}
    for i in vars(mssql):
        if i.startswith("ana_"):
            otype=i[4:]
            dbdata["sql"][otype]={}
            dbdata["exp"][otype]=[]
            getattr(mssql,i)(otype)

def connect(arg):
    '连接到mssql数据库'
    return dbtt.connect(arg,"pytds")

def export(stdata,storidata):
    dbtt.export(stdata,storidata,dbdata)
