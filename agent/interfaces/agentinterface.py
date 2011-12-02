#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gesuser.interfaces.gagent import GAgent

class GAgentInterface:
    def __init__(self):
        self.bot = None
    
    def connect_to_agent(self, jid, nick, password, parent, server=None):
        self.bot = GAgent(jid, nick, password, parent)
        if server:
            self.bot.connect((server, 5222))
        else:
            self.bot.connect(("localhost", 5222))
        self.bot.process(threaded=False)

