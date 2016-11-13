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

import curses
from tui.window import *
from tui import *

class Control(Window):
    def __init__(self, text, parent, rect):
        self.visible = True
        Window.__init__(self, text, parent, rect)

    def init_window(self):
        self.init_control()

    def init_control(self):
        pass

    def dispatch_ctrl_msg(self, msg_type):
        return self.parent.dispatch_msg(Message(msg_type, self))
