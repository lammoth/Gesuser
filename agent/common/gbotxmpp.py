# -*- coding: utf-8 -*-
## \namespace common

import sleekxmpp
import time
from threading import Thread

class GBotXMPP(sleekxmpp.ClientXMPP):
    def __init__(self, jid, nick, passwd="anonymous", parent=None):
        print 'XMPP bot initialization\n'
        sleekxmpp.ClientXMPP.__init__(self, jid, passwd)
        self.core = parent
        self.nick = nick
        self.thread = None
       
        # Load the needed XEP's
        self._load_plugins()

        # Sets common event handlers
        self._load_event_handlers()
        
        # Create custom event handlers
        self._create_event_handlers()
        
        #self._check_items()

        print 'Sleekxmpp trace\n'

    ## \fn _load_plugins(self)
    #  \brief Load sleekxmpp's plugins needed 
    def _load_plugins(self):
        for p in ["xep_0030", "xep_0045", "xep_0060"]:
            print "Loading plugin %s" % p
            self.registerPlugin(p)
        self.disco = self["xep_0030"]
        self.muc = self["xep_0045"]
        self.pubsub = self["xep_0060"]

    ## \fn _load_event_handlers(self)
    #  \brief Load event handlers for session start
    def _load_event_handlers(self):
        self.add_event_handler("session_start", self._session_start)
        self.add_event_handler("connected", self._handle_connected)
        self.add_event_handler("disconnected", self._handle_disconnected)

    ## \fn _session_start(self, event)
    #  \brief Inizialitation stuff: Request roster
    #  \params[in] event: 
    def _session_start(self, event):
        print 'Session start\n'
        #print 'Getting shared roster\n'
        #1self.getRoster()
        self.thread = Thread(target=self._checking_mods)
        self.thread.start()

    def _checking_mods(self):
        print("Checking mods")
        result = False

        while not result:
            result = self.check_mods()
            if not result:
                time.sleep(3)

        if result:
            print('Sending presence')
            self.sendPresence()

        # For test purposes
        if self.nick == "prueba":
            time.sleep(1)
            self.send_stanza_to_agent()

        if self.nick == "test_result":
            time.sleep(1)
            self.send_stanza_result()
        ##################
        
    def _handle_connected(self, event):
        print 'Status: Connected\n'
        
    ## \fn _handle_disconnected(self, event)
    #  \brief Disconnected event handler
    #  \param event: event
    def _handle_disconnected(self, event):
        print 'Disconnecting ...\n'
        # We are not handling the disconnection event in the bot.
        pass
        
    ## \fn reconnect(self)
    #  \brief Overriding sleekxmpp reconnect method.
    def reconnect(self):
        sleekxmpp.XMLStream.disconnect(self)

