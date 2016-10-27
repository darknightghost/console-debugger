#! /usr/bin/python3
# -*- coding: utf-8 -*-

'''
      Copyright 2016,暗夜幽灵 <darknightghost.cn@gmail.com>

      This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    at your option) any later version.

      This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

      You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os

class PluginManager:
    def __init__(self, adapter, cfg):
        pass

    def dispatch_cmd(self, command):
        return "Unknow command."

    def dispatch_shotcut_key(self, key):
        pass

    def get_plugin_list(self):
        '''
            PluginManager.get_plugin_list(self) -> list

            Get a list of plugin names.
        '''
        plugin_dir = os.path.split(os.path.realpath(__file__))[0]
        ret = []
        files = os.listdir(plugin_dir)
        for t in files:
            if os.path.isdir(plugin_dir + "/" + t) and t != "__pycache__":
                ret.append(t)
        return ret

    def open_plugin(self, name, view, local_cfg):
        '''
            PluginManager.open_plugin(self, name, view, local_cfg) -> PluginWndFrame

            Open a plugin window.
        '''
        if name not in self.get_plugin_list():
            raise NameError("Unknow plugin \"%s\"."%(name))
