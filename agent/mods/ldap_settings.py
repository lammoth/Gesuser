#!/usr/bin/env python
# -*- coding: utf-8 -*-

LDAP_SERVER = "winterfall.local"

OBJECTCLASS_LIST = ['posixAccount','inetOrgPerson','organizationalPerson','person','top','shadowAccount']
PROFILE_TYPE_TEACHER = "3"
TEACHER_PROFILE_NUMBER = "10001"
PROFILE_TYPE_PUPIL = "1"
PUPIL_PROFILE_NUMBER = "10000"
PROFILE_TYPE_MANAGEMENT = "2"
MANAGEMENT_PROFILE_NUMBER = "10002"
PROFILE_TYPE_FIXED = "1"
PROFILE_TYPE_MOBILE = "2"
HOME_DIR = "/home/%s"
HOME_DIR_MOBILE = "/home/nfs/%s"
SHELL = "/bin/bash"
SHADOW_MAX = "99999"
SHADOW_WARNING = "7"

# Table name to save users data
TABLE_NAME = "users_data"

# List of fields availables for read operation
FIELDS_LIST = ['uid', 'gecos', 'group', 'quota', 'profile', 'course', 'order']
FIELDS_DICT = {'uid':'uid', 'gecos':'gecos', 'group':'gidNumber', 'quota':'homePostalAddress', 'profile':'homeDirectory', 'course':'roomNumber'}

