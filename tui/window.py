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
import log

class Window(Frame):
    def __init__(self, text, parent, rect):
        self.text = text
        self.visible = False
        self.vscoll_off = 0
        self.hscoll_off = 0

        Frame.__init__(self, parent, rect)

        self.init_window()

        self.dispatch_msg(Message(Message.MSG_CREATE, None))
        if self.visible:
            self.redraw()
            self.update()

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
        Frame.set_focus(self, stat)

    def redraw(self):
        if self.visible:
            drawer = Drawer(self)
            drawer.rectangle(Rect(Pos(0, 0), Size(self.rect.size.width, self.rect.size.height)), 
                    ' ', Color.get_color(Color.WHITE, Color.BLACK))
            self.draw(Pos(0, 0), self.text, Color.get_color(Color.WHITE, Color.RED))
            Frame.redraw(self)

    def update(self):
        if self.visible:
            Frame.update(self)

    def draw(self, pos, string, attr):
        Frame.draw(self, Pos(pos.top - self.hscoll_off, pos.left - self.vscoll_off),
                string, attr)
