#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gesuser.interfaces.agentinterface import GAgentInterface

class Agent:
    def __init__(self, jid, nick, password, server):
        agentInstance = GAgentInterface()
        agentInstance.connect_to_agent(jid, nick, password, self, server)

if __name__=="__main__":
    muc_jid = "%s@conference.%s" % ("clients", "winterfall.local")
    agent = Agent("user@winterfall.local/GESUSER_Client", "user", "user", "winterfall.local")
