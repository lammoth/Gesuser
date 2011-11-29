#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from gesuser.datahandlers.mysql.views.mysql_views import *

class ConnectToMysql:
    def __init__(self, server=None, port=None, username=None, password=None):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.database = None
        self.cursor = None
        self.dbname = None
        
    def connect(self, db):
        if not self.server:
            self.server = "localhost"
        if not self.port:
            self.port = "3306"
            
        self.getDatabase(db)        
        
    def createDatabase(self, db):
        self.database = MySQLdb.connect(host=self.server,
                                           port=self.port,
                                           user=self.username,
                                           passwd=self.password)
        self.cursor = self.database.cursor()
        self.cursor.execute = (CREATE_DATABASE % db)
        self.database = MySQLdb.connect(host=self.server,
                                           port=self.port,
                                           user=self.username,
                                           passwd=self.password,
                                           db=db)
        self.cursor = self.database.cursor()
        
    def getDatabase(self, db):
        try:
            self.database = MySQLdb.connect(host=self.server,
                                           port=self.port,
                                           user=self.username,
                                           passwd=self.password,
                                           db=db)
            self.cursor = self.database.cursor()
        except:
            self.createDatabase(db)

        
    ################
    # CRUD Methods #
    ################
    
    def createDocument(self, dict):
        # doc_type field specify a table in MySQL
        table_exist = False
        self.cursor.execute(SHOW_TABLES)
        tables_list = self.cursor.fetchall()
        for table in tables_list:
            for t in table:
                if t == dict['doc_type']:
                    self.dbname = dict['doc_type']
                    table_exist = True
                    data = self.insertData(dict)
                    sql_insert = INSERT_DOCUMENT_PREFIX % self.dbname + data
                    print sql_insert
                    self.cursor.execute(sql_insert)
        
        #if not table_exist:
        #    self.createTable(dict['doc_type'])
        #    self.dbname = dict['doc_type']
        #    data = self.insertData(dict)
        #    sql_insert = INSERT_DOCUMENT_PREFIX + data
        #    self.cursor.execute(sql_insert)
        
    def insertData(self, dict):
        #(a,b,c) VALUES (1,2,3)
        str = "("
        keys_str = ""
        for key in dict.keys():
            if key != "doc_type":
                keys_str = keys_str + key + ","
        str_main_keys = keys_str[:-1] + ")"
        keys_data = str + str_main_keys
        
        values_str = ""
        for value in dict.values():
            if value != self.dbname:
                values_str = values_str + "'" + value + "'" + ","
        str_main_values = values_str[:-1] + ")"
        values_data = str + str_main_values
        
        main_str = keys_data + " VALUES " + values_data
        return main_str   
        
    def createTable(self, dict):
        prefix = CREATE_TABLE_PREFIX % dict['doc_type']
        fields_data = "("
        for field in dict['fields']:
            #{"doc_type":"test","fields":[{"field":"id","type":" int","options":""}
            fields_data = fields_data + field['field'] + field['type'] + field['options'] + ","
        fields = fields_data[:-1] + ")"
        sql = prefix + fields + CREATE_TABLE_SUFIX
        print sql
        self.cursor.execute(sql)
    
    # Receives a list with the field to search
    # Return a dictionary with document fields
    def readDocument(self, fields=None):
        sql = READ_DATA % fields
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def updateDocument(self, docId, data):
        sql = UPDATE_DATA_PREFIX % data['doc_type']
        if len(data) > 1:
            for key in data.keys():
                if key != "key_value" and key != "doc_type":
                    sql = sql + data[key] + ","
        sql = sql[:-1]
        sufix = " WHERE %s=%s" % (docId, data['key_value'])
        sql = sql + sufix
        print sql
        self.cursor.execute(sql)
    
    def delDocument(self, ids):
        if len(ids) > 1:
            sql = DELETE_SPEC_DOC % ids
        else:
            sql = DELETE_DOCS % ids
        self.cursor.execute(sql)
        return self.cursor.fetchall()