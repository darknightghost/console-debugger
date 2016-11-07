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
import log
from tui import *
import sys

class Popup:
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
        wnd_size = self.workspace.stdscr.getmaxyx()
        self.wnd_width = wnd_size[1]
        self.wnd_height = wnd_size[0]

        if pos.top < self.wnd_height / 2:
            if pos.left < self.wnd_width / 2:
                self.left_above_pop(pos)

            else:
                self.right_above_pop(pos)

        else:
            if pos.left < self.wnd_width / 2:
                self.left_below_pop(pos)

            else:
                self.right_below_pop(pos)

        self.begin = 0

        #Draw menu
        self.curse = 0
        self.update()

        #Get selection
        curses.flushinp()

        while True:
            key, mouse = self.workspace.get_input()
            if key == Keyboard.KEY_ESC:
                return None

            elif key == Keyboard.KEY_LF:
                    break

            elif key == Keyboard.KEY_UP:
                if self.curse > 0:
                    self.curse -= 1

                if self.draw_pg_up and self.curse == 0:
                    self.curse += 1
                    self.begin -= 1

            elif key == Keyboard.KEY_DOWN:
                if self.curse < self.rect.size.height - 1:
                    self.curse += 1

                if self.draw_pg_down and self.curse == self.rect.size.height - 1:
                    self.curse -= 1
                    self.begin += 1

            elif key == Keyboard.KEY_MOUSE:
                if mouse[4] in (curses.BUTTON1_PRESSED, curses.BUTTON2_PRESSED, \
                    curses.BUTTON3_PRESSED):

                    click_pos = Pos(mouse[2], mouse[1])
                    if click_pos in self.rect:
                        clicked_line = click_pos.top - self.rect.pos.top

                        if clicked_line == 0 and self.draw_pg_up:
                            self.begin -= 1

                        elif clicked_line == self.rect.size.height - 1 \
                            and self.draw_pg_down:
                            self.begin += 1

                        else:
                            self.curse = clicked_line
                            break

                    else:
                        return None

            self.update()

        index = self.curse
        if self.draw_pg_up:
            index -= 1

        index += self.begin

        return index

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
        line_num = min(self.rect.size.height, len(self.lst) - self.begin)
        self.draw_pg_up = False
        if self.begin > 0:
            line_num = self.rect.size.height - 1
            self.draw_pg_up = True

        self.draw_pg_down = False
        if len(self.lst) - self.begin > line_num:
            line_num -= 1
            self.draw_pg_down = True

        l = 0
        normal_color = Color.get_color(Color.BLACK, Color.MAGENTA)
        drawer = Drawer(self.workspace)
        drawer.rectangle(self.rect, ' ', normal_color)
        if self.draw_pg_up:
            if l == self.curse:
                self.curse += 1

            color = normal_color

            self.workspace.draw(Pos(self.rect.pos.top + l,
                self.rect.pos.left + int(self.rect.size.width / 2)),
                    '↑',color )
            l += 1

        for i in range(0, line_num):
            if l == self.curse:
                color = normal_color | curses.A_REVERSE

            else:
                color = normal_color

            self.workspace.draw(Pos(self.rect.pos.top + l,
                self.rect.pos.left),
                    self.lst[i + self.begin],
                    color)
            l += 1

        if self.draw_pg_down:
            if l == self.curse:
                self.curse -= 1

            color = normal_color

            self.workspace.draw(Pos(self.rect.pos.top + l,
                self.rect.pos.left + int(self.rect.size.width / 2)),
                    '↓', color)


    def longgest_line_len(self):
        ret = 0
        for l in self.lst:
            if len(l) > ret:
                ret = len(l)

        return ret
