#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gesuser.interfaces.agentinterface import GAgentInterface

class Agent:
    def __init__(self, jid, muc_jid, nick, password, server):
        agentInstance = GAgentInterface()
        agentInstance.connect_to_agent(jid, muc_jid, nick, password, self, server)

if __name__=="__main__":
    muc_jid = "%s@conference.%s" % ("clients", "winterfall.local")
    agent = Agent("ldapagent@winterfall.local/GESUSER_Client", muc_jid, "ldapagent", "ldapagent", "winterfall.local")
