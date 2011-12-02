#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ldap
import ldap.modlist as modlist
from datetime import date
import hashlib
import unicodedata
from base64 import b64encode
from operator import itemgetter

from gesuser.mods.ldap_settings import *
from gesuser.datahandlers.couchdb.handler_couchdb import *

class MOD_ldap(object):
    def __init__(self):
        self.name = "MOD_LDAP"
        self.server = None
        self.port = None
        self.server_uri = "ldap://"
        self.dn = None
        self.passwd = None
        self.connection = None
        self.datahandle = None
        #self.count = 0

        # Connect tool to LDAP
        self.connect(LDAP_SERVER)

        # Connect with datahandler (Default: CouchDB)
        self.datahandle = ConnectToCouch(server="winterfall.local")
        self.datahandle.connect(TABLE_NAME)

    def isActive(self):
        result = self.stablish_connection()
        return result
    
    def connect(self, server, port=None):
        self.server = server
        if port:
            self.port = port
            self.server_uri = self.server_uri + server + ":" + port
        else:
            self.server_uri = self.server_uri + server
        self.connection = ldap.initialize(self.server_uri)

    def stablish_connection(self):
        try:
            self.connection.simple_bind_s()
            return True
        except ldap.LDAPError, e:
            print e
            return False

    def create_user(self, data):
        print 'Create user'
        #self.count = self.count + 1
        # Bind/authenticate with a user with apropriate rights to add objects
        #if self.count < 2:
        #    self.connection.simple_bind_s("cn=admin,dc=winterfall,dc=local","gepet0")
        self.connection.simple_bind_s("cn=admin,dc=winterfall,dc=local","gepet0")

        # The dn of our new entry/object
        dn="uid=%s,ou=People,dc=winterfall,dc=local" % data['user']['uid']

        # A dict to help build the "body" of the object
        attrs = {}

        # Field for assign objectClass to Ldap entry
        # Following fields are required:
        # Field: objectClass
        # Field: uid ================> uid
        # Field: sn =================> uid
        # Field: gecos ==============> gecos
        # Field: cn =================> gecos
        # Field: uidNumber
        # Field: gidNumber ==========> group
        # Field: roomNumber =========> course
        # Field: loginShell
        # Field: userPassword  ======> pwd
        # Field: shadowMax
        # Field: shadowWarning
        # Field: homeDirectory ======> profile
        # Field: homePostalAddress ==> quota

        attrs['objectClass'] = OBJECTCLASS_LIST

        attrs['uid'] = data['user']['uid']
        attrs['sn'] = data['user']['uid']
        gecos_unicode = unicodedata.normalize('NFKD', unicode(data['user']['gecos']))
        gecos_ascii = gecos_unicode.encode('ASCII', 'ignore')
        #print gecos_ascii
        attrs['gecos'] = gecos_ascii
        #print type(attrs['gecos'])
        attrs['cn'] = data['user']['gecos'].encode('utf-8')
        #print attrs['cn']
        #print type(attrs['cn'])

        # Field for assign user uidNumber
        next_uidnumber = self._check_uidnumber_presence()
        attrs['uidNumber'] = str(next_uidnumber + 1)

        # Field for group type
        # Default value for group
        attrs['gidNumber'] = data['user']['group']
        if data['user']['group'] == PROFILE_TYPE_TEACHER:
            attrs['gidNumber'] = TEACHER_PROFILE_NUMBER
        elif data['user']['group'] == PROFILE_TYPE_PUPIL:
            attrs['gidNumber'] = PUPIL_PROFILE_NUMBER
        elif data['user']['group'] == PROFILE_TYPE_MANAGEMENT:
            attrs['gidNumber'] = MANAGEMENT_PROFILE_NUMBER

        # Field for course
        #course_unicode = unicodedata.normalize('NFKD', unicode(data['user']['course']))
        course_utf = data['user']['course'].encode('utf-8')
        attrs['roomNumber'] = course_utf

        # Field for assign login shell
        attrs['loginShell'] = SHELL

        # Fields related with user password
        #password_sha = hashlib.sha1(data['user']['pwd']).digest()
        #password = "{SHA}" + b64encode(password_sha)0
        attrs['userPassword'] = data['user']['pwd']
        attrs['shadowMax'] = SHADOW_MAX
        attrs['shadowWarning'] = SHADOW_WARNING

        # Field for profile type (fixed or mobile)
        # Default value for profile
        attrs['homeDirectory'] = HOME_DIR % data['user']['uid']
        if data['user']['profile'] == PROFILE_TYPE_FIXED:
            attrs['homeDirectory'] = HOME_DIR % data['user']['uid']
        elif data['user']['profile'] == PROFILE_TYPE_MOBILE:
            attrs['homeDirectory'] = HOME_DIR_MOBILE % data['user']['uid']

        # Field for quotas
        attrs['homePostalAddress'] = data['user']['quota']

        # Convert our dict to nice syntax for the add-function using modlist-module
        ldif = modlist.addModlist(attrs)

        # Do the actual synchronous add-operation to the ldapserver
        try:
            self.connection.add_s(dn,ldif)
            print "casca ..."
            # Write with datahanlder (CouchDB by default)
            user_data_dict = {'_id':data['user']['uid'],'group':attrs['gidNumber'],'date':str(date.today())}
            self.datahandle.createDocument(user_data_dict)
            #self.connection.unbind_s()
            return {'error':'', 'desc':'ok', 'data':''}
        except Exception as e:
            #self.connection.unbind_s()
            error_dict = {}
            error_dict['error'] = "501"
            #error_dict['desc'] = e[0]['desc']
            error_dict['desc'] = ""
            error_dict['data'] = ""
            print e
            return error_dict

        # Its nice to the server to disconnect and free resources when done
        #self.connection.unbind_s()
    
    def read_user(self, data):
        print 'Read user'
        searchFilter = ""
        rs = []
        search_result = []
        ldap_result_id = None
        order_by = None

        fields_dict = self._extract_field_operator(data['user'])
        
        for f in FIELDS_LIST:
            print f
            try:
                sf = None
                op = fields_dict[f]
                print op
                if op == "gt":
                    operator = ">"
                elif op == "lt":
                    operator = "<"
                elif op == "eq":
                    operator = "="
                elif op == "ge":
                    operator = ">="
                elif op == "le":
                    operator = "<="
                elif op == "ap":
                    operator = "~="

                if f == "group":
                    if data['user']['group'] == PROFILE_TYPE_PUPIL:
                        data['user']['group'] = PUPIL_PROFILE_NUMBER
                    elif data['user']['group'] == PROFILE_TYPE_MANAGEMENT:
                        data['user']['group'] = MANAGEMENT_PROFILE_NUMBER
                    elif data['user']['group'] == PROFILE_TYPE_TEACHER:
                        data['user']['group'] = TEACHER_PROFILE_NUMBER

                # searchFilter Example: "(&(uid=*i*)(&(homePostalAddress=250)))"
                # searchFilter Example: "(&(!(homeDirectory~=nfs)))"
                
                if f == "uid" or f == "gecos":
                    if data['user'][f] == "*":
                        sf = "(%s%s%s)" % (FIELDS_DICT[f],operator,data['user'][f])
                    else:
                        sf = "(%s%s%s%s%s)" % (FIELDS_DICT[f],operator,"*",data['user'][f],"*")
                else:
                    if f == "group":
                        sf = "(%s%s%s)" % (FIELDS_DICT[f],operator,data['user'][f])

                if f == "order":
                    print "ordenado por: " + data['user']['order']
                    order_by = data['user']['order']

                searchFilter = searchFilter + sf
                print searchFilter
            except:
                print f + " Exclude"

        if searchFilter:
            searchFilter = "(&" + searchFilter + ")"

        print searchFilter

        # The next lines will also need to be changed to support your search requirements and directory
        baseDN = "ou=People, dc=winterfall, dc=local"
        searchScope = ldap.SCOPE_SUBTREE
        # Retrieve all attributes
        retrieveAttributes = None
        users = []

        try:
            # Bind/authenticate with a user with apropriate rights to add objects
            self.connection.simple_bind_s("cn=admin,dc=winterfall,dc=local","gepet0")
            ldap_result_id = self.connection.search(baseDN, searchScope, searchFilter, retrieveAttributes)
            result_set = []
            while 1:
                result_type, result_data = self.connection.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
            #print result_set
            for result in result_set:
                dict = {'uid':result[0][1]['uid'][0],
                        'group':self.translate_data_friendly(result[0][1]['gidNumber'][0],'group'),
                        #'gecos':result[0][1]['gecos'][0],
                        'gecos':result[0][1]['cn'][0],
                        'course':result[0][1]['roomNumber'][0],
                        'profile':self.translate_data_friendly(result[0][1]['homeDirectory'][0],'profile'),
                        'quota':result[0][1]['homePostalAddress'][0]
                        }
                users.append(dict)

            if not order_by:
                order_by = "uid"
            rs = self._apply_search_filter(data, users, fields_dict)
            search_result = self.order_by(order_by, rs)
            #print "*"*80
            #print search_result
            #print "*"*80
            return {'error':'', 'desc':'ok', 'data':search_result}
        except Exception as e:
            error_dict = {}
            error_dict['error'] = "501"
            error_dict['desc'] = e[0]['desc']
            error_dict['data'] = ""
            return error_dict

    def translate_data_friendly(self, data, type):
        if type == "group":
            if data == PUPIL_PROFILE_NUMBER:
                result = "A"
            elif data == TEACHER_PROFILE_NUMBER:
                result = "P"
            else:
                result = "G"
        elif type == "profile":
            if data.find("nfs") > 0:
                result = "M&oacute;vil"
            else:
                result = "Fijo"
        return result

    def order_by(self, field, data):
#        data_dict = []
#        result_list = []
#        for d in data:
#            if field == "quota" or field == "course":
#                data_dict.append(int(d[field]))
#            else:
#                data_dict.append(d[field])
#        data_dict.sort()
#        print data_dict
#        for o in data_dict:
#            for obj in data:
#                if field == "quota" or field == "course":
#                    if obj[field] == str(o):
#                        result_list.append(obj)
#                else:
#                    if obj[field] == o:
#                        result_list.append(obj)
#        return result_list
        #for d in data:
        #    d['quota'] = int(d['quota'])
        #result = sorted(data, key=itemgetter(field))
        #if field == "quota" or field == "course":
        if field == "quota":
            result = sorted(data, key=lambda k: int(k[field]))
        else:
            result = sorted(data, key=lambda k: k[field].lower())
        return result

    def update_user(self, data):
        print 'Update user test'
        # Bind/authenticate with a user with apropriate rights to add objects
        self.connection.simple_bind_s("cn=admin,dc=winterfall,dc=local","gepet0")
        
        user_dict = self._data_philter(data)
        # Form example: data = ['lammoth',{fields_to_change}]
        data = [user_dict['uid'], user_dict]
        user_dn = 'uid=%s,ou=People,dc=winterfall,dc=local' % data[0]
        fields = []
        # Check fields to change
        # To change gecos field
        try:
            gecos_unicode = unicodedata.normalize('NFKD', unicode(data[1]['gecos']))
            gecos_ascii = gecos_unicode.encode('ASCII', 'ignore')
            list_gecos = ['gecos',gecos_ascii]
            fields.append(list_gecos)
            list_cn = ['cn',data[1]['gecos'].encode('utf-8')]
            fields.append(list_cn)
        except:
            print("Error while changing gecos")

        # To change password field
        try:
            #password_sha = hashlib.sha1(data[1]['pwd']).digest()
            #password = "{SHA}" + b64encode(password_sha)
            list_password = ['userPassword',data[1]['pwd']]
            fields.append(list_password)
        except:
            print("Error while changing password")

        # To change quota field
        try:
            list_quota = ['homePostalAddress',data[1]['quota']]
            fields.append(list_quota)
        except:
            print("Error while changing quota")

        # To change course field
        try:
            list_course = ['roomNumber',data[1]['course'].encode('utf-8')]
            fields.append(list_course)
        except:
            print("Error while changing course")

        # To change profile field
        try:
            if data[1]['profile'] == PROFILE_TYPE_FIXED:
                data[1]['profile'] = HOME_DIR % data[1]['uid']
            elif data[1]['profile'] == PROFILE_TYPE_MOBILE:
                data[1]['profile'] = HOME_DIR_MOBILE % data[1]['uid']

            list_profile = ['homeDirectory',data[1]['profile']]
            fields.append(list_profile)
        except:
            print("Error while changing profile")

        # To change group field
        try:
            if data[1]['group'] == PROFILE_TYPE_PUPIL:
                data[1]['group'] = PUPIL_PROFILE_NUMBER
            elif data[1]['group'] == PROFILE_TYPE_MANAGEMENT:
                data[1]['group'] = MANAGEMENT_PROFILE_NUMBER
            elif data[1]['group'] == PROFILE_TYPE_TEACHER:
                data[1]['group'] = TEACHER_PROFILE_NUMBER
                
            list_group = ['gidNumber',data[1]['group']]
            fields.append(list_group)
        except:
            print("Error while changing group")

        # Through this loop, creates a list with the fields to change
        mod_attrs = []
        for f in fields:
            t = (ldap.MOD_REPLACE,f[0],f[1])
            mod_attrs.append(t)
        
        try:
            self.connection.modify_s(user_dn, mod_attrs)
            return {'error':'', 'desc':'ok', 'data':''}
        except Exception as e:
            error_dict = {}
            error_dict['error'] = "501"
            #error_dict['desc'] = e[0]['desc']
            print e
            error_dict['desc'] = ""
            error_dict['data'] = ""
            return error_dict

    def delete_user(self, uid):
        print 'Delete user test'
        try:
            del_result = self.connection.delete('uid=%s,ou=People,dc=winterfall,dc=local' % uid)
            self.connection.result(del_result)
            return {'error':'', 'desc':'ok', 'data':''}
        except Exception as e:
            error_dict = {}
            error_dict['error'] = "501"
            error_dict['desc'] = e[0]['desc']
            error_dict['data'] = ""
            return error_dict

    # Used to extract the operator of field (used in read method)
    def _extract_field_operator(self, data):
        fields_dict = {}
        for field in FIELDS_LIST:
            try:
                element = data.findall('{%s}%s' % ("cga:gesuser3:user", field))
                fields_dict[field] = element[0].attrib['op']
            except:
                pass
        return fields_dict
        
    def _check_uidnumber_presence(self):
        print 'Check uidNumber field'
        baseDN = "ou=People, dc=winterfall, dc=local"
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = ['uidNumber']
        searchFilter = "uid=*"

        try:
            ldap_result_id = self.connection.search(baseDN, searchScope, searchFilter, retrieveAttributes)
            result_set = 0
            while 1:
                result_type, result_data = self.connection.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        if result_set < int(result_data[0][1]['uidNumber'][0]):
                            result_set = int(result_data[0][1]['uidNumber'][0])
            return result_set
        except ldap.LDAPError, e:
            print e

    def _data_philter(self, data):
        dict = {'uid':data['user']['uid'],
                'pwd':data['user']['pwd'],
                'gecos':data['user']['gecos'],
                'quota':data['user']['quota'],
                'course':data['user']['course'],
                'profile':data['user']['profile'],
                'group':data['user']['group'],
               }
        return dict

    def _apply_search_filter(self, data, search, operators):
        # Filter for fields: profile, quota and course
        list_profile = []
        list_quota = []
        list_course = []
        profile_exist = False
        quota_exist = False
        course_exist = False

        if data['user']['profile']:
            profile_exist = True
            if data['user']['profile'] == "2":
                for d in search:
                    try:
                        if d['profile'].index("vil"):
                            list_profile.append(d)
                    except:
                        pass
            else:
                for d in search:
                    try:
                        if d['profile'].index("jo"):
                            list_profile.append(d)
                    except:
                        pass

        if data['user']['quota']:
            quota_exist = True
            if profile_exist:
                if list_profile:
                    op = operators['quota']
                    for d in list_profile:
                        if self._compare_operator(op, int(data['user']['quota']), int(d['quota'])):
                            list_quota.append(d)
                else:
                    return []
            else:
                op = operators['quota']
                for d in search:
                    if self._compare_operator(op, int(data['user']['quota']), int(d['quota'])):
                        list_quota.append(d)


        if data['user']['course']:
            course_exist = True
            if quota_exist:
                if list_quota:
                    op = operators['course']
                    for d in list_quota:
                        #if self._compare_operator(op, int(data['user']['course']), int(d['course'])):
                        if self._compare_operator(op, data['user']['course'], d['course']):
                            list_course.append(d)
                else:
                    return []

            elif profile_exist:
                if list_profile:
                    op = operators['course']
                    for d in list_profile:
                        #if self._compare_operator(op, int(data['user']['course']), int(d['course'])):
                        if self._compare_operator(op, data['user']['course'], d['course']):
                            list_course.append(d)
                else:
                    return []
            else:
                op = operators['course']
                for d in search:
                    #if self._compare_operator(op, int(data['user']['course']), int(d['course'])):
                    if self._compare_operator(op, data['user']['course'], d['course']):
                        list_course.append(d)

        if profile_exist and quota_exist and course_exist:
            return list_course
        elif profile_exist and quota_exist:
            return list_quota
        elif profile_exist and course_exist:
            return list_course
        elif quota_exist and course_exist:
            return list_course
        elif profile_exist:
            return list_profile
        elif quota_exist:
            return list_quota
        elif course_exist:
            return list_course
        else:
            return search

    def _compare_operator(self, op, data_source, data_target):
        if op == "gt":
            if data_target > data_source:
                return True
        elif op == "lt":
            if data_target < data_source:
                return True
        elif op == "eq":
            if data_target == data_source:
                return True
        elif op == "ge":
            if data_target >= data_source:
                return True
        elif op == "le":
            if data_target <= data_source:
                return True
        else:
            return False
    
if __name__=="__main__":
    l = MOD_ldap()