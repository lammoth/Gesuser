#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sleekxmpp.xmlstream.stanzabase import ET
from sleekxmpp.basexmpp import *

from gesuser.common.customstanzahandler import *

class TestClass(object):
    def create_stanza_iq(self, stanza_type, action_type, parent):
        # For now all stanza types are "user"
        print action_type
        if stanza_type == "user":
            if action_type == "create":
                iq = self.create_user_stanza(parent)
                print iq
                iq.send()
            elif action_type == "read":
                print "entrando en read"
                iq = self.read_user_stanza(parent)
                print iq
                iq.send()
            elif action_type == "update":
                iq = self.update_user_stanza(parent)
                print iq
                iq.send()
            elif action_type == "delete":
                iq = self.delete_user_stanza(parent)
                print iq
                iq.send()

    def create_response_iq(self,target_client,action_type,response_type, parent):
        if action_type == "create":
            iq = self.create_response(response_type,parent,target_client)
            iq.attrib['action'] = "create"
        elif action_type == "read":
            iq = self.read_response(response_type,parent,target_client)
            iq.attrib['action'] = "read"
        elif action_type == "update":
            iq = self.create_response(response_type,parent,target_client)
            iq.attrib['action'] = "update"
        elif action_type == "delete":
            iq = self.create_response(response_type,parent,target_client)
            iq.attrib['action'] = "delete"

        iq.send()

    def create_user_stanza(self, parent):
        iq = parent.make_iq_set(sub=None, ito="user@winterfall.local/GESUSER_Client", ifrom=None, iq=None)
        #iq = parent.make_iq(self, id=0, ifrom=None, ito=None, itype=None, iquery=None)

        item = {'uid':'pepearnesto','pwd':'pepe','gecos':'Pepe Arnesto','quota':'250','course':'3','group':'1','type':'1'}

        # Field uid
        obj_uid = ET.Element('uid')
        obj_uid.text = item['uid']
        # Field pwd
        obj_pwd = ET.Element('pwd')
        obj_pwd.text = item['pwd']
        # Field gecos
        obj_gecos = ET.Element('gecos')
        obj_gecos.text = item['gecos']
        # Field quota
        obj_quota = ET.Element('quota')
        obj_quota.text = item['quota']
        # Field course
        obj_course = ET.Element('course')
        obj_course.text = item['course']
        # Field group
        obj_group = ET.Element('group')
        obj_group.text = item['group']
        # Field profile
        obj_profile = ET.Element('type')
        obj_profile.text = item['type']
        # Make a item element
        obj_item = ET.Element('user')
        obj_item.attrib['xmlns'] = "cga:gesuser3:user"
        obj_item.attrib['action'] = "create"

        obj_item.append(obj_uid)
        obj_item.append(obj_pwd)
        obj_item.append(obj_gecos)
        obj_item.append(obj_quota)
        obj_item.append(obj_course)
        obj_item.append(obj_group)
        obj_item.append(obj_profile)
        iq.append(obj_item)

        return iq

    def read_user_stanza(self, parent):
        #iq = parent.make_iq_get(sub=None, ito="usersagent@winterfall.local/GESUSER_Client", ifrom=None, iq=None)
        iq = parent.make_iq_get(queryxmlns=None, ito="user@winterfall.local/GESUSER_Client", ifrom=None, iq=None)
        # Make a item element
        obj_item = ET.Element('user')
        obj_item.attrib['xmlns'] = "cga:gesuser3:user"
        obj_item.attrib['action'] = "read"


        # Field uid
        obj_uid = ET.Element('uid')
        obj_uid.text = "o"
        obj_uid.attrib['op'] = "eq"
        # Field gecos
        obj_gecos = ET.Element('gecos')
        obj_gecos.text = "e"
        obj_gecos.attrib['op'] = "eq"
        # Field quota
        obj_quota = ET.Element('quota')
        obj_quota.text = "100"
        obj_quota.attrib['op'] = "gt"
        # Field course
        obj_course = ET.Element('course')
        obj_course.text = "5"
        obj_course.attrib['op'] = "le"
        # Field group
        obj_group = ET.Element('group')
        obj_group.text = "2"
        obj_group.attrib['op'] = "eq"
        # Field profile
        obj_profile = ET.Element('profile')
        obj_profile.text = "2"
        obj_profile.attrib['op'] = "ap"



        obj_item.append(obj_uid)
        obj_item.append(obj_gecos)
        obj_item.append(obj_quota)
        obj_item.append(obj_course)
        obj_item.append(obj_group)
        obj_item.append(obj_profile)
        iq.append(obj_item)
        print iq

        return iq

    def update_user_stanza(self, parent):
        iq = parent.make_iq_set(sub=None, ito="user@winterfall.local/GESUSER_Client", ifrom=None, iq=None)
        #iq = parent.make_iq(self, id=0, ifrom=None, ito=None, itype=None, iquery=None)

        item = {'uid':'pepearnesto','pwd':'pepito','gecos':'Pepe Arnestorrrr','quota':'200','course':'4','group':'2','profile':'2'}

        # Field uid
        obj_uid = ET.Element('uid')
        obj_uid.text = item['uid']
        # Field pwd
        obj_pwd = ET.Element('pwd')
        obj_pwd.text = item['pwd']
        # Field gecos
        obj_gecos = ET.Element('gecos')
        obj_gecos.text = item['gecos']
        # Field quota
        obj_quota = ET.Element('quota')
        obj_quota.text = item['quota']
        # Field course
        obj_course = ET.Element('course')
        obj_course.text = item['course']
        # Field group
        obj_group = ET.Element('group')
        obj_group.text = item['group']
        # Field profile
        obj_profile = ET.Element('profile')
        obj_profile.text = item['profile']
        # Make a item element
        obj_item = ET.Element('user')
        obj_item.attrib['xmlns'] = "cga:gesuser3:user"
        obj_item.attrib['action'] = "update"

        obj_item.append(obj_uid)
        obj_item.append(obj_pwd)
        obj_item.append(obj_gecos)
        obj_item.append(obj_quota)
        obj_item.append(obj_course)
        obj_item.append(obj_group)
        obj_item.append(obj_profile)
        iq.append(obj_item)

        return iq

    def delete_user_stanza(self, parent):
        iq = parent.make_iq_set(sub=None, ito="user@winterfall.local/GESUSER_Client", ifrom=None, iq=None)
        #iq = parent.make_iq(self, id=0, ifrom=None, ito=None, itype=None, iquery=None)

        item = {'uid':'epepes'}

        # Field uid
        obj_uid = ET.Element('uid')
        obj_uid.text = item['uid']

        obj_item = ET.Element('user')
        obj_item.attrib['xmlns'] = "cga:gesuser3:user"
        obj_item.attrib['action'] = "delete"

        obj_item.append(obj_uid)
        iq.append(obj_item)

        return iq

    def create_response(self,response_type,parent,target):
        iq = parent.make_iq_result(id="3", ito=target, ifrom=None, iq=None)
        if response_type == "result":
            pass
        else:
            obj_error = ET.Element('error')
            obj_error.attrib['code'] = "501"
            obj_error.text = "Deafult error"
            iq.append(obj_error)
        return iq

    def read_response(self,response_type,parent,target):
        iq = parent.make_iq_result(id="3", ito=target, ifrom=None, iq=None)
        if response_type == "result":
            # Field uid
            obj_uid = ET.Element('uid')
            obj_uid.text = "pepe"
            # Field gecos
            obj_gecos = ET.Element('gecos')
            obj_gecos.text = "pepe garcia"
            # Field quota
            obj_quota = ET.Element('quota')
            obj_quota.text = "250"
            # Field course
            obj_course = ET.Element('course')
            obj_course.text = "3"
            # Field group
            obj_group = ET.Element('group')
            obj_group.text = "10000"
            # Field profile
            obj_profile = ET.Element('type')
            obj_profile.text = "fijo"
            # Make a item element
            obj_item = ET.Element('item')
            obj_item.append(obj_uid)
            obj_item.append(obj_gecos)
            obj_item.append(obj_quota)
            obj_item.append(obj_course)
            obj_item.append(obj_group)
            obj_item.append(obj_profile)
            iq.append(obj_item)
            ###########################################33
            # Field uid
            obj_uid2 = ET.Element('uid')
            obj_uid2.text = "jose"
            # Field gecos
            obj_gecos2 = ET.Element('gecos')
            obj_gecos2.text = "jose gil"
            # Field quota
            obj_quota2 = ET.Element('quota')
            obj_quota2.text = "100"
            # Field course
            obj_course2 = ET.Element('course')
            obj_course2.text = "7"
            # Field group
            obj_group2 = ET.Element('group')
            obj_group2.text = "10001"
            # Field profile
            obj_profile2 = ET.Element('type')
            obj_profile2.text = "movil"
            # Make a item element
            obj_item2 = ET.Element('item')
            obj_item2.append(obj_uid2)
            obj_item2.append(obj_gecos2)
            obj_item2.append(obj_quota2)
            obj_item2.append(obj_course2)
            obj_item2.append(obj_group2)
            obj_item2.append(obj_profile2)
            iq.append(obj_item2)
        else:
            obj_error = ET.Element('error')
            obj_error.attrib['code'] = "501"
            obj_error.text = "Default error"
            iq.append(obj_error)
        return iq