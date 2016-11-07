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
            cls.initialized = False

        return cls._instance
    
    def __init__(self, workspace, adapter, global_cfg):
        if type(self).initialized:
            return

        else:
            type(self).initialized = True

        #Initialize the plugin
        self.cfg = global_cfg
        self.adapter = adapter
        self.workspace = workspace
        self.name = type(self).__module__.split('.')[-2]
        log.debug_log("Plugin \"%s\" loaded."%(self.name))
        self.__on_plugin_init()

    '''
        Called by other classes.
    '''
    def open(self, cfg, view, argv):
        if type(self).openable():
            return self.__on_open(cfg, view, argv)

        else:
            return False

    def configure(self, cfg, view):
        if type(self).configureable():
            return self.__on_configure(cfg, view)

        else:
            return False

    def openable():
        '''
            Plugin.openable() -> bool

            Should be implemented by user.

            If the plugin can be opened, returns True. Otherwise returns False.
        '''
        raise NotImplementedError()

    def configureable():
        '''
            Plugin.configureable(() -> bool

            Should be implemented by user.

            If the plugin can be configured, returns True. Otherwise returns False.
        '''
        raise NotImplementedError()

    def complete_open(self, compstr):
        '''
            plugin.complete_open(compstr) -> list

            Should be implemented by user.

            Complete the open command.
        '''
        raise NotImplementedError()

    '''
        Called by itself.
    '''
    def __on_plugin_init(self):
        '''
            Should be implemented by user.

            The function will be called when the plugin is initialized.
        '''
        raise NotImplementedError()

    def __on_open(self, cfg, view, argv):
        '''
            Should be implemented by user.

            The function will be called when the plugin is initialized.

            Return True if succeed. Return False if failed.
        '''
        raise NotImplementedError()

    def __on_configure(self, cfg, view):
        '''
            Should be implemented by user.

            The function will be called when the plugin is initialized.

            Return True if succeed. Return False if failed.
        '''
        raise NotImplementedError()

