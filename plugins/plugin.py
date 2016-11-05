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

class Plugin:
    def __new__(cls, *args, **kwargs):
        if "_instance" not in cls.__dict__:
            cls._instance = object.__new__(cls)

        return cls._instance
    
    def __init__(self, workspace, adapter, global_cfg):
        #Initialize the plugin
        self.cfg = global_cfg
        self.adapter = adapter
        self.workspace = workspace
        self.name = os.path.split(os.path.dirname( \
                __import__(type(self).__module__).__file__))[-1]
        log.debug_log("Plugin \"%s\" loaded."%(self.name))
        self.on_plugin_init()

    def open(self, cfg, view, argv):
        if type(self).openable():
            self.on_open(cfg, view, argv)

    def configure(self, cfg, view):
        self.on_configure(view)
    
    def on_plugin_init(self):
        raise NotImplementedError()

    def on_open(self, cfg, view, argv):
        raise NotImplementedError()

    def on_configure(self, cfg, view):
        raise NotImplementedError()

    def openable():
        raise NotImplementedError()

    def configureable():
        raise NotImplementedError()
