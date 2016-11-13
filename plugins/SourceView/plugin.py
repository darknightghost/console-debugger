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
import tui
import log
import os

from plugins.SourceView.SourceWnd import *

class Plugin(base_module.Plugin):
    def __on_plugin_init(self):
        pass

    def __on_open(self, cfg, view, argv):
        try:
            path = argv[1]
            filename = os.path.split(path)[1]

        except IndexError:
            path = None
            filename = "SourceView"

        wnd = SourceWnd(filename, view, Rect(Pos(1, 1),
                view.client_size),
                cfg,
                self, 
                path)

        return False

    def __on_configure(self, cfg, view):
        return False

    def openable(*args, **kwargs):
        return True

    def configureable(*args, **kwargs):
        return True

    def complete_open(self, compstr):
        #Get path to complete
        cmd = tui.Command(compstr)

        if len(cmd) != 3:
            return []

        compstr = tui.Command.get_last_str(compstr)

        #Complete path
        comppath = ""
        compname = ""
        if compstr[-1] == os.path.sep:
            comppath = compstr

        else:
            comppath = compstr[: compstr.rfind(os.path.sep) + 1]
            compname = compstr[compstr.rfind(os.path.sep) + 1 :]

        try:
            dir_list = os.listdir(comppath)

        except Exception:
            return []
        ret = []
        for n in dir_list:
            if n[: len(compname)] == compname:
                ret.append(comppath + n)

        return ret
