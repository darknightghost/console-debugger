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

import watchdog
import watchdog.events
import watchdog.observers
import os
import math

from tui import *
from tui.window import *
from tui.controls import *
from plugins.PluginWnd import *
from config import config
from common.types import *

class SourceWnd(PluginWnd):
    def __init__(self, text, parent, rect, cfg, plugin, path):
        self.path = path
        self.cursor = 0
        self.begin = 0
        self.client_rect = Rect(
                Pos(0,
                    rect.pos.left + 6),
                Size(rect.size.width - 6 - 3,
                    rect.size.height))
        self.lines = SourceWnd.Lines(self.client_rect.size.width)
        self.max_line_len = 0
        PluginWnd.__init__(self, text, parent, rect, cfg, plugin)

    def init_window(self):
        #Create plugins
        self.m_scoll_vertical = Scollbar("", self, Rect(Pos(0,
            self.rect.size.width - 3),
            Size(3, self.rect.size.height)),
            direction = Scollbar.VERTICAL)

        self.m_scoll_vertical.show()

        #Regist message handlers
        self.regist_msg_func(Message.MSG_RESIZE, self.on_resize)
        self.regist_msg_func(Message.MSG_GETFOCUS, self.on_get_focus)
        self.regist_msg_func(Message.MSG_LOSTFOCUS, self.on_lost_focus)
        self.regist_msg_func(Message.MSG_CLOSE, self.on_close)
        self.regist_msg_func(Message.MSG_CREATE, self.on_create)
        self.regist_msg_func(Message.MSG_REDRAW, self.on_draw)
        self.regist_msg_func(Message.MSG_KEYPRESS, self.on_keypress)

        self.regist_ctrl_msg_func(self.m_scoll_vertical,
                Message.MSG_CHANGED, self.on_scoll)

        #Regist commands
        self.reg_wnd_command("source", self.on_cmd_source, self.complete_source)

    def on_create(self, msg):
        #Load config
        try:
            self.path = self.cfg.get_value("path")

        except config.ConfigValueError:
            if self.path != None:
                self.cfg.set_value("path", self.path)

        try:
            self.begin = int(self.cfg.get_value("begin"))

        except config.ConfigValueError:
            self.cfg.set_value("begin", str(self.begin))

        try:
            self.cursor = int(self.cfg.get_value("cursor"))

        except config.ConfigValueError:
            self.cfg.set_value("cursor", str(self.cursor))

        #Load file
        if self.path != None:
            try:
                self.load_source_file()

            except FileNotFoundError:
                self.text = "SourceView"

        self.redraw()
        self.update()

    def on_get_focus(self, msg):
        self.enable_wnd_command()

    def on_lost_focus(self, msg):
        self.disable_wnd_command()

    def on_close(self, msg):
        if self.focused:
            self.disable_wnd_command()

    def on_cmd_source(self, command):
        if len(command) < 2:
            return "Too few arguments."

        elif len(command) > 2:
            return "Too many arguments."

        self.begin = 0
        self.cursor = 0
        old_path = self.path
        self.path = command[1]
        try:
            self.load_source_file()

        except FileNotFoundError:
            self.path = old_path
            return "Failed to open file \"%s\"."%(command[1])

        self.redraw()
        self.update()

    def on_draw(self, msg):
        self.draw_cursor()
        self.draw_line_num()
        self.draw_fold_button()
        self.lines.draw(self.client_rect, self)

    def draw_cursor(self):
        for i in range(0, self.rect.size.height):
            self.draw(Pos(i, 0), ' ',
                    Color.get_color(Color.YELLOW, Color.BLACK) | curses.A_BOLD)

    def draw_line_num(self):
        for i in range(0, self.rect.size.height):
            self.draw(Pos(i, 1), ' ' * 4,
                    Color.get_color(Color.YELLOW, Color.BLACK))

    def draw_fold_button(self):
        for i in range(0, self.rect.size.height):
            self.draw(Pos(i, 5), ' ',
                    Color.get_color(Color.YELLOW, Color.WHITE))

    def complete_source(self, compstr):
        return []

    def on_scoll(self, msg):
        self.lines.scoll_to_voff(self.m_scoll_vertical.get_value())
        self.redraw()
        self.update()

    def on_resize(self, msg):
        self.m_scoll_vertical.resize(Rect(Pos(0,
            self.rect.size.width - 3),
            Size(3, self.rect.size.height)))

        self.client_rect = Rect(
                Pos(0,
                    self.rect.pos.left + 6),
                Size(self.rect.size.width - 6 - 3,
                    self.rect.size.height))

        self.lines.set_width(self.client_rect.size.width)

        self.redraw()
        self.update()

    def on_keypress(self, msg):
        if msg.data == Keyboard.KEY_NPAGE:
            self.m_scoll_vertical.set_value(self.m_scoll_vertical.get_value() \
                    + self.client_rect.size.height)

        elif msg.data == Keyboard.KEY_PPAGE:
            self.m_scoll_vertical.set_value(self.m_scoll_vertical.get_value() \
                    - self.client_rect.size.height)


        elif msg.data == Keyboard.KEY_UP:
            self.m_scoll_vertical.set_value(self.m_scoll_vertical.get_value() \
                    - 1)

        elif msg.data == Keyboard.KEY_DOWN:
            self.m_scoll_vertical.set_value(self.m_scoll_vertical.get_value() \
                    + 1)

        return False

    def load_source_file(self):
        #Load file
        f = open(self.path, "r")
        lines = f.readlines()
        f.close()

        self.max_line_len = 0
        self.lines = SourceWnd.Lines(self.client_rect.size.width)

        for l in lines:
            t = l.strip("\r\n")
            self.lines.append(t)

        #Set title
        self.text = os.path.split(self.path)[-1]

        #Scollbar
        self.m_scoll_vertical.set_max_value(
                self.lines.get_height() - self.client_rect.size.height)

    class FileChangeHandler(watchdog.events.FileSystemEventHandler):
        def __init__(self, name, wnd):
            self.name = name
            self.wnd = wnd
            watchdog.events.FileSystemEventHandler.__init__(self)

        def on_modified(self, event):
            if not event.is_diself.text_attrrectory:
                if os.path.split(event.src_path)[1] == self.name:
                    #Send message
                    #wnd.msg_inject(Message())
                    pass

    #Source file lines
    class Lines:
        class Line:
            def __init__(self, string, width):
                self.string = string
                self.width = width
                self.text_attr = Color.get_color(Color.WHITE, Color.BLACK)
                self.additional_text_attr = Color.get_color(Color.WHITE, Color.BLACK)
                self.additional_text = ""

            def set_text_attr(self, attr):
                self.text_attr = attr

            def get_text_attr(self, attr):
                return self.text_attr

            def set_additional_text_attr(self, attr):
                self.additional_text_attr = attr

            def get_additional_text_attr(self, attr):
                return self.additional_text_attr

            def set_additional_text(self, txt):
                self.additional_text = txt

            def set_width(self, width):
                self.width = width

            def height(self):
                ret = math.ceil(String.width(self.string) / self.width)
                if self.additional_text != "":
                    ret += math.ceil(String.width(self.additional_text)
                            / self.width)
                return ret

            def draw(self, rect, begin_off, wnd):
                self.width = rect.size.width

                #Split lines
                lines = []
                s = self.string

                while s != "":
                    newl_len = String.width_to_len(s, 0, self.width)
                    lines.append(s[: newl_len] + ' ' * (self.width - newl_len))
                    s = s[newl_len :]
                    
                text_line_num = len(s)
                additional_txt_lines = self.additional_text.split("\n")
                additional_lines = []
                
                if self.additional_text != "":
                    for l in additional_txt_lines:
                        s = l
                        while s != "":
                            newl_len = String.width_to_len(s, 0, self.width)
                            additional_lines.append(
                                    s[: newl_len] + ' ' * (self.width - newl_len))
                            s = s[newl_len :]

                #Draw lines
                drawed_lines = 0
                for i in range(begin_off, len(lines) + len(additional_lines)):
                    if drawed_lines > rect.size.height:
                        break

                    attr = None

                    if drawed_lines <text_line_num:
                        attr = self.text_attr

                    else:
                        attr = self.additional_text_attr

                    wnd.draw(Pos(rect.pos.top + i - begin_off,
                        rect.pos.left),
                        lines[i], attr)

            def __str__(self):
                return "%s\n%s"%(self.string, self.additional_text)

        #End of class Lines.line

        @check_arg_type(width = (int, ))
        def __init__(self, width):
            self.height = 0
            self.begin_line = 0
            self.v_off = 0
            self.width = width
            #[[line, height], [line, height], ...]
            self.lines = []

        @check_arg_type(string = (str, ))
        def append(self, string):
            new_line = SourceWnd.Lines.Line(string, self.width)
            self.lines.append([new_line, self.height])
            self.height += new_line.height()

        @check_arg_type(line = (int, ))
        def pop(self, line):
            #Pop line
            ret = self.lines.pop(line)
            self.height -= ret[1]

            #Recompute line
            for i in range(line, len(self.lines)):
                self.lines[i][1] -= ret[1]

            return ret[0]

        @check_arg_type(key = (int, ))
        def __getitem__(self, key):
            return self.lines[key][0]

        @check_arg_type(width = (int, ))
        def set_width(self, width):
            if width != self.width:
                self.width = width
                
                self.height = 0
                for i in range(0, len(self.lines)):
                    line = self.lines[i][0]
                    line.set_width(width)
                    self.lines[i][1] = self.height
                    self.height += line.height()

        def get_height(self):
            return self.height

        @check_arg_type(rect = (Rect, ), wnd = (frame.Frame, ))
        def draw(self, rect, wnd):
            #Check width
            if rect.size.width != self.width:
                self.set_width(rect.size.width)

            #Draw lines
            top_off = 0
            begin_off = 0
            for i in range(self.begin_line, len(self.lines)):
                if top_off >= rect.size.height:
                    break

                if i == self.begin_line:
                    begin_off = self.v_off - self.lines[self.begin_line][1]

                else:
                    begin_off = 0

                #Draw line
                self.lines[i][0].draw(Rect(
                    Pos(rect.pos.top + top_off,
                        rect.pos.left),
                    Size(self.width,
                        rect.size.height - top_off)),
                    begin_off,
                    wnd)

                top_off += self.lines[i][0].height()

        def __iter__(self):
            class LinesIter:
                def __init__(self, parent):
                    self.count = 0
                    self.parent = parent

                def next(self):
                    try:
                        ret = self.parent[self.count]
                        self.count += 1
                        return ret

                    except IndexError:
                        raise StopIteration()

            return SourceWnd.Lines.LinesIter(self)

        def line_to_voff(self, line_num):
            return self.lines[line_num][1]

        def voff_to_line(self, v_off):
            if v_off >= self.height:
                raise IndexError()

            line_num = round(len(self.lines) * v_off / self.height)
            while self.lines[line_num][1] > v_off:
                line_num -= 1

            while self.lines[line_num][1] \
                    + self.lines[line_num][0].height() < v_off:
                line_num += 1

            return line_num

        def scoll_to_voff(self, v_off):
            self.v_off = round(v_off)
            if self.v_off >= self.height:
                raise IndexError()

            self.begin_line = self.voff_to_line(self.v_off)

        def scoll_to_line(self, line_num):
            self.v_off = self.lines[line_num][1]
            self.begin_line = line_num
