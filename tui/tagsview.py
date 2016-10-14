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
import curses

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
        self.regist_msg_func(Message.MSG_LCLICK, self.on_lclick)

    def set_focus(self, stat):
        if stat:
            self.parent.focused_view.set_focus(False)
            self.parent.focused_view = self

        Frame.set_focus(self, stat)

    def on_draw(self, msg):
        self.draw_borders()
        for i in range(1, self.rect.size.height - 1):
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
        #Check size
        if direct == TagsView.SP_VERTICAL and self.rect.size.width < 6:
            return

        elif direct == TagsView.SP_HORIZONTAL and self.rect.size.height < 6:
            return
        
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

    def change_height(self, offset, update = True):
        #Check size of views
        if self.rect.size.height + offset < 3:
            return

        if len(self.bottom_docked) > 0:
            #Check size of views
            for v in self.bottom_docked:
                if v.rect.size.height - offset < 3:
                    return

            for v in self.bottom_docked[0].top_docked:
                if v.rect.size.height + offset < 3:
                    return

            #Resize
            self.rect.size.height += offset
            for v in self.bottom_docked:
                v.rect.pos.top += offset
                v.rect.size.height -= offset
                v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                v.redraw()
                
            for v in self.bottom_docked[0].top_docked:
                if v != self:
                    v.rect.size.height += offset
                    v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                    v.redraw()

        elif len(self.top_docked) > 0:
            #Check size of views
            for v in self.top_docked:
                if v.rect.size.height - offset < 3:
                    return

            for v in self.top_docked[0].bottom_docked:
                if v.rect.size.height + offset < 3:
                    return

            #Resize
            self.rect.pos.top -= offset
            self.rect.size.height += offset
            for v in self.top_docked:
                v.rect.size.height -= offset
                v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                v.redraw()

            for v in self.top_docked[0].bottom_docked:
                if v != self:
                    v.rect.pos.top -= offset
                    v.rect.size.height +=  offset
                    v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                    v.redraw()

        else:
            return

        self.dispatch_msg(Message(Message.MSG_RESIZE, self.rect))
        self.dispatch_msg(Message(Message.MSG_REDRAW, None))

        if update:
            self.update()

        return

    def change_width(self, offset, update = True):
        #Check size of views
        if self.rect.size.width + offset < 3:
            return

        if len(self.right_docked) > 0:
            #Check size of views
            for v in self.right_docked:
                if v.rect.size.width - offset < 3:
                    return

            for v in self.right_docked[0].left_docked:
                if v.rect.size.width + offset < 3:
                    return

            #Resize
            self.rect.size.width += offset
            for v in self.right_docked:
                v.rect.pos.left += offset
                v.rect.size.width -= offset
                v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                v.redraw()

            for v in self.right_docked[0].left_docked:
                if v != self:
                    v.rect.size.width += offset
                    v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                    v.redraw()

        elif len(self.left_docked) > 0:
            #Check size of views
            for v in self.left_docked:
                if v.rect.size.width - offset < 3:
                    return

            for v in self.left_docked[0].right_docked:
                if v.rect.size.width + offset < 3:
                    return

            #Resize
            self.rect.pos.left -= offset
            self.rect.size.width += offset
            for v in self.left_docked:
                v.rect.size.width -= offset
                v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                v.redraw()

            for v in self.left_docked[0].right_docked:
                if v != self:
                    v.rect.pos.left -= offset
                    v.rect.size.width += offset
                    v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                    v.redraw()

        else:
            return

        self.dispatch_msg(Message(Message.MSG_RESIZE, self.rect))
        self.dispatch_msg(Message(Message.MSG_REDRAW, None))

        if update:
            self.update()

        return

    def workspace_h_resize(self, top, rate):
        self.rect.pos.top = top
        new_height = max(int(self.rect.size.height * rate), 3)

        if len(self.bottom_docked) == 0:
            if new_height + top != self.parent.client_size.height:
                new_height = self.parent.client_size.height - top

            self.rect.size.height = new_height

        else:
            self.rect.size.height = new_height
            for v in self.bottom_docked:
                v.workspace_h_resize(top + new_height, rate)

        return

    def workspace_w_resize(self, left, rate):
        self.rect.pos.left = left
        new_width = max(int(self.rect.size.width * rate), 3)

        if len(self.right_docked) == 0:
            if new_width + left != self.parent.client_size.width:
                new_width = self.parent.client_size.width - left

            self.rect.size.width = new_width

        else:
            self.rect.size.width = new_width
            for v in self.right_docked:
                v.workspace_w_resize(left + new_width, rate)
        return

    def on_ldrag(self, msg):
        if msg.data.top == 0:
            self.top_drag()

        elif msg.data.top == self.rect.size.height - 1:
            self.bottom_drag()

        elif msg.data.left == 0:
            self.left_drag()

        elif msg.data.left == self.rect.size.width - 1:
            self.right_drag()

        else:
            return False

        return True

    def on_lclick(self, msg):
        if msg.data.top == 0:
            pass
        return False

    def top_drag(self):
        if len(self.top_docked) == 0:
            return

        return

        while True:
            stat = curses.getmouse()
            raise Exception()
            offset = pos.top - self.rect.pos.top

            if self.rect.size.height + offset < 3:
                offset = 3 - self.rect.size.height

            #Check size of views
            for v in self.top_docked:
                if v.rect.size.height - offset < 3:
                    continue

            for v in self.top_docked[0].bottom_docked:
                if v.rect.size.height + offset < 3:
                    continue

            #Resize
            self.rect.pos.top -= offset
            self.rect.size.height += offset
            for v in self.top_docked:
                v.rect.size.height -= offset
                v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                v.redraw()

            for v in self.top_docked[0].bottom_docked:
                if v != self:
                    v.rect.pos.top -= offset
                    v.rect.size.height +=  offset
                    v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                    v.redraw()
        return

    def bottom_drag(self):
        if len(self.bottom_docked) == 0:
            return

        while not test_l_btn_release():
            pos = get_mouse_pos()

        return

    def left_drag(self):
        if len(self.left_docked) == 0:
            return

        while not test_l_btn_release():
            pos = get_mouse_pos()

        return

    def right_drag(self):
        if len(self.right_docked) == 0:
            return

        while not test_l_btn_release():
            pos = get_mouse_pos()

        return
