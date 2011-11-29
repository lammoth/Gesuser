#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from gesuser.mods.ldap_settings import *
from gesuser.datahandlers.couchdb.handler_couchdb import *

class MOD_System(object):
    def __init__(self):
        self.name = "MOD_SYSTEM"
        self.datahandle = None

        # Connect with datahandler (Default: CouchDB)
        self.datahandle = ConnectToCouch(server="winterfall.local")
        self.datahandle.connect(TABLE_NAME)
        list = self.groups_graphic()
        print list

    def isActive(self):
        return True

    def get_disk_space(self, dir=None, data_type=None):
        # Data types availables: b, mb, gb

        if dir:
            s = os.statvfs(dir)
        else:
             s = os.statvfs("/")
    
        if data_type:
            if data_type == "b":
                space_bytes = (s.f_bavail * s.f_frsize) / 1024
            elif data_type == "mb":
                space_bytes = (s.f_bavail * s.f_frsize) / (1024**2)
            elif data_type == "gb":
                space_bytes = (s.f_bavail * s.f_frsize) / (1024**3)
        else:
            space_bytes = (s.f_bavail * s.f_frsize) / 1024

        return space_bytes

    def users_stadistics(self):
        pass

    def groups_stadistics(self):
        complete_list = self.datahandle.readDocument()
        list_groups = []
        main_list = []
        for dict in complete_list:
            group_data = dict["group"]
            try:
                list_groups.index(group_data)
            except:
                list_groups.append(group_data)
                list_years = []
                for entry in complete_list:
                    if entry['group'] == group_data:
                        year_data = (entry["date"].split("-"))[0]
                        try:
                            list_years.index(year_data)
                        except:
                            list_years.append(year_data)
                            list_months = []
                            for e in complete_list:
                                if e['group'] == group_data:
                                    if (e['date'].split("-"))[0] == year_data:
                                        month_data = (e["date"].split("-"))[1]
                                        try:
                                            main_dict = {}
                                            list_months.index(month_data)
                                            main_dict["group"] = group_data
                                            main_dict["year"] = year_data
                                            main_dict["month"] = month_data
                                            main_list.append(main_dict)
                                        except:
                                            main_dict = {}
                                            list_months.append(month_data)
                                            main_dict["group"] = group_data
                                            main_dict["year"] = year_data
                                            main_dict["month"] = month_data
                                            main_list.append(main_dict)
        return main_list

    def groups_graphic(self, groups=None, year=None):
        if not groups:
            groups = ["10000", "10001"]
        if not year:
            year = "2011"
        list = self.groups_stadistics()
        main_list = []
        for g in groups:
            dict = {}
            list_months = []
            list_dict_months = []
            for l in list:
                if l['group'] == g:
                    if l['year'] == year:
                        d_month = {}
                        try:
                            list_months.index(l['month'])
                            for dm in list_dict_months:
                                if dm['month'] == l['month']:
                                    dm['quantity'] = dm['quantity'] + 1
                        except:
                            list_months.append(l['month'])
                            d_month['month'] = l['month']
                            d_month['quantity'] = 1
                            list_dict_months.append(d_month)
            dict['group'] = g
            dict['year'] = year
            dict['months'] = list_dict_months
            main_list.append(dict)
        return main_list
        
        
    def profile_stadistics(self):
        pass

if __name__=="__main__":
    l = MOD_System()