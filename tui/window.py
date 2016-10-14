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
from tui.frame import *

class Window(Frame):
    def __init__(self, title, parent, rect):
        Frame.__init__(self, parent, rect)
        self.title = title
        self.visible = False

        self.init_window()

        self.dispatch_msg(Message(Message.MSG_CREATE, None))

    def init_window(self):
        pass

    def show(self):
        self.visible = True
        self.dispatch_msg(Message(Message.MSG_SHOW,
            None))
        self.redraw()
        self.update()
        return

    def hide(self):
        self.visible = False
        self.dispatch_msg(Message(Message.MSG_HIDE,
            None))
        return

    def set_focus(self, stat):
        if stat:
            if self.parent.focused_child != self:
                self.parent.focused_child.set_focus(False)
                self.parent.focused_child = self

        Frame.set_focus(self, stat)

        if self.focused_child != None:
            self.focused_child.set_focus(stat)


