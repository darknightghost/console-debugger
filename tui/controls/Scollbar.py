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
from tui import *

class Scollbar(Control):
    def __init__(self, text, parent, rect):
        rect.size.width = 1
        Control(self, text, parent, rect)
        self.max_value = 0
        self.value = 0

    '''
        Getters and setters.
    '''
    def get_max_value(self):
        '''
            scollbar.get_max_value() -> float

            Get the max value of the scollbar.
        '''
        return self.max_value

    def set_max_value(self, val):
        '''
            scollbar.set_max_value(value)

            Set the max value of scollbar.
        '''
        value_changed = False

        if self.max_value != val:
            value_changed = True

        self.max_value = val

        if val < self.value:
            self.value = val

        if value_changed:
            self.redraw()
            self.update()

    def get_value(self):
        '''
            scollbar.get_value() -> float

            Get the value of scollbar.
        '''
        return self.value

    def set_value(self, val):
        '''
            scollbar.set_value(val)

            Set the value of scollbar.
        '''
        value_changed = False

        if val > self.max_value:
            val = self.max_value

        if self.value != val:
            value_changed = True

        self.value = val

        if value_changed:
            self.parent.dispatch_msg(Message(Message.MSG_CHANGED, self))
            self.redraw()
            self.update()

    '''
        Message handlers.
    '''
    def init_control(self):
        self.regist_msg_func(Message.MSG_REDRAW, self.on_draw)
        self.regist_msg_func(Message.MSG_LCLICK, self.on_lclick)
        self.regist_msg_func(Message.MSG_DRAG, self.on_drag)
        self.regist_msg_func(Message.MSG_RESIZE, self.on_resize)

    def on_draw(self, msg):
        color = Color.get_color(Color.WHITE, Color.BLACK) | curses.A_BOLD
        block_top = round(self.value * (self.rect.size.height - 3) / self.max_value) + 1

        self.draw(Pos(0, 0), "▲", color)
        self.draw(Pos(self.rect.size.height - 1, 0), "▼", color)

        for top in range(1, self.rect.size.height - 1):
            if block_top == top:
                self.draw(Pos(top, 0), ' ', color | curses.A_REVERSE)
                    
            else:
                self.draw(Pos(top, 0), '|', color)

    def on_lclick(self, msg):
        top = msg.data.top

        if top == 0:
            #Scoll up
            self.value += 1
            self.redraw()
            self.update()

        elif top == self.rect.size.height - 1:
            #Scoll down
            self.value -= 1
            self.redraw()
            self.update()

        else:
            new_val = (top - 1) / (self.value.height - 3)
            self.set_value(new_val)

        return True

    def on_drag(self, msg):
        begin_top = msg.data[0].top
        if begin_top < 1 or begin_top > self.rect.size.height - 2:
            return False

        top = msg.data[1].top
        if top < 1:
            top = 1

        elif top > self.rect.size.height - 2:
            top = self.rect.size.height - 2

        new_val = (top - 1) / (self.value.height - 3)
        self.set_value(new_val)
        return True

    def on_resize(self, msg):
        if self.rect.size.width != 1:
            self.rect.size.width = 1
            self.resize(self.rect)
