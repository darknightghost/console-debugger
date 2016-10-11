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
from tui.container import *

class Workspace:
    COMMAND_MODE = 0
    EDIT_MODE = 1
    def __init__(self, max_history = 256):
        self.alive = True
        self.exit_code = 0
        self.containers = []
        self.focused_container = None
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
            self.size = Size(wnd_size[1] - 1, wnd_size[0])
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

            #Main container
            self.containers.append(Container(self, Rect(Pos(0, 0), 
                Size(self.client_size.width, self.client_size.height))))

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
        for c in self.containers:
            c.close()
        return

    def input_loop(self):
        while self.alive:
            try:
                key = self.stdscr.getch()
                if key == curses.KEY_MOUSE:
                    self.dispatch_input(key, curses.getmouse())
                else:
                    self.dispatch_input(key, None)
            except KeyboardInterrupt:
                key = self.stdscr.getch()
                self.dispatch_input(key, None)

        return

    def dispatch_input(self, key, mouse):
        if key == Keyboard.KEY_RESIZE:
            wnd_size = self.stdscr.getmaxyx()
            self.resize(Size(wnd_size[1] - 1, wnd_size[0]))
            return

        if key == Keyboard.KEY_ESC:
            self.mode = self.COMMAND_MODE
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
        if ch == Keyboard.KEY_LF:
            #Enter
            self.add_history()
            self.on_command(self.command_buf)
            self.command_buf = ""
            self.command_curser = 0
            self.cmd_show_begin = 0

        elif ch in (Keyboard.KEY_DEL, Keyboard.KEY_BACKSPACE):
            #Backspace
            if self.command_curser > 0:
                self.command_buf = self.command_buf[: self.command_curser - 1] \
                        + self.command_buf[self.command_curser :]
                self.command_curser = self.command_curser - 1
                if self.cmd_show_begin > 0:
                    self.cmd_show_begin = self.cmd_show_begin - 1

        elif ch == Keyboard.KEY_DC:
            #Delete
            if self.command_curser < len(self.command_buf):
                self.command_buf = self.command_buf[: self.command_curser] \
                        + self.command_buf[self.command_curser + 1 :]
                if self.cmd_show_begin > 0 \
                        and self.command_curser < self.cmd_show_begin:
                    self.cmd_show_begin = self.command_curser

        elif ch == Keyboard.KEY_UP:
            #Up
            s = self.prev_history()
            if s != None:
                self.command_buf = s
            self.command_curser = len(self.command_buf)

        elif ch == Keyboard.KEY_DOWN:
            #Down
            s = self.next_history()
            if s != None:
                self.command_buf = s
            self.command_curser = len(self.command_buf)

        elif ch == Keyboard.KEY_LEFT:
            #Left
            if self.command_curser > 0:
                self.command_curser = self.command_curser - 1
                
                if self.command_curser < self.cmd_show_begin:
                    self.cmd_show_begin = self.command_curser

        elif ch == Keyboard.KEY_RIGHT:
            #Right
            if self.command_curser < len(self.command_buf) + 1:
                self.command_curser = self.command_curser + 1

                if self.command_curser - self.cmd_show_begin + 1 \
                        > self.size.width:
                    self.cmd_show_begin = self.command_curser - self.size.width + 1

        elif ch == Keyboard.KEY_HOME:
            #Home
            self.command_curser = 0
            self.cmd_show_begin = 0

        elif ch == Keyboard.KEY_END:
            #End
            self.command_curser = len(self.command_buf)
            if self.command_curser - self.cmd_show_begin \
                    > self.size.width:
                self.cmd_show_begin = self.command_curser - self.size.width + 1

        else:
            self.command_buf = self.command_buf[: self.command_curser] + chr(ch) \
                    + self.command_buf[self.command_curser :]
            self.command_curser = self.command_curser + 1
            if self.command_curser - self.cmd_show_begin + 1 \
                    > self.size.width:
                self.cmd_show_begin = self.command_curser - self.size.width + 1


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

    def cmdline_refresh(self):
        #Draw command line
        for i in range(self.cmd_show_begin, \
                self.cmd_show_begin + self.size.width):
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

    def enter_edit_mode(self):
        self.mode == self.EDIT_MODE
        self.stdscr.addstr(self.size.height - 1, 0, " " * self.size.width,
                Color.get_color(Color.WHITE, Color.Black) | curses.A_BOLD)
        self.stdscr.addnstr(self.size.height - 1, 0, "<Edit Mode>",
                self.size.width, 
                Color.get_color(Color.WHITE, Color.Black) | curses.A_BOLD)

        self.command_buf = ""
        self.command_curser = 0
        self.update()

        return

    def resize(self, size):
        old_size = self.size
        self.size = size
        self.client_size = Size(self.size.width, self.size.height - 1)
        self.cmdline_refresh()

        x_rate = size.width / old_size.width
        y_rate = size.height / old_size.height

        for c in self.containers:
            c.resize(Rect(
                Pos(round(c.rect.pos.top * y_rate),
                    round(c.rect.pos.left * x_rate)),
                Size(round(c.rect.size.width * x_rate),
                    round(c.rect.size.height * y_rate))))
        return

    def on_command(self, command):
        raise NotImplementedError() 

    def on_create(self):
        raise NotImplementedError() 
