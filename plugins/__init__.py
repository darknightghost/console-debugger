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
import log
import importlib

class PluginManager:
    def __new__(cls, *args, **kwargs):
        if "_instance" not in PluginManager.__dict__:
            PluginManager._instance = object.__new__(cls)

        return PluginManager._instance
    
    def __init__(self, adapter, cfg, workspace):
        self.adapter = adapter
        self.cfg = cfg
        self.workspace = workspace

        #Load plugins
        for k in self.cfg.keys:
            self.get_plugin(k)

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

    def get_plugin(self, name):
        '''
            PluginManager.get_plugin(self, name) -> Plugin

            Get a Plugin object.
        '''
        if name not in self.get_plugin_list():
            raise NameError("Unknow plugin \"%s\"."%(name))

        cls = importlib.import_module("plugins.%s.plugin"%(name)).Plugin

        return cls(self.workspace, self.adapter, self.get_cfg_node(name))

    def get_cfg_node(self, name):
        try:
            return self.cfg.get_key(name)

        except KeyError:
            return self.cfg.add_key(name)

    def complete_open(self, name, compstr):
        return []

    def reg_command(self, cmd, hndlr, autocomplete):
        self.workspace.reg_command(cmd, hndlr, autocomplete)

    def reg_shotcut_key(self, key, hndlr):
        self.workspace.reg_shotcut_key(key, hndlr)
