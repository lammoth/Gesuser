#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from sleekxmpp.xmlstream.stanzabase import ElementBase
from sleekxmpp.basexmpp import *

from gesuser.common.customstanzahandler import *

class UserActions(object):
    def _handle_user_iq(self, stanza, parent):
        # Core instance
        self.core = parent
        self.mods = []
        is_active = False
        count = 0

        # Elements to compose the answer
        stanza_id = stanza.xml.attrib['id']
        stanza_to = stanza.xml.attrib['to']
        stanza_from = stanza.xml.attrib['from']

        # Set mod instance to work with actions
        while not is_active or count == 42:
            # Yes, 42 ... because I can ... I know the truth
            is_active = self._activate_modules()
            time.sleep(0.17)
            count += 1
            if count == 42 and not is_active:
                break
        
        # If the mods are not active send and error
        if not is_active:
            dict_error = {"code":"404","msg":"Unavailable mods","type":""}
            result = iqClass.create_result_iq(parent, dict_error, id_stanza=stanza_id)
            iqClass.send_custom_iq(stanza_from, stanza_to, result)
        else:
            # User skill instance
            register_stanza_plugin(UserIq, UserIqPlugin)
            stanza_data = UserIq(stanza.xml)

            # Exec pertinent user actions
            result_exec = self._exec_user_action(stanza_data)

            # Custom IQ skill instance
            iqClass = IqCustomMessage()

            # Making the answer
            result = iqClass.create_result_iq(parent, result_exec, id_stanza=stanza_id)
            iqClass.send_custom_iq(stanza_from, stanza_to, result)

    def _exec_user_action(self, stanza):
        data = {}
        mod = None
        if stanza['user']['action']:

            for m in self.mods:
                if m['name'] == "MOD_LDAP":
                    mod = m['instance']

            data['action'] = stanza['user']['action']

            if data['action'] == "create":
                result = self._create_user_data(mod,stanza)
                return result
            elif data['action'] == "update":
                result = self._update_user_data(mod,stanza)
                return result
            elif data['action'] == "delete":
                result = self._remove_user_data(mod,stanza)
                return result
            elif data['action'] == "read":
                result = self._read_user_data(mod,stanza)
                return result
        else:
            pass

    # Result dict must be by this way:
    # {"code":"404","msg":"service unavailable","type":"create","stanza":"user","items":[{},{}]}
    def _create_user_data(self, mod, data):
        d = mod.create_user(data)
        dict = {"code":d['error'],"msg":d['desc'],"type":"create","stanza":"user"}
        return dict

    def _update_user_data(self, mod, data):
        d = mod.update_user(data)
        dict = {"code":d['error'],"msg":d['desc'],"type":"update","stanza":"user"}
        return dict

    def _remove_user_data(self, mod, data):
        d = mod.delete_user(data['user']['uid'])
        dict = {"code":d['error'],"msg":d['desc'],"type":"delete","stanza":"user"}
        return dict

    def _read_user_data(self, mod, data):
        d = mod.read_user(data)
        dict = {"code":d['error'],
                "msg":d['desc'],
                "type":"read",
                "stanza":"user",
                "items":d['data']
                }
        return dict

    def _activate_modules(self):
        self.mods = []
        for mod in self.core.mods_list:
            if mod['name'] == "MOD_LDAP":
                if mod['active']:
                    self.mods.append({'name':'MOD_LDAP', 'instance':mod['instance']})
                    #return True
                else:
                    self.core.check_mods()
            if mod['name'] == "MOD_SYSTEM":
                if mod['active']:
                    self.mods.append({'name':'MOD_SYSTEM', 'instance':mod['instance']})
                    #return True
                else:
                    self.core.check_mods()
                    
        if self.mods:
            return True
        else:
            return False
 
 
# Class to get user data
class UserIqPlugin(ElementBase):
    namespace = 'cga:gesuser3:user'
    name = 'user'
    plugin_attrib = 'user'
    interfaces = set(('action', 'uid', 'pwd', 'gecos', 'profile', 'quota', 'course', 'group', 'role', 'order'))
    sub_interfaces = set(('uid', 'pwd', 'gecos', 'profile', 'quota', 'course', 'group', 'role', 'order'))
        

# Class to process user data
class UserIq(ElementBase):
    namespace = 'jabber:client'
    name = 'iq'
    plugin_attrib = 'iq'
    interfaces = set(('type',))