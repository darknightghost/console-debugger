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
import platform
import os
import sys
import pyperclip
import _thread

class Color:
    BLACK = curses.COLOR_BLACK
    BLUE = curses.COLOR_BLUE
    GREEN = curses.COLOR_GREEN
    CYAN = curses.COLOR_CYAN
    RED = curses.COLOR_RED
    MAGENTA = curses.COLOR_MAGENTA
    YELLOW = curses.COLOR_YELLOW
    WHITE = curses.COLOR_WHITE

    def init_color():
        curses.start_color()
        for i in range(7 + 1):
            for j in range(7 + 1):
                if (7 - i) * 8 + j != 0:
                    curses.init_pair((7 - i) * 8 + j,i,j)
        return
        
    def get_color(fg, bg):
        return curses.color_pair((7 - fg) * 8 + bg)

class Pos:
    def __init__(self, top, left):
        self.top = round(top)
        self.left = round(left)

    def __eq__(self, obj):
        if self.top == obj.top and self.left == obj.left:
            return True

        else:
            return False

    def __str__(self):
        return "top = %d, left = %d"%(self.top, self.left)

class Size:
    def __init__(self, width, height):
        self.width = round(width)
        self.height = round(height)

    def __eq__(self, obj):
        if self.width == obj.width and self.height == obj.height:
            return True

        else:
            return False

    def __str__(self):
        return "width = %d, height = %d"%(self.width, self.height)

class Rect:
    def __init__(self, pos, size):
        if not isinstance(pos, Pos):
            raise TypeError("\"pos\" must be a instance of Pos.")
        self.pos = pos

        if not isinstance(size, Size):
            raise TypeError("\"size\" must be a instance of Size.")
        self.size = size

    def __contains__(self, key):
        if isinstance(key, Pos):
            if key.top >= self.pos.top \
                    and key.left >= self.pos.left \
                    and key.top < self.pos.top + self.size.height \
                    and key.left < self.pos.left + self.size.width:
                return True

            else:
                return False


        elif isinstance(key, Rect):
            if key.pos in self \
                    and Pos(key.pos.top + key.size.height - 1, 
                            key.pos.left) in self \
                    and Pos(key.pos.top, 
                            key.pos.left + key.size.width - 1) in self \
                    and Pos(key.pos.top + key.size.height - 1, 
                            key.pos.left + key.size.width - 1) in self:
                return True

            else:
                return False

        else:
            raise TypeError("Rect() only contains Rect() or Pos().")

    def __eq__(self, obj):
        if self.pos == obj.pos and self.size == obj.size:
            return True

        else:
            return False

    def __str__(self):
        return str(self.pos) + "," + str(self.size)

class Keyboard:
    KEY_INTERRUPT = -1

    KEY_NULL = 0
    KEY_SOH = 1
    KEY_STX = 2
    KEY_ETX = 3
    KEY_EOT = 4
    KEY_ENQ = 5
    KEY_ACK = 6
    KEY_BEL = 7
    KEY_BS = 8
    KEY_HT = 9
    KEY_LF = 10
    KEY_VT = 11
    KEY_FF = 12
    KEY_CR = 13
    KEY_SO = 14
    KEY_SI = 15
    KEY_DLE = 16
    KEY_DC1 = 17
    KEY_DC2 = 18
    KEY_DC3 = 19
    KEY_DC4 = 20
    KEY_NAK = 21
    KEY_SYN = 22
    KEY_ETB = 23
    KEY_CAN = 24
    KEY_EM = 25
    KEY_SUB = 26
    KEY_ESC = 27
    KEY_FS = 28
    KEY_GS = 29
    KEY_RS = 30
    KEY_US = 31

    KEY_DEL = 127

    KEY_BREAK = curses.KEY_BREAK
    KEY_MIN = curses.KEY_MIN
    KEY_DOWN = curses.KEY_DOWN
    KEY_UP = curses.KEY_UP
    KEY_LEFT = curses.KEY_LEFT
    KEY_RIGHT = curses.KEY_RIGHT
    KEY_HOME = curses.KEY_HOME
    KEY_BACKSPACE = curses.KEY_BACKSPACE
    KEY_F0 = curses.KEY_F0
    KEY_F1 = curses.KEY_F1
    KEY_F2 = curses.KEY_F2
    KEY_F3 = curses.KEY_F3
    KEY_F4 = curses.KEY_F4
    KEY_F5 = curses.KEY_F5
    KEY_F6 = curses.KEY_F6
    KEY_F7 = curses.KEY_F7
    KEY_F8 = curses.KEY_F8
    KEY_F9 = curses.KEY_F9
    KEY_F10 = curses.KEY_F10
    KEY_F11 = curses.KEY_F11
    KEY_F12 = curses.KEY_F12
    KEY_F13 = curses.KEY_F13
    KEY_F14 = curses.KEY_F14
    KEY_F15 = curses.KEY_F15
    KEY_F16 = curses.KEY_F16
    KEY_F17 = curses.KEY_F17
    KEY_F18 = curses.KEY_F18
    KEY_F19 = curses.KEY_F19
    KEY_F20 = curses.KEY_F20
    KEY_F21 = curses.KEY_F21
    KEY_F22 = curses.KEY_F22
    KEY_F23 = curses.KEY_F23
    KEY_F24 = curses.KEY_F24
    KEY_F25 = curses.KEY_F25
    KEY_F26 = curses.KEY_F26
    KEY_F27 = curses.KEY_F27
    KEY_F28 = curses.KEY_F28
    KEY_F29 = curses.KEY_F29
    KEY_F30 = curses.KEY_F30
    KEY_F31 = curses.KEY_F31
    KEY_F32 = curses.KEY_F32
    KEY_F33 = curses.KEY_F33
    KEY_F34 = curses.KEY_F34
    KEY_F35 = curses.KEY_F35
    KEY_F36 = curses.KEY_F36
    KEY_F37 = curses.KEY_F37
    KEY_F38 = curses.KEY_F38
    KEY_F39 = curses.KEY_F39
    KEY_F40 = curses.KEY_F40
    KEY_F41 = curses.KEY_F41
    KEY_F42 = curses.KEY_F42
    KEY_F43 = curses.KEY_F43
    KEY_F44 = curses.KEY_F44
    KEY_F45 = curses.KEY_F45
    KEY_F46 = curses.KEY_F46
    KEY_F47 = curses.KEY_F47
    KEY_F48 = curses.KEY_F48
    KEY_F49 = curses.KEY_F49
    KEY_F50 = curses.KEY_F50
    KEY_F51 = curses.KEY_F51
    KEY_F52 = curses.KEY_F52
    KEY_F53 = curses.KEY_F53
    KEY_F54 = curses.KEY_F54
    KEY_F55 = curses.KEY_F55
    KEY_F56 = curses.KEY_F56
    KEY_F57 = curses.KEY_F57
    KEY_F58 = curses.KEY_F58
    KEY_F59 = curses.KEY_F59
    KEY_F60 = curses.KEY_F60
    KEY_F61 = curses.KEY_F61
    KEY_F62 = curses.KEY_F62
    KEY_F63 = curses.KEY_F63
    KEY_DL = curses.KEY_DL
    KEY_IL = curses.KEY_IL
    KEY_DC = curses.KEY_DC
    KEY_IC = curses.KEY_IC
    KEY_EIC = curses.KEY_EIC
    KEY_CLEAR = curses.KEY_CLEAR
    KEY_EOS = curses.KEY_EOS
    KEY_EOL = curses.KEY_EOL
    KEY_SF = curses.KEY_SF
    KEY_SR = curses.KEY_SR
    KEY_NPAGE = curses.KEY_NPAGE
    KEY_PPAGE = curses.KEY_PPAGE
    KEY_STAB = curses.KEY_STAB
    KEY_CTAB = curses.KEY_CTAB
    KEY_CATAB = curses.KEY_CATAB
    KEY_ENTER = curses.KEY_ENTER
    KEY_SRESET = curses.KEY_SRESET
    KEY_RESET = curses.KEY_RESET
    KEY_PRINT = curses.KEY_PRINT
    KEY_LL = curses.KEY_LL
    KEY_A1 = curses.KEY_A1
    KEY_A3 = curses.KEY_A3
    KEY_B2 = curses.KEY_B2
    KEY_C1 = curses.KEY_C1
    KEY_C3 = curses.KEY_C3
    KEY_BTAB = curses.KEY_BTAB
    KEY_BEG = curses.KEY_BEG
    KEY_CANCEL = curses.KEY_CANCEL
    KEY_CLOSE = curses.KEY_CLOSE
    KEY_COMMAND = curses.KEY_COMMAND
    KEY_COPY = curses.KEY_COPY
    KEY_CREATE = curses.KEY_CREATE
    KEY_END = curses.KEY_END
    KEY_EXIT = curses.KEY_EXIT
    KEY_FIND = curses.KEY_FIND
    KEY_HELP = curses.KEY_HELP
    KEY_MARK = curses.KEY_MARK
    KEY_MESSAGE = curses.KEY_MESSAGE
    KEY_MOVE = curses.KEY_MOVE
    KEY_NEXT = curses.KEY_NEXT
    KEY_OPEN = curses.KEY_OPEN
    KEY_OPTIONS = curses.KEY_OPTIONS
    KEY_PREVIOUS = curses.KEY_PREVIOUS
    KEY_REDO = curses.KEY_REDO
    KEY_REFERENCE = curses.KEY_REFERENCE
    KEY_REFRESH = curses.KEY_REFRESH
    KEY_REPLACE = curses.KEY_REPLACE
    KEY_RESTART = curses.KEY_RESTART
    KEY_RESUME = curses.KEY_RESUME
    KEY_SAVE = curses.KEY_SAVE
    KEY_SBEG = curses.KEY_SBEG
    KEY_SCANCEL = curses.KEY_SCANCEL
    KEY_SCOMMAND = curses.KEY_SCOMMAND
    KEY_SCOPY = curses.KEY_SCOPY
    KEY_SCREATE = curses.KEY_SCREATE
    KEY_SDC = curses.KEY_SDC
    KEY_SDL = curses.KEY_SDL
    KEY_SELECT = curses.KEY_SELECT
    KEY_SEND = curses.KEY_SEND
    KEY_SEOL = curses.KEY_SEOL
    KEY_SEXIT = curses.KEY_SEXIT
    KEY_SFIND = curses.KEY_SFIND
    KEY_SHELP = curses.KEY_SHELP
    KEY_SHOME = curses.KEY_SHOME
    KEY_SIC = curses.KEY_SIC
    KEY_SLEFT = curses.KEY_SLEFT
    KEY_SMESSAGE = curses.KEY_SMESSAGE
    KEY_SMOVE = curses.KEY_SMOVE
    KEY_SNEXT = curses.KEY_SNEXT
    KEY_SOPTIONS = curses.KEY_SOPTIONS
    KEY_SPREVIOUS = curses.KEY_SPREVIOUS
    KEY_SPRINT = curses.KEY_SPRINT
    KEY_SREDO = curses.KEY_SREDO
    KEY_SREPLACE = curses.KEY_SREPLACE
    KEY_SRIGHT = curses.KEY_SRIGHT
    KEY_SRSUME = curses.KEY_SRSUME
    KEY_SSAVE = curses.KEY_SSAVE
    KEY_SSUSPEND = curses.KEY_SSUSPEND
    KEY_SUNDO = curses.KEY_SUNDO
    KEY_SUSPEND = curses.KEY_SUSPEND
    KEY_UNDO = curses.KEY_UNDO
    KEY_MOUSE = curses.KEY_MOUSE
    KEY_RESIZE = curses.KEY_RESIZE
    KEY_MAX = curses.KEY_MAX

    def KEY_ASCII(key):
        return ord(key)

    def KEY_CTRL_(c):
        return ord(c) - ord('a') + 1


class Message:
    #Common messages
    MSG_CREATE = 0
    MSG_CLOSE = 1

    MSG_CHILDCLOSE = 2

    MSG_SHOW = 100
    MSG_HIDE = 101

    MSG_RESIZE = 200
    MSG_REDRAW = 201

    MSG_GETFOCUS = 300
    MSG_LOSTFOCUS = 301

    #Control  messages
    MSG_COMMAND = 400
    MSG_CHANGED = 401
    MSG_SCOLLBAR = 402
    MSG_CTRLFOCUSED = 403

    #Input message
    #data = Pos
    MSG_LCLICK = 1000
    MSG_LDBLCLICK = 1001
    MSG_LPRESSED = 1002
    MSG_LRELEASED = 1003

    MSG_MCLICK = 1010
    MSG_MDBLCLICK = 1011
    MSG_MPRESSED = 1012
    MSG_MRELEASED = 1013

    MSG_RCLICK = 1020
    MSG_RDBLCLICK = 1021
    MSG_RPRESSED = 1022
    MSG_RRELEASED = 1023

    #data = (prev_pos, pos)
    MSG_DRAG = 1030

    MSG_KEYPRESS = 1100

    #User message
    MSG_USER = 10000

    #Scoll
    #data = offset
    MSG_SCOLL = 1200

    def __init__(self, msg, data):
        self.msg = msg
        self.data = data

    def is_broadcast(self):
        if self.msg >= 1000 and self.msg < Message.MSG_USER:
            return True
        else:
            return False

    def is_mouse_msg(self):
        if self.msg >= 1000 and self.msg < 1100:
            return True

        else:
            return False

    def is_mouse_begin_msg(self):
        if self.is_mouse_msg() \
                and (self.msg - int(self.msg / 10) * 10) != 4:
            return True

        else:
            return False

    def is_user_msg(self):
        if self.msg >= Message.MSG_USER:
            return True

        return False

    def __str__(self):
        return "msg = %d, data = %s"%(self.msg, str(self.data))

class Clipboard:
    buf = ""
    def read():
        try:
            return pyperclip.paste()
        except Exception:
            return str(Clipboard.buf)

    def write(data):
        try:
            pyperclip.copy(str(data))
        except Exception:
            Clipboard.buf = str(data)

        return

class TicketLock:
    def __init__(self):
        self.owner = 0
        self.ticket = 0
        self.lock = _thread.allocate_lock()
        self.ticket_lock = _thread.allocate_lock()

    def acquire(self):
        ticket = self.get_ticket()

        while True:
            self.lock.acquire()
            if self.owner == ticket:
                return
            self.lock.release()

    def release(self):
        self.add_owner()
        self.lock.release()
        return

    def get_ticket(self):
        self.ticket_lock.acquire()
        ret = self.ticket
        self.ticket += 1
        self.ticket_lock.release()
        return ret

    def add_owner(self):
        self.ticket_lock.acquire()
        self.owner += 1
        self.ticket_lock.release()
        return

class Command:
    def __init__(self, cmd):
        self.argv = []
        if isinstance(cmd, str):
            self.__analyse(cmd)

        else:
            for i in cmd:
                self.argv.append(i)

    def __iter__(self):
        class CommandIter:
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

        return CommandIter(self)

    def __analyse(self, cmd):
        quote_flag = False
        backslash_flag = False
        s = ""

        for i in range(0, len(cmd)):
            if backslash_flag:
                s += cmd[i]

            else:
                if cmd[i] == '\\':
                    backslash_flag = True
                    continue

                elif cmd[i] == '\"':
                    quote_flag = not quote_flag

                elif cmd[i] in (' ', '\t') and not quote_flag:
                    self.argv.append(s)
                    s = ""

                else:
                    s += cmd[i]

            backslash_flag = False

        if s != "":
            self.argv.append(s)

        return

    def get_last_str(s):
        ret = ""
        quote_flag = False
        backslash_flag = False

        for c in s:
            if backslash_flag:
                ret += c

            else:
                if c in (' ', '\t'):
                    if quote_flag:
                        ret += c

                    else:
                        ret = ""

                elif c in ('\'', '\"'):
                    quote_flag = not quote_flag
                        
                elif c == '\\':
                    backslash_flag = True
                    continue

                else:
                    ret += c

            backslash_flag = False

        return ret

    def __len__(self):
        return len(self.argv)

    def __getitem__(self, key):
        return self.argv[key]

    def __contains__(self, item):
        return item in self.argv

    def __str__(self):
        ret = ""
        for i in self.argv:
            if ret != "":
                ret += " "

            if ' ' in i or '\t' in i:
                ret += "\"" + i + "\""

            else:
                ret += i

        return ret

class Drawer:
    def __init__(self, frame):
        self.frame = frame

    def rectangle(self, rect, ch, attr):
        for top in range(rect.pos.top, rect.pos.top + rect.size.height):
            self.frame.draw(Pos(top, rect.pos.left), ch[0] * rect.size.width,
                    attr)
