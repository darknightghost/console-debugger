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

import plugins.plugin as base_module

class Plugin(base_module.Plugin):
    def on_plugin_init(self):
        pass

    def on_open(self, cfg, view, argv):
        pass

    def on_configure(self, cfg, view):
        pass

    def openable(*args, **kwargs):
        return True

    def configureable(*args, **kwargs):
        return True
