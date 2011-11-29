#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sleekxmpp.xmlstream.stanzabase import ET
from sleekxmpp.basexmpp import *
    
# Class to manage a custom iq    
class IqCustomMessage:
    def __init__(self):
        pass

    # To create an IQ of type "result"
    def create_result_iq(self, parent, data, id_stanza):
        # Create a custom IQ result
        print data
        iq = parent.makeIqResult(id_stanza)

        # Set IQ "action" attribute
        iq.attrib['action'] = data['stanza'] + ":" + data['type']

        # If exist a code, there are an error
        #if data["code"] or data["msg"] != "ok":
        if data["code"]:
            obj_error = ET.Element('error')
            obj_error.attrib['code'] = data["code"]
            if data["msg"]:
                obj_error.text = data["msg"]
            iq.append(obj_error)

        # Return user data for query
        # Maybe should return an stanza with user element to englobe the users data (<user><item>...</item></user>)
        if data['type'] == 'read' and data['stanza'] == 'user' and not data['code']:
            for item in data["items"]:
                # Field uid
                obj_uid = ET.Element('uid')
                obj_uid.text = item['uid']
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
                obj_item = ET.Element('item')
                obj_item.append(obj_uid)
                obj_item.append(obj_gecos)
                obj_item.append(obj_quota)
                obj_item.append(obj_course)
                obj_item.append(obj_group)
                obj_item.append(obj_profile)
                iq.append(obj_item)

            # This means that the searching don't return any results
            obj_response = ET.Element('response')
            obj_response.text = "read"
            iq.append(obj_response)

        # Return IQ formatted
        return iq

    # To send and IQ
    def send_custom_iq(self, from_jid, to_jid, iq):
        iq.attrib['from'] = to_jid
        iq.attrib['to'] = from_jid
        iq.send()