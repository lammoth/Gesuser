#!/usr/bin/env python
# -*- coding: utf-8 -*-

import couchdb
from gesuser.datahandlers.couchdb.views.couchdb_views import *

class ConnectToCouch:
    def __init__(self, server=None, port=None):
        print "Initializing CouchDB"
        self.couchserver = None
        self.server = server
        self.port = port
        self.database = None
        
    def connect(self, db):
        if not self.server:
            self.server = "localhost"
        if not self.port:
            self.port = "5984"
        location = "http://" + self.server + ":" + self.port + "/"
        self.couchserver = couchdb.Server(location)
        self.getDatabase(db)
        
    def createDatabase(self, db):
        self.database = self.couchserver.create(db)
        
    def getDatabase(self, db):
        try:
            self.database = self.couchserver[db]
        except:
            self.createDatabase(db) 
        
    ################
    # CRUD Methods #
    ################
        
    def createDocument(self, dict):
        # This method is for most newest version
        # self.database.save(doc)
        # doc_type field specify a table in MySQL
        doc = dict
        try:
            self.database.create(doc)
        except Exception as e:
            for error in e:
                if error == "conflict":
                    self.updateDocument(doc['_id'], doc)
    
    # Receives a list with the field to search
    # Return a dictionary with document fields
    def readDocument(self, fields=None):
        data_list = []
        if  fields:
            map = SPEC_DOC % fields
        else:
            map = ALL_DOCS
        result = self.database.query(map)
        for data in result:
            data_list.append(data.value)
        return data_list
    
    def updateDocument(self, docId, data):
        result = self.readDocument(("doc._id",docId))
        for r in result:
            for key in r:
                if key != "_id" and key != "_rev":
                    r[key] = data[key]
            self.createDocument(r)
    
    def delDocument(self, ids):
        for id in ids:
            del self.database[id]
    
class UserDocument:
    def __init__(self, connection):
        self.userFields = {}
        self.connection = connection
    
    def createUserReg(self, data):
        # Data is a dict formed by the following fields:
        # User UID, user password, user gecos,
        # user type, user quota, user course,
        # user group, user role
        self.userFields = data
        self.connection.createDocument(self.userFields)