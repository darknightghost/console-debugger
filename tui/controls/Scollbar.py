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
from tui.controls.Control import *

class Scollbar(Control):
    def __init__(self, text, parent, rect):
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
            self.redraw()
            self.update()

    '''
        Message handlers.
    '''
    def init_control(self):
        pass

