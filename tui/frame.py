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

        if not (msg.is_broadcast() or msg.is_user_msg()):
            try:
                hndlr = self.msg_dict[msg.msg]

            except KeyError:
                pass

            else:
                hndlr(msg)

            return

        if msg.is_mouse_msg():
            return self.dispatch_mouse_msg(msg)

        else:
            if self.focused_child != None:
                ret = self.focused_child.dispatch_msg(msg)

                if ret:
                    return True
            try:
                hndlr =  self.msg_dict[msg.msg]

            except KeyError:
                return False
            
            else:
                return hndlr(msg)

    def dispatch_mouse_msg(self, msg):
        if msg.is_mouse_begin_msg():
            for c in self.children:
                if msg.msg == Message.MSG_DRAG:
                    if msg.data[0] in c.rect:
                        if not c.focused:
                            self.focused_child = c
                            c.set_focus(True)

                        if not c.dispatch_msg(Message(msg.msg,(
                            Pos(msg.data[0].top - c.rect.pos.top,
                                msg.data[0].left - c.rect.pos.left),
                            Pos(msg.data[1].top - c.rect.pos.top,
                                msg.data[1].left - c.rect.pos.left)))):
                            break

                        else:
                            return True

                else:
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
                hndlr = self.msg_dict[msg.msg]

            except KeyError:
                return False

            else:
                return hndlr(msg)

        else:
            ret = None

            if msg.msg == Message.MSG_DRAG:
                ret = self.focused_child.dispatch_msg(Message(msg.msg,
                    (Pos(msg.data[0].top - self.focused_child.rect.pos.top,
                        msg.data[0].left - self.focused_child.rect.pos.left),
                    Pos(msg.data[1].top - self.focused_child.rect.pos.top,
                        msg.data[1].left - self.focused_child.rect.pos.left)
                    )))

            else:
                ret = self.focused_child.dispatch_msg(Message(msg.msg,
                    Pos(msg.data.top - self.focused_child.rect.pos.top,
                        msg.data.left - self.focused_child.rect.pos.left)))

            if not ret:
                try:
                    hndlr = self.msg_dict[msg.msg](msg)

                except KeyError:
                    return False

                else:
                    return hndlr(msg)

            else:
                return ret

    def regist_msg_func(self, msg_type, func):
        self.msg_dict[msg_type] = func
        return

    def set_focus(self, stat):
        if stat == True and isinstance(self.parent, Frame):
            #Auto switch focused window
            if self != self.parent.focused_child:
                self.parent.focused_child = self

            if not self.parent.focused:
                self.parent.set_focus(True)

        #Send message
        if stat and not self.focused:
            self.focused = stat
            self.dispatch_msg(Message(Message.MSG_GETFOCUS, None))

        elif not stat and self.focused:
            self.focused = stat
            self.dispatch_msg(Message(Message.MSG_LOSTFOCUS, None))

        if self.focused_child != None:
            if self.focused_child.focused != stat:
                self.focused_child.set_focus(stat)

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

    def print_stat(self, info):
        self.parent.print_stat(info)

    def msg_inject(self, msg, target = None):
        if target == None:
            target = self

        return self.parent.msg_inject(msg, target)

    def popup(self, lst, pos):
        '''
            Must be called in message handlers.
        '''
        return self.parent.popup(lst, Pos(self.rect.pos.top + pos.top,
            self.rect.pos.left + pos.left))

    def show_text(self, txt):
        self.parent.show_text(txt)
