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
        self.regist_msg_func(Message.MSG_DRAG, self.on_ldrag)
        self.regist_msg_func(Message.MSG_CLOSE, self.on_close)

        self.dispatch_msg(Message(Message.MSG_CREATE, None))

    def set_focus(self, stat):
        if stat:
            self.parent.focused_view.set_focus(False)
            self.parent.focused_view = self

        Frame.set_focus(self, stat)
        
        if self.focused_child != None:
            self.focused_child.set_focus(stat)

        self.update()

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

    def on_lost_focus(self, msg):
        self.draw_borders()

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

        unselected_color = Color.get_color(Color.BLUE, bg)
        selected_color = Color.get_color(Color.RED, bg)

        left = 1
        if self.begin_tag > 0:
            s = "<<"
            self.draw(Pos(0, left), s, unselected_color)
            left = left +len(s)

        for i in range(self.begin_tag, len(self.children)):
            s = "[%d:%s]"%(i, self.children[i].text)
            if self.client_size.width < left + len(s) + 2 - 1:
                if self.client_size.width < left + len(s):
                    self.draw(Pos(0, left), ">>", unselected_color)
                    break

                elif i + 1 < len(self.children):
                    self.draw(Pos(0, left), ">>", unselected_color)
                    break

            if self.children[i] == self.focused_child:
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

        new_view.redraw()
        self.update()

        return

    def add_child(self, child):
        Frame.add_child(self, child)
        self.draw_tags()
        return

    def dock(self, view, edge):
        if edge == TagsView.DOCK_TOP and not view in self.top_docked:
            self.top_docked.append(view)
            view.dock(self, TagsView.DOCK_BOTTOM)

        elif edge == TagsView.DOCK_BOTTOM and not view in self.bottom_docked:
            self.bottom_docked.append(view)
            view.dock(self, TagsView.DOCK_TOP)

        elif edge == TagsView.DOCK_LEFT and not view in self.left_docked:
            self.left_docked.append(view)
            view.dock(self, TagsView.DOCK_RIGHT)

        elif edge == TagsView.DOCK_RIGHT and not view in self.right_docked:
            self.right_docked.append(view)
            view.dock(self, TagsView.DOCK_LEFT)

        return

    def undock(self, view, edge):
        if edge == TagsView.DOCK_TOP and view in self.top_docked:
            self.top_docked.remove(view)
            view.undock(self, TagsView.DOCK_BOTTOM)

        elif edge == TagsView.DOCK_BOTTOM and view in self.bottom_docked:
            self.bottom_docked.remove(view)
            view.undock(self, TagsView.DOCK_TOP)

        elif edge == TagsView.DOCK_LEFT and view in self.left_docked:
            self.left_docked.remove(view)
            view.undock(self, TagsView.DOCK_RIGHT)

        elif edge == TagsView.DOCK_RIGHT and view in self.right_docked:
            self.right_docked.remove(view)
            view.undock(self, TagsView.DOCK_LEFT)

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
        self.redraw()

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
        self.redraw()

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
        if msg.data[0].top == 0:
            self.top_drag(msg.data[0], msg.data[1])

        elif msg.data[0].top == self.rect.size.height - 1:
            self.bottom_drag(msg.data[0], msg.data[1])

        elif msg.data[0].left == 0:
            self.left_drag(msg.data[0], msg.data[1])

        elif msg.data[0].left == self.rect.size.width - 1:
            self.right_drag(msg.data[0], msg.data[1])

        else:
            return False

        return True

    def on_lclick(self, msg):
        if msg.data.top == 0 and len(self.children) > 0:
            self.print_stat(str(msg.data.left))
            offset = 1
            if self.begin_tag > 0:
                if msg.data.left in range(offset, offset + len("<<")):
                    self.begin_tag -= 1
                    self.draw_borders()
                    self.update()
                    return True

                offset += 2

            i = self.begin_tag
            while offset + len(self.children[i].text) - 1 \
                    < self.client_size.width - 2 and i < len(self.children):
                if msg.data.left in range(offset,
                        offset + len(self.children[i].text)):
                    #Active tag
                    if self.children[i] != self.focused_child:
                        if self.focused_child != None:
                            self.focused_child.hide()
                        self.children[i].set_focus(True)
                        self.children[i].show()
                        self.draw_borders()
                        self.update()

                    return True
                offset += len(self.children[i].text)

            if i < len(self.children):
                if len(self.children) > 1 or len(self.children[i].text) > 2:
                    if msg.data.left in range(offset, offset + 2):
                        self.begin_tag += 1
                        self.draw_borders()
                        self.update()
                        return True

                else:
                    if self.children[i] != self.focused_child:
                        if self.focused_child != None:
                            self.focused_child.hide()
                        self.children[i].set_focus(True)
                        self.children[i].show()
                        self.draw_borders()
                        self.update()

                    return True

        return False

    def top_drag(self, old_pos, new_pos):
        if len(self.top_docked) == 0:
            return

        offset = new_pos.top - old_pos.top

        self.top_docked[0].change_height(offset)

    def bottom_drag(self, old_pos, new_pos):
        if len(self.bottom_docked) == 0:
            return

        offset = new_pos.top - old_pos.top

        self.change_height(offset)
       
    def left_drag(self, old_pos, new_pos):
        if len(self.left_docked) == 0:
            return

        offset = new_pos.left - old_pos.left

        self.left_docked[0].change_width(offset)

    def right_drag(self, old_pos, new_pos):
        if len(self.right_docked) == 0:
            return

        offset = new_pos.left - old_pos.left

        self.change_width(offset)

    def on_close(self, msg):
        if len(self.top_docked) > 0 \
                and len(self.top_docked[0].bottom_docked) == 1:
            #Top
            for v in self.top_docked:
                v.rect.size.height += self.rect.size.height
                v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                v.redraw()

                for v1 in self.bottom_docked:
                    v1.dock(v, TagsView.DOCK_TOP)
        
        elif len(self.bottom_docked) > 0 \
                and len(self.bottom_docked[0].top_docked) == 1:
            #Bottom
            for v in self.bottom_docked:
                v.rect.pos.top -= self.rect.size.height
                v.rect.size.height += self.rect.size.height
                v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                v.redraw()

                for v1 in self.top_docked:
                    v1.dock(v, TagsView.DOCK_BOTTOM)

        elif len(self.left_docked) > 0 \
                and len(self.left_docked[0].right_docked) == 1:
            #Left
            for v in self.left_docked:
                v.rect.size.width += self.rect.size.width
                v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                v.redraw()

                for v1 in self.right_docked:
                    v1.dock(v, TagsView.LEFT_BOTTOM)

        elif len(self.right_docked) > 0 \
                and len(self.right_docked[0].left_docked) == 1:
            #Right
            for v in self.right_docked:
                v.rect.pos.left -= self.rect.size.width
                v.rect.size.width += self.rect.size.width
                v.dispatch_msg(Message(Message.MSG_RESIZE, v.rect))
                v.redraw()

                for v1 in self.left_docked:
                    v1.dock(v, TagsView.DOCK_RIGHT)

        else:
            self.parent.close()

        self.undock_all()
        self.parent.update()

    def undock_all(self):
        for v in self.top_docked:
            self.undock(v, TagsView.DOCK_TOP)

        for v in self.bottom_docked:
            self.undock(v, TagsView.DOCK_BOTTOM)

        for v in self.left_docked:
            self.undock(v, TagsView.DOCK_LEFT)

        for v in self.right_docked:
            self.undock(v, TagsView.DOCK_RIGHT)

        return

