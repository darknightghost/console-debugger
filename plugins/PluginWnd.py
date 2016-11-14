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

from tui import *
from tui.window import *

class PluginWnd(Window):
    def __init__(self, text, parent, rect, cfg, plugin):
        self.cfg = cfg
        self.wnd_cmd_dict = {}
        self.plugin = plugin
        Window.__init__(self, text, parent, rect)

    def reg_wnd_command(self, cmd, hndlr, autocompile):
        if cmd in self.wnd_cmd_dict:
            return False

        self.wnd_cmd_dict[cmd] = (hndlr, autocompile)

        return True

    def unreg_wnd_command(self, cmd):
        self.wnd_cmd_dict.pop(cmd)

    def enable_wnd_command(self):
        for c in self.wnd_cmd_dict:
            self.plugin.workspace.reg_command(c, self.wnd_cmd_dict[c][0],
                    self.wnd_cmd_dict[c][1])

    def disable_wnd_command(self):
        for c in self.wnd_cmd_dict:
            self.plugin.workspace.unreg_command(c)
