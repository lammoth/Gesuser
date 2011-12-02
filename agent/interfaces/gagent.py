#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gesuser.common.gbotxmpp import GBotXMPP

from sleekxmpp.xmlstream.handler.callback import Callback
from sleekxmpp.xmlstream.matcher.xpath import MatchXPath

from gesuser.actions.user_actions import *

# For test purposes
from gesuser.actions.stanzas_test import *

class GAgent(GBotXMPP):
    def __init__(self, jid, nick, passwd=None, parent=None, handlers=None):
        self.mods_list = []
        super(GAgent, self).__init__(jid, nick, passwd, parent)

    def _create_event_handlers(self):
        if self.nick == "user":
            self.registerHandler(Callback('UserIq',
                                          MatchXPath('{%s}iq/{%s}user' % ('jabber:client', 'cga:gesuser3:user')),
                                          self._handle_user_iq
                                          )
                                 )

    def _handle_user_iq(self, stanza):
        print 'Capturing user iq stanza\n'
        user_instance = UserActions()
        user_instance._handle_user_iq(stanza, self)
        
    def check_mods(self):
        if self.nick == "user":
            users_mods = ["ldap","system"]
            self.load_mods(users_mods)
        return self.check_mods_activity()

    def load_mods(self, mod_names):
        mods = __import__("gesuser.mods", fromlist=["*",])
        for m in dir(mods):
            for t in mod_names:
                if m.startswith("mod_" + t):
                    print "Importing mod: '%s'" % m
                    mod = mods.__dict__[m]
                    try:
                        self._register_mod(mod)
                    except Exception, m:
                        print "Error loading mod: '%s'" % m

    def _register_mod(self, mod):
        for k in mod.__dict__.keys():
            if k.upper().startswith("MOD_"):
                dict = {}
                print "Instantiating class '%s'" % k
                o = mod.__dict__[k]()
                print "New mod: %s" % (o.name)
                dict = {"name":o.name,"instance":o,"active":False}
                self.mods_list.append(dict)

    def check_mods_activity(self):
        size_list = len(self.mods_list)
        count_mod = 0
        for m in self.mods_list:
            active_result = m['instance'].isActive()
            if active_result:
                print('Mod %s: Active' % m['name'])
                m['active'] = True
                count_mod = count_mod + 1
            else:
                print('Mod %s: Inactive' % m['name'])
        if size_list == count_mod:
            return True
        else:
            return False

    # For test purposes
    def send_stanza_to_agent(self):

        stanza_type = "user"
        print("Introduce the action type (create,read,update,delete):")
        action_type = raw_input()

        test_instance = TestClass()
        test_instance.create_stanza_iq(str(stanza_type), str(action_type), self)

    # For test purposes
    def send_stanza_result(self):
        print("Set target (Default: q@winterfall.local/GESUSER_Client)")
        target_client = raw_input()
        if not target_client:
            target_client = "q@winterfall.local/GESUSER_Client"
        print("Set response for action (create, read, update, delete):")
        action_type = raw_input()
        if not action_type:
            action_type = "create"
        print("Set response type (result, error):")
        response_type = raw_input()
        if not response_type:
            response_type = "result"
        test_instance = TestClass()
        test_instance.create_response_iq(target_client,action_type,response_type,self)