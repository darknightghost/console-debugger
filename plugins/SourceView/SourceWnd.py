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

from tui import *
from tui.window import *
from tui.controls import *
from plugins.PluginWnd import *
from config import config

class SourceWnd(PluginWnd):
    def __init__(self, text, parent, rect, cfg, plugin, path):
        self.path = path
        self.cursor = 0
        self.lines = []
        self.begin = 0
        self.cliend_size = Size(rect.size.width - 3,
                rect.size.height)
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
                self.print_stat("Failed to open file \"%s\"."%(self.path))
                self.close()

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

    def complete_source(self, compstr):
        return []

    def on_scoll(self, msg):
        pass

    def on_resize(self, msg):
        self.m_scoll_vertical.resize(Rect(Pos(0,
            self.rect.size.width - 3),
            Size(3, self.rect.size.height)))

        self.cliend_size = Size(self.rect.size.width - 3,
                self.rect.size.height)

        self.redraw()
        self.update()

    def count_total_height(self):
        pass

    def load_source_file(self):
        #Load fle
        f = open(self.path, "r")
        lines = f.readlines()
        f.close()

        self.max_line_len = 0

        for l in self.lines:
            t = l.strip("\r\n")
            self.lines.append(t)

        #Set title
        self.text = os.path.split(self.path)[-1]

    class FileChangHandler(watchdog.events.FileSystemEventHandler):
        def __init__(self, name, wnd):
            self.name = name
            self.wnd = wnd
            watchdog.events.FileSystemEventHandler.__init__(self)

        def on_modified(self, event):
            if not event.is_directory:
                if os.path.split(event.src_path)[1] == self.name:
                    #Send message
                    #wnd.msg_inject(Message())
                    pass

    class Line:
        def __init__(self, string, width):
            self.string = string
            self.width = width
