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

from tui.frame import *
from tui import *

class TagsView(Frame):
    def __init__(self, parent, rect):
        Frame.__init__(self, parent, rect)
        self.top_docked = []
        self.bottom_docked = []
        self.left_docked = []
        self.right_docked = []

        self.client_size = Size(self.rect.size.width - 2,
                self.rect.size.height - 2)

        self.begin_tag = 0

        #Message handlers
        self.regist_msg_func(Message.MSG_REDRAW, self.on_draw)
        self.regist_msg_func(Message.MSG_RESIZE, self.on_resize)
        self.regist_msg_func(Message.MSG_GETFOCUS, self.on_get_focus)
        self.regist_msg_func(Message.MSG_LOSTFOCUS, self.on_lost_focus)

    def on_draw(self, msg):
        self.draw_borders()
        for i in range(1, self.rect.size.height - 2):
            self.draw(Pos(i, 1), " " * (self.rect.size.width - 2),
                    Color.get_color(Color.WHITE, Color.BLACK))
        return

    def on_resize(self, msg):
        self.client_size = Size(self.rect.size.width - 2,
                self.rect.size.height - 2)

    def on_get_focus(self, msg):
        self.draw_borders()
        self.update()

    def on_lost_focus(self, msg):
        self.draw_borders()
        self.update()

    def draw_borders(self):
        c = None
        if self.focused:
            c = Color.get_color(Color.BLACK, Color.YELLOW)
        else:
            c = Color.get_color(Color.BLACK, Color.WHITE)

        #Top
        self.draw(Pos(0, 0), ' ' * self.rect.size.width, c)

        #Bottom
        self.draw(Pos(self.rect.size.height - 1, 0), 
                ' ' * self.rect.size.width, c)

        #Left
        for top in range(1, self.rect.size.height - 1):
            self.draw(Pos(top, 0), ' ', c)

        #Right
        for top in range(1, self.rect.size.height - 1):
            self.draw(Pos(top, self.rect.size.width - 1), ' ', c)

        self.draw_tags()

    def draw_tags(self):
        bg = None
        if self.focused:
            bg = Color.YELLOW
        else:
            bg = Color.WHITE

        unselected_color = Color.get_color(Color.GREEN, bg)
        selected_color = Color.get_color(Color.RED, bg)

        left = 1
        if self.begin_tag > 0:
            s = "<<"
            self.draw(Pos(0, left), s, unselected_color)
            left = left +len(s)

        for i in range(self.begin_tag, len(self.children)):
            s = "[%d:%s]"%(i, w.title)
            if self.client_size.width < left + len(s) + 2:
                if self.client_size.width < left + len(s):
                    self.draw(Pos(0, left), ">>", unselected_color)
                    break

                elif i + 1 < len(self.children):
                    self.draw(Pos(0, left), ">>", unselected_color)
                    break

            if self.children[i].focused:
                self.draw(Pos(0, left), s, selected_color)
            else:
                self.draw(Pos(0, left), s, unselected_color)

        return
