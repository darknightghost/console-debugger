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
import sys
import locale
import traceback

from tui import *
from tui.tagsview import *

class Workspace:
    COMMAND_MODE = 0
    EDIT_MODE = 1
    def __init__(self, max_history = 256):
        self.alive = True
        self.exit_code = 0
        self.views = []
        self.focused_view = None
        self.mode = self.COMMAND_MODE
        self.command_buf = ""
        self.history = []
        self.max_history = max_history
        self.current_history = 0
        self.command_curser = 0
        self.cmd_show_begin = 0

        return

    def winmain(self):
        try:
            #Begin TUI
            self.stdscr = curses.initscr();

            wnd_size = self.stdscr.getmaxyx()
            self.size = Size(wnd_size[1], wnd_size[0])
            self.client_size = Size(self.size.width, self.size.height - 1)

            curses.noecho()
            curses.cbreak()
            self.stdscr.keypad(1)
            self.stdscr.nodelay(0)

            #Color
            Color.init_color()

            #Background
            self.stdscr.bkgd(' ', Color.get_color(0,Color.BLACK))
            curses.curs_set(0)
            self.cmdline_refresh()

            #Main view
            main_view = TagsView(self, Rect(Pos(0, 0), 
                Size(self.client_size.width, self.client_size.height)))
            self.focused_view = main_view
            main_view.dispatch_msg(Message(Message.MSG_CREATE, None))
            main_view.redraw()
            main_view.set_focus(True)

            self.on_create()
            
            self.update()

            #Input loop
            self.input_loop()

        except Exception as e:
            #End GUI
            self.stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            raise e
        else:
            #End GUI
            self.stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            print("")

        return self.exit_code

    def update(self):
        self.stdscr.refresh()

    def close(self):
        self.alive = False
        for c in self.views:
            c.close()
        return

    def input_loop(self):
        while self.alive:
            try:
                key = self.stdscr.get_wch()
                if isinstance(key, str):
                    key = list(key.encode(errors = "ignore"))

                elif isinstance(key, int):
                    key = [key]

                if key == curses.KEY_MOUSE:
                    self.dispatch_input(key, curses.getmouse())

                else:
                    self.dispatch_input(key, None)

            except KeyboardInterrupt:
                key = list(b'\x03')
                self.dispatch_input(key, None)

            except curses.error:
                continue

        return

    def dispatch_input(self, key, mouse):
        if key[0] <= 26 and key[0] >= 0 and key[0] != Keyboard.KEY_LF:
            #Shotcut key
            self.on_shotcut_key(key)
            return

        if key[0] == Keyboard.KEY_RESIZE:
            wnd_size = self.stdscr.getmaxyx()
            self.resize(Size(wnd_size[1], wnd_size[0]))
            return

        if key[0] == Keyboard.KEY_ESC:
            if self.mode != self.COMMAND_MODE:
                self.mode = self.COMMAND_MODE
            else:
                self.mode = self.EDIT_MODE
            self.cmdline_refresh()
            return

        if self.mode == self.COMMAND_MODE:
            #Command mode
            self.get_command(key)

        else:
            #Edit mode
            pass

        return

    def get_command(self, ch):
        if ch[0] == Keyboard.KEY_LF:
            #Enter
            if self.command_buf == "":
                return

            self.add_history()
            stat = self.on_command(self.command_buf)
            self.command_buf = ""
            self.command_curser = 0
            self.cmd_show_begin = 0

            if stat != None:
                self.print_stat(stat)
                return

        elif ch[0] in (Keyboard.KEY_DEL, Keyboard.KEY_BACKSPACE):
            #Backspace
            if self.command_curser > 0:
                self.command_buf = self.command_buf[: self.command_curser - 1] \
                        + self.command_buf[self.command_curser :]
                self.command_curser = self.command_curser - 1
                if self.cmd_show_begin > 0:
                    self.cmd_show_begin = self.cmd_show_begin - 1

        elif ch[0] == Keyboard.KEY_DC:
            #Delete
            if self.command_curser < len(self.command_buf):
                self.command_buf = self.command_buf[: self.command_curser] \
                        + self.command_buf[self.command_curser + 1 :]
                if self.cmd_show_begin > 0 \
                        and self.command_curser < self.cmd_show_begin:
                    self.cmd_show_begin = self.command_curser

        elif ch[0] == Keyboard.KEY_UP:
            #Up
            s = self.prev_history()
            if s != None:
                self.command_buf = s
            self.command_curser = len(self.command_buf)

        elif ch[0] == Keyboard.KEY_DOWN:
            #Down
            s = self.next_history()
            if s != None:
                self.command_buf = s
            self.command_curser = len(self.command_buf)

        elif ch[0] == Keyboard.KEY_LEFT:
            #Left
            if self.command_curser > 0:
                self.command_curser = self.command_curser - 1
                
                if self.command_curser < self.cmd_show_begin:
                    self.cmd_show_begin = self.command_curser

        elif ch[0] == Keyboard.KEY_RIGHT:
            #Right
            if self.command_curser < len(self.command_buf) + 1:
                self.command_curser = self.command_curser + 1

                if self.command_curser - self.cmd_show_begin + 2 \
                        > self.size.width:
                    self.cmd_show_begin = self.command_curser - self.size.width + 2

        elif ch[0] == Keyboard.KEY_HOME:
            #Home
            self.command_curser = 0
            self.cmd_show_begin = 0

        elif ch[0] == Keyboard.KEY_END:
            #End
            self.command_curser = len(self.command_buf)
            if self.command_curser - self.cmd_show_begin \
                    > self.size.width:
                self.cmd_show_begin = self.command_curser - self.size.width + 2

        else:
            self.command_buf = self.command_buf[: self.command_curser] \
                    + bytes(ch).decode(errors = "ignore") \
                    + self.command_buf[self.command_curser :]
            self.command_curser = self.command_curser + 1
            if self.command_curser - self.cmd_show_begin + 2 \
                    > self.size.width:
                self.cmd_show_begin = self.command_curser - self.size.width + 2


        self.cmdline_refresh()

        return
        
    def add_history(self):
        if self.command_buf == "":
            return

        self.history.append(self.command_buf)
        if len(self.history) > self.max_history:
            self.history = self.history[len(self.history) - self.max_history :]
        self.current_history = len(self.history) - 1

    def prev_history(self):
        if self.current_history == 0:
            return None
        else:
            self.current_history = self.current_history - 1
            return self.history[self.current_history]

    def next_history(self):
        if self.current_history > len(self.history) - 2:
            return None
        else:
            self.current_history = self.current_history + 1
            return self.history[self.current_history]

    def print_stat(self, info):
        attr = Color.get_color(Color.YELLOW, Color.RED) | curses.A_BOLD
        self.stdscr.addstr(self.size.height - 1, 0, " " * (self.size.width - 1), 
                attr);
        self.stdscr.addnstr(self.size.height - 1, 0, info, self.size.width - 1,
                attr);

    def cmdline_refresh(self):
        #Draw command line
        for i in range(self.cmd_show_begin, \
                self.cmd_show_begin + self.size.width - 1):
            attr = Color.get_color(Color.WHITE, Color.BLUE)
            if i == self.command_curser and self.mode == self.COMMAND_MODE:
                attr = attr | curses.A_REVERSE | curses.A_BOLD

            else:
                attr = attr | curses.A_BOLD

            c = ''
            if i < len(self.command_buf):
                c = self.command_buf[i]
            else:
                c = ' '
            self.stdscr.addstr(self.size.height - 1, i - self.cmd_show_begin,
                    c, attr)

        self.update()

        return

    def resize(self, size):
        old_size = self.size
        self.size = size
        self.client_size = Size(self.size.width, self.size.height - 1)
        self.cmdline_refresh()

        x_rate = size.width / old_size.width
        y_rate = size.height / old_size.height

        #Resize child views
        for c in self.views:
            c.resize(Rect(
                Pos(round(c.rect.pos.top * y_rate),
                    round(c.rect.pos.left * x_rate)),
                Size(round(c.rect.size.width * x_rate),
                    round(c.rect.size.height * y_rate))))
        return

    def draw(self, pos, string, attr):
        self.stdscr.addstr(pos.top, pos.left, string, attr)
        return

    def add_child(self, child):
        self.views.append(child)

    def remove_child(self, child):
        self.views.remove(child)
        #TODO:Join view

    def on_command(self, command):
        raise NotImplementedError() 

    def on_create(self):
        raise NotImplementedError() 

    def on_shotcut_key(self, key):
        if key == Keyboard.KEY_CTRL_("w"):
            #Tab view control
            pass
        return
