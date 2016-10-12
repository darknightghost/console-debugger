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

class Frame:
    def __init__(self, parent, rect):
        self.parent = parent
        self.rect = rect
        self.alive = True
        self.msg_dict = {}
        self.focused = False
        parent.add_child(self)
        self.children = []
        self.focused_child = None

    def close(self):
        self.parent.remove_child(self)
        self.alive = False
        
        return

    def resize(self, rect):
        self.rect = rect
        self.dispatch_msg(Message(Message.MSG_RESIZE, rect))
        self.dispatch_msg(Message(Message.MSG_REDRAW, None))
        return

    def input(self, key,  mouse):
        pass

    def draw(self, pos, string, attr):
        if pos.top in range(0, self.rect.size.height) \
                and pos.left in range(0, self.rect.size.width):
            s = string[: self.rect.size.width - pos.left]
            self.parent.draw(Pos(pos.top + self.rect.pos.top,
                pos.left + self.rect.pos.left), s, attr)

        return

    def update(self):
        self.parent.update()
        return

    def dispatch_msg(self, msg):
        try:
            self.msg_dict[msg.msg](msg)
        except KeyError:
            pass

        return

    def regist_msg_func(self, msg_type, func):
        self.msg_dict[msg_type] = func
        return

    def set_focus(self, stat):
        self.focused = stat
        if stat:
            self.dispatch_msg(Message(Message.MSG_GETFOCUS, None))
        else:
            self.dispatch_msg(Message(Message.MSG_LOSTFOCUS, None))
        return

    def add_child(self, child):
        self.children.append(child)
        if self.focused_child == None:
            self.focused_child = child

    def remove_child(self, child):
        self.children.remove(child)
        if self.focused_child == child:
            self.focused_child = None
        return

    def redraw(self):
        self.dispatch_msg(Message(Message.MSG_REDRAW, None))
        for w in self.children:
            w.dispatch_msg(Message(Message.MSG_REDRAW, None))

