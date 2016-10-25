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


    '''
        Popup menu.
    '''
    def __init__(self, lst, workspace):
        self.lst = lst
        self.workspace = workspace

    def pop(self, pos):
        if len(self.lst) == 0:
            return None

        #Compute rect
        wnd_size = self.stdscr.getmaxyx()
        self.wnd_width = wnd_size[1]
        self.wnd_height = wnd_size[0]

        if pos.top < wnd_height / 2:
            if pos.left < wnd_width / 2:
                self.left_above_pop(pos)

            else:
                self.right_above_pop(pos)

        else:
            if pos.left < wnd_width / 2:
                self.left_below_pop(pos)

            else:
                self.right_below_pop(pos)

        self.begin = 0

        #Draw menu
        self.update()

        #Get input
        #Refresh menu

    def left_above_pop(self, pos):
        width = self.longgest_line_len()
        if width + pos.left > self.wnd_width:
            width = self.wnd_width - pos.left

        elif width < 2:
            width = 2

        height = len(self.lst)
        if height + pos.top > self.wnd_height:
            height = self.wnd_height - pos.top

        self.rect = Rect(pos, Size(width, height))

    def right_above_pop(self, pos):
        width = self.longgest_line_len()
        if width > pos.left:
            width = pos.left

        elif width < 2:
            width = 2

        height = len(self.lst)
        if height + pos.top > self.wnd_height:
            height = self.wnd_height - pos.top

        self.rect = Rect(Pos(pos.top, pos.left - width), 
                Size(width, height))

    def left_below_pop(self, pos):
        width = self.longgest_line_len()
        if width + pos.left > self.wnd_width:
            width = self.wnd_width - pos.left

        elif width < 2:
            width = 2

        height = len(self.lst)
        if height > pos.top:
            height = pos.top

        self.rect = Rect(Pos(pos.top - height, pos.left),
                Size(width, height))

    def right_below_pop(self, pos):
        width = self.longgest_line_len()
        if width > pos.left:
            width = pos.left

        elif width < 2:
            width = 2

        height = len(self.lst)
        if height > pos.top:
            height = pos.top

        self.rect = Rect(Pos(pos.top - height, pos.left - width),
                Size(width, height))

    def update(self):


    def longgest_line_len(self):
        ret = 0
        for l in self.lst:
            if len(l) > ret:
                ret = len(l)

        return ret
