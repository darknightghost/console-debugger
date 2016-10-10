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
from tui.frame import *

class Workspace:
    COMMAND_MODE = 0
    EDIT_MODE = 1
    def __init__(self):
        self.alive = True
        self.exit_code = 0
        self.frames = []
        self.focused_frame = None
        self.mode = self.COMMAND_MODE

        return

    def winmain(self):
        try:
            #Begin TUI
            self.stdscr = curses.initscr();

            wnd_size = self.stdscr.getmaxyx()
            self.size = Size(wnd_size[0] + 1, wnd_size[1] + 1)
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
        for f in self.frames:
            f.close()
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
        if key == Keyboard.KEY_ESC:
            self.close()

        elif key == Keyboard.KEY_ASCII("a"):
            Clipboard.write("aaaacccc")

        elif key == Keyboard.KEY_ASCII("s"):
            raise Exception(Clipboard.read())
