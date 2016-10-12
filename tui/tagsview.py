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
    SP_VERTICAL = 0
    SP_HORIZONTAL = 1

    DOCK_TOP = 0
    DOCK_BOTTOM = 1
    DOCK_LEFT = 2
    DOCK_RIGHT = 3

    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3

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

            left = left + len(s)

        return

    def split(self, direct):
        self_rect = None
        new_rect = None

        #Compute new rect
        if direct == TagsView.SP_VERTICAL:
            self_rect = Rect(Pos(self.rect.pos.top,
                self.rect.pos.left),
                Size(self.rect.size.width / 2,
                    self.rect.size.height))
            new_rect = Rect(Pos(self.rect.pos.top,
                self.rect.pos.left + self_rect.size.width),
                Size(self.rect.size.width - self_rect.size.width,
                    self.rect.size.height))

        elif direct == TagsView.SP_HORIZONTAL:
            self_rect = Rect(Pos(self.rect.pos.top,
                self.rect.pos.left),
                Size(self.rect.size.width,
                    self.rect.size.height / 2))

            new_rect = Rect(Pos(self.rect.pos.top + self_rect.size.height,
                self.rect.pos.left),
                Size(self.rect.size.width,
                    self.rect.size.height - self_rect.size.height))

        #Resize current tagsview
        self.resize(self_rect)

        #Create new tagsview
        new_view = TagsView(self.parent, new_rect)
        new_view.set_focus(False)

        #Dock view
        if direct == TagsView.SP_VERTICAL:
            #Right
            for v in self.right_docked:
                new_view.dock(v, TagsView.DOCK_RIGHT)
                self.undock(v, TagsView.DOCK_RIGHT)
            self.dock(new_view, TagsView.DOCK_RIGHT)

            #Top
            for v in self.top_docked:
                new_view.dock(v, TagsView.DOCK_TOP)

            #Bottom
            for v in self.bottom_docked:
                new_view.dock(v, TagsView.DOCK_BOTTOM)

        elif direct == TagsView.SP_HORIZONTAL:
            #Bottom
            for v in self.bottom_docked:
                new_view.dock(v, TagsView.DOCK_BOTTOM)
                self.undock(v, TagsView.DOCK_BOTTOM)
            self.dock(new_view, TagsView.DOCK_BOTTOM)

            #Left
            for v in self.left_docked:
                new_view.dock(v, TagsView.DOCK_LEFT)

            #Right
            for v in self.right_docked:
                new_view.dock(v, TagsView.DOCK_RIGHT)

            return

    def dock(self, view, edge, autodock = True):
        if edge == TagsView.DOCK_TOP and not view in self.top_docked:
            self.top_docked.append(view)
            view.dock(self, TagsView.DOCK_BOTTOM, autodock = False)

        elif edge == TagsView.DOCK_BOTTOM and not view in self.bottom_docked:
            self.bottom_docked.append(view)
            view.dock(self, TagsView.DOCK_TOP, autodock = False)

        elif edge == TagsView.DOCK_LEFT and not view in self.left_docked:
            self.left_docked.append(view)
            view.dock(self, TagsView.DOCK_RIGHT, autodock = False)

        elif edge == TagsView.DOCK_RIGHT and not view in self.right_docked:
            self.right_docked.append(view)
            view.dock(self, TagsView.DOCK_LEFT, autodock = False)

        return

    def undock(self, view, edge, autodock = True):
        if edge == TagsView.DOCK_TOP and view in self.top_docked:
            self.top_docked.remove(view)
            view.undock(self, TagsView.DOCK_BOTTOM, autodock = False)

        elif edge == TagsView.DOCK_BOTTOM and view in self.bottom_docked:
            self.bottom_docked.remove(view)
            view.undock(self, TagsView.DOCK_TOP, autodock = False)

        elif edge == TagsView.DOCK_LEFT and view in self.left_docked:
            self.left_docked.remove(view)
            view.undock(self, TagsView.DOCK_RIGHT, autodock = False)

        elif edge == TagsView.DOCK_RIGHT and view in self.right_docked:
            self.right_docked.remove(view)
            view.undock(self, TagsView.DOCK_LEFT, autodock = False)

        return

    def next_view(self, direct):
        try:
            if direct == TagsView.TOP:
                return self.top_docked[0]

            elif direct == TagsView.BOTTOM:
                return self.bottom_docked[0]

            elif direct == TagsView.LEFT:
                return self.left_docked[0]

            elif direct == TagsView.RIGHT:
                return self.right_docked[0]

        except IndexError:
            return None

