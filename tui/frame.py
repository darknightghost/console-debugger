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
import log

class Frame:
    def __init__(self, parent, rect):
        self.parent = parent
        self.rect = rect
        self.alive = True
        self.msg_dict = {}
        self.focused = False
        self.children = []
        self.focused_child = None

        parent.add_child(self)

    def close(self):
        for c in self.children:
            c.close()

        self.parent.remove_child(self)
        self.dispatch_msg(Message(Message.MSG_CLOSE, None))
        self.alive = False
        
        return

    def resize(self, rect):
        self.rect = rect
        self.dispatch_msg(Message(Message.MSG_RESIZE, rect))
        self.redraw()
        return

    def draw(self, pos, string, attr):
        if not self.alive:
            return

        if pos.top in range(0, self.rect.size.height) \
                and pos.left in range(0, self.rect.size.width):
            s = string[: self.rect.size.width - pos.left]
            self.parent.draw(Pos(pos.top + self.rect.pos.top,
                pos.left + self.rect.pos.left), s, attr)

        return

    def update(self):
        if not self.alive:
            return

        self.parent.update()
        return

    def dispatch_msg(self, msg):
        if not self.alive:
            return False

        if msg.is_broadcast() or msg.is_user_msg():
            try:
                self.msg_dict[msg.msg](msg)
            except KeyError:
                pass
            return

        if msg.is_mouse_msg():
            return self.dispatch_mouse_msg(msg)

        else:
            if self.focused_child != None:
                ret = self.focused_child.dispatch_msg(msg)
                if ret:
                    return True
            try:
                return self.msg_dict[msg.msg](msg)
            except KeyError:
                return False

    def dispatch_mouse_msg(self, msg):
        if msg.is_mouse_begin_msg():
            for c in self.children:
                if msg.data in c.rect:
                    if not c.focused:
                        self.focused_child = c
                        c.set_focus(True)
                    if not c.dispatch_msg(Message(msg.msg,
                        Pos(msg.data.top - c.rect.pos.top,
                            msg.data.left - c.rect.pos.left))):
                        break

                    else:
                        return True

            try:
                return self.msg_dict[msg.msg](msg)
            except KeyError:
                return False

        else:
            if not self.focused_child.dispatch_msg(Message(msg.msg,
                Pos(msg.data.top - self.focused_child.rect.pos.top,
                    msg.data.left - self.focused_child.rect.pos.left))):
                try:
                    return self.msg_dict[msg.msg](msg)
                except KeyError:
                    return False

    def regist_msg_func(self, msg_type, func):
        self.msg_dict[msg_type] = func
        return

    def set_focus(self, stat):
        if stat and not self.focused:
            self.focused = stat
            self.dispatch_msg(Message(Message.MSG_GETFOCUS, None))
        elif not stat and self.focused:
            self.focused = stat
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

    def print_stat(self, info):
        self.parent.print_stat(info)

    def msg_inject(self, msg, target = None):
        if target == None:
            target = self

        return self.parent.msg_inject(msg, target)
