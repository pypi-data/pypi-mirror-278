#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,pymysql,dbcfg
import database2text.tool as dbtt
from database2text.tool import *

class mysql(object):
    def ana_TABLE(otype):
        for oname, in db.exec("show tables"):
            res=db.res1("show create table %s" %(oname))
            odata=res[1]
            oridata=[]
            coldata=[]
            tdesc=db.res1("SELECT TABLE_COMMENT FROM INFORMATION_SCHEMA.TABLES  WHERE TABLE_NAME ='%s' AND TABLE_SCHEMA = '%s'" %(oname,database))
            md=[]   #markdown等用的字段数据，每字段一个字典
            for i in db.exec2("select * from information_schema.COLUMNS where TABLE_SCHEMA='%s' and table_name='%s' order by ORDINAL_POSITION" %(database,oname)):
                oridata.append(i)
                mddata={"name":i["COLUMN_NAME"], "desc":i["COLUMN_COMMENT"], "type":i["DATA_TYPE"], "size":i["CHARACTER_OCTET_LENGTH"], "null":i["IS_NULLABLE"]=="NO", "default":i["COLUMN_DEFAULT"], "ts":i["COLUMN_TYPE"]}
                md.append(mddata)
            dbdata["sql"]["TABLE"][oname]=odata
            dbdata["exp"]["TABLE"].append({"tname":oname,"tdesc":tdesc,"ori":oridata,"c":coldata,"md":md})
    def getobjtext(otype,oname):
        _,ssql=db.res1("show create %s %s" %(otype,oname))
        return ssql

def readdata(arg):
    dbdata["sql"]={}
    dbdata["exp"]={}
    for i in vars(mysql):
        if i.startswith("ana_"):
            otype=i[4:]
            dbdata["sql"][otype]={}
            dbdata["exp"][otype]=[]
            getattr(mysql,i)(otype)

def connect(arg):
    global database
    if "dbcfg" in stdata:
        database=dbtt.cfg["d"]["database"]
        db.conn=dbtt.dbc.connect()
    else:
        database=stdata["database"]
        if "port" in stdata:
            stdata["port"]=int(stdata["port"])
        stdata.pop("driver")
        db.conn=pymysql.connect(**stdata)

def export(stdata,storidata):
    dbtt.export(stdata,storidata,dbdata)

__all__=[]
