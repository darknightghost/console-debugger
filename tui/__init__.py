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
import log
from common.types import *

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
    @check_arg_type(pos = (Pos, ), size = (Size, ))
    def __init__(self, pos, size):
        self.pos = pos
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
    class Key:
        index_tree = {}
        def __init__(self, *collections, base_key = False):
            lst = []
            for c in collections:
                lst.append(tuple(c))

            self.collection = tuple(lst)
            if base_key == True:
                #Add to index tree
                for k in self.collection:
                    node = __class__.index_tree
                    for n in k:
                        try:
                            node = node[n]

                        except KeyError:
                            node[n] = {}
                            node = node[n]

        def __eq__(self, val):
            if not isinstance(val, Keyboard.Key):
                raise TypeError()

            for k in val.collection:
                if k in self.collection:
                    return True

            for k in self.collection:
                if k in val.collection:
                    return True

            return False

        def __str__(self):
            return str(self.collection)

        def get_wch(self):
            seq = []
            for t in self.collection[0]:
                if t < 256:
                    seq.append(t)

            return bytes(seq).decode(errors = 'ignore')

        def is_ctrl_key(self):
            for k in self.collection:
                if len(k) == 1:
                    if k[0] in range(1, 27):
                        return True

            return False

        def is_function_key(self):
            for k in self.collection:
                if len(k) == 1:
                    if k[0] in range(curses.KEY_F0, curses.KEY_F63 + 1):
                        return True

            return False

        def key_len(buff):
            i = 0
            node = __class__.index_tree
            while i < len(buff):
                try:
                    node = node[i]

                except KeyError:
                    return 1

                i += 1

            return i

        def get_sequence(self):
            return bytes(self.collection[0])

    KEY_INTERRUPT = Key((-1, ), base_key = True)

    KEY_NULL = Key((0, ), base_key = True)
    KEY_SOH = Key((1, ), base_key = True)
    KEY_STX = Key((2, ), base_key = True)
    KEY_ETX = Key((3, ), base_key = True)
    KEY_EOT = Key((4, ), base_key = True)
    KEY_ENQ = Key((5, ), base_key = True)
    KEY_ACK = Key((6, ), base_key = True)
    KEY_BEL = Key((7, ), base_key = True)
    KEY_BS = Key((8, ), base_key = True)
    KEY_HT = Key((9, ), base_key = True)
    KEY_LF = Key((10, ), base_key = True)
    KEY_VT = Key((11, ), base_key = True)
    KEY_FF = Key((12, ), base_key = True)
    KEY_CR = Key((13, ), base_key = True)
    KEY_SO = Key((14, ), base_key = True)
    KEY_SI = Key((15, ), base_key = True)
    KEY_DLE = Key((16, ), base_key = True)
    KEY_DC1 = Key((17, ), base_key = True)
    KEY_DC2 = Key((18, ), base_key = True)
    KEY_DC3 = Key((19, ), base_key = True)
    KEY_DC4 = Key((20, ), base_key = True)
    KEY_NAK = Key((21, ), base_key = True)
    KEY_SYN = Key((22, ), base_key = True)
    KEY_ETB = Key((23, ), base_key = True)
    KEY_CAN = Key((24, ), base_key = True)
    KEY_EM = Key((25, ), base_key = True)
    KEY_SUB = Key((26, ), base_key = True)
    KEY_ESC = Key((27, ), base_key = True)
    KEY_FS = Key((28, ), base_key = True)
    KEY_GS = Key((29, ), base_key = True)
    KEY_RS = Key((30, ), base_key = True)
    KEY_US = Key((31, ), base_key = True)

    KEY_DEL = Key((127, ), base_key = True)

    KEY_BREAK = Key((curses.KEY_BREAK, ), base_key = True)
    KEY_MIN = Key((curses.KEY_MIN, ), base_key = True)
    KEY_DOWN = Key((curses.KEY_DOWN, ), base_key = True)
    KEY_UP = Key((curses.KEY_UP, ), base_key = True)
    KEY_LEFT = Key((curses.KEY_LEFT, ), base_key = True)
    KEY_RIGHT = Key((curses.KEY_RIGHT, ), base_key = True)
    KEY_HOME = Key((curses.KEY_HOME, ), (27, 91, 49, 126), base_key = True,)
    KEY_BACKSPACE = Key((curses.KEY_BACKSPACE, ), base_key = True)
    KEY_F0 = Key((curses.KEY_F0, ), base_key = True)
    KEY_F1 = Key((curses.KEY_F1, ), base_key = True)
    KEY_F2 = Key((curses.KEY_F2, ), base_key = True)
    KEY_F3 = Key((curses.KEY_F3, ), base_key = True)
    KEY_F4 = Key((curses.KEY_F4, ), base_key = True)
    KEY_F5 = Key((curses.KEY_F5, ), base_key = True)
    KEY_F6 = Key((curses.KEY_F6, ), base_key = True)
    KEY_F7 = Key((curses.KEY_F7, ), base_key = True)
    KEY_F8 = Key((curses.KEY_F8, ), base_key = True)
    KEY_F9 = Key((curses.KEY_F9, ), base_key = True)
    KEY_F10 = Key((curses.KEY_F10, ), base_key = True)
    KEY_F11 = Key((curses.KEY_F11, ), base_key = True)
    KEY_F12 = Key((curses.KEY_F12, ), base_key = True)
    KEY_F13 = Key((curses.KEY_F13, ), base_key = True)
    KEY_F14 = Key((curses.KEY_F14, ), base_key = True)
    KEY_F15 = Key((curses.KEY_F15, ), base_key = True)
    KEY_F16 = Key((curses.KEY_F16, ), base_key = True)
    KEY_F17 = Key((curses.KEY_F17, ), base_key = True)
    KEY_F18 = Key((curses.KEY_F18, ), base_key = True)
    KEY_F19 = Key((curses.KEY_F19, ), base_key = True)
    KEY_F20 = Key((curses.KEY_F20, ), base_key = True)
    KEY_F21 = Key((curses.KEY_F21, ), base_key = True)
    KEY_F22 = Key((curses.KEY_F22, ), base_key = True)
    KEY_F23 = Key((curses.KEY_F23, ), base_key = True)
    KEY_F24 = Key((curses.KEY_F24, ), base_key = True)
    KEY_F25 = Key((curses.KEY_F25, ), base_key = True)
    KEY_F26 = Key((curses.KEY_F26, ), base_key = True)
    KEY_F27 = Key((curses.KEY_F27, ), base_key = True)
    KEY_F28 = Key((curses.KEY_F28, ), base_key = True)
    KEY_F29 = Key((curses.KEY_F29, ), base_key = True)
    KEY_F30 = Key((curses.KEY_F30, ), base_key = True)
    KEY_F31 = Key((curses.KEY_F31, ), base_key = True)
    KEY_F32 = Key((curses.KEY_F32, ), base_key = True)
    KEY_F33 = Key((curses.KEY_F33, ), base_key = True)
    KEY_F34 = Key((curses.KEY_F34, ), base_key = True)
    KEY_F35 = Key((curses.KEY_F35, ), base_key = True)
    KEY_F36 = Key((curses.KEY_F36, ), base_key = True)
    KEY_F37 = Key((curses.KEY_F37, ), base_key = True)
    KEY_F38 = Key((curses.KEY_F38, ), base_key = True)
    KEY_F39 = Key((curses.KEY_F39, ), base_key = True)
    KEY_F40 = Key((curses.KEY_F40, ), base_key = True)
    KEY_F41 = Key((curses.KEY_F41, ), base_key = True)
    KEY_F42 = Key((curses.KEY_F42, ), base_key = True)
    KEY_F43 = Key((curses.KEY_F43, ), base_key = True)
    KEY_F44 = Key((curses.KEY_F44, ), base_key = True)
    KEY_F45 = Key((curses.KEY_F45, ), base_key = True)
    KEY_F46 = Key((curses.KEY_F46, ), base_key = True)
    KEY_F47 = Key((curses.KEY_F47, ), base_key = True)
    KEY_F48 = Key((curses.KEY_F48, ), base_key = True)
    KEY_F49 = Key((curses.KEY_F49, ), base_key = True)
    KEY_F50 = Key((curses.KEY_F50, ), base_key = True)
    KEY_F51 = Key((curses.KEY_F51, ), base_key = True)
    KEY_F52 = Key((curses.KEY_F52, ), base_key = True)
    KEY_F53 = Key((curses.KEY_F53, ), base_key = True)
    KEY_F54 = Key((curses.KEY_F54, ), base_key = True)
    KEY_F55 = Key((curses.KEY_F55, ), base_key = True)
    KEY_F56 = Key((curses.KEY_F56, ), base_key = True)
    KEY_F57 = Key((curses.KEY_F57, ), base_key = True)
    KEY_F58 = Key((curses.KEY_F58, ), base_key = True)
    KEY_F59 = Key((curses.KEY_F59, ), base_key = True)
    KEY_F60 = Key((curses.KEY_F60, ), base_key = True)
    KEY_F61 = Key((curses.KEY_F61, ), base_key = True)
    KEY_F62 = Key((curses.KEY_F62, ), base_key = True)
    KEY_F63 = Key((curses.KEY_F63, ), base_key = True)
    KEY_DL = Key((curses.KEY_DL, ), base_key = True)
    KEY_IL = Key((curses.KEY_IL, ), base_key = True)
    KEY_DC = Key((curses.KEY_DC, ), base_key = True)
    KEY_IC = Key((curses.KEY_IC, ), base_key = True)
    KEY_EIC = Key((curses.KEY_EIC, ), base_key = True)
    KEY_CLEAR = Key((curses.KEY_CLEAR, ), base_key = True)
    KEY_EOS = Key((curses.KEY_EOS, ), base_key = True)
    KEY_EOL = Key((curses.KEY_EOL, ), base_key = True)
    KEY_SF = Key((curses.KEY_SF, ), base_key = True)
    KEY_SR = Key((curses.KEY_SR, ), base_key = True)
    KEY_NPAGE = Key((curses.KEY_NPAGE, ), base_key = True)
    KEY_PPAGE = Key((curses.KEY_PPAGE, ), base_key = True)
    KEY_STAB = Key((curses.KEY_STAB, ), base_key = True)
    KEY_CTAB = Key((curses.KEY_CTAB, ), base_key = True)
    KEY_CATAB = Key((curses.KEY_CATAB, ), base_key = True)
    KEY_ENTER = Key((curses.KEY_ENTER, ), base_key = True)
    KEY_SRESET = Key((curses.KEY_SRESET, ), base_key = True)
    KEY_RESET = Key((curses.KEY_RESET, ), base_key = True)
    KEY_PRINT = Key((curses.KEY_PRINT, ), base_key = True)
    KEY_LL = Key((curses.KEY_LL, ), base_key = True)
    KEY_A1 = Key((curses.KEY_A1, ), base_key = True)
    KEY_A3 = Key((curses.KEY_A3, ), base_key = True)
    KEY_B2 = Key((curses.KEY_B2, ), base_key = True)
    KEY_C1 = Key((curses.KEY_C1, ), base_key = True)
    KEY_C3 = Key((curses.KEY_C3, ), base_key = True)
    KEY_BTAB = Key((curses.KEY_BTAB, ), base_key = True)
    KEY_BEG = Key((curses.KEY_BEG, ), base_key = True)
    KEY_CANCEL = Key((curses.KEY_CANCEL, ), base_key = True)
    KEY_CLOSE = Key((curses.KEY_CLOSE, ), base_key = True)
    KEY_COMMAND = Key((curses.KEY_COMMAND, ), base_key = True)
    KEY_COPY = Key((curses.KEY_COPY, ), base_key = True)
    KEY_CREATE = Key((curses.KEY_CREATE, ), base_key = True)
    KEY_END = Key((curses.KEY_END, ), (27, 91, 52, 126), base_key = True)
    KEY_EXIT = Key((curses.KEY_EXIT, ), base_key = True)
    KEY_FIND = Key((curses.KEY_FIND, ), base_key = True)
    KEY_HELP = Key((curses.KEY_HELP, ), base_key = True)
    KEY_MARK = Key((curses.KEY_MARK, ), base_key = True)
    KEY_MESSAGE = Key((curses.KEY_MESSAGE, ), base_key = True)
    KEY_MOVE = Key((curses.KEY_MOVE, ), base_key = True)
    KEY_NEXT = Key((curses.KEY_NEXT, ), base_key = True)
    KEY_OPEN = Key((curses.KEY_OPEN, ), base_key = True)
    KEY_OPTIONS = Key((curses.KEY_OPTIONS, ), base_key = True)
    KEY_PREVIOUS = Key((curses.KEY_PREVIOUS, ), base_key = True)
    KEY_REDO = Key((curses.KEY_REDO, ), base_key = True)
    KEY_REFERENCE = Key((curses.KEY_REFERENCE, ), base_key = True)
    KEY_REFRESH = Key((curses.KEY_REFRESH, ), base_key = True)
    KEY_REPLACE = Key((curses.KEY_REPLACE, ), base_key = True)
    KEY_RESTART = Key((curses.KEY_RESTART, ), base_key = True)
    KEY_RESUME = Key((curses.KEY_RESUME, ), base_key = True)
    KEY_SAVE = Key((curses.KEY_SAVE, ), base_key = True)
    KEY_SBEG = Key((curses.KEY_SBEG, ), base_key = True)
    KEY_SCANCEL = Key((curses.KEY_SCANCEL, ), base_key = True)
    KEY_SCOMMAND = Key((curses.KEY_SCOMMAND, ), base_key = True)
    KEY_SCOPY = Key((curses.KEY_SCOPY, ), base_key = True)
    KEY_SCREATE = Key((curses.KEY_SCREATE, ), base_key = True)
    KEY_SDC = Key((curses.KEY_SDC, ), base_key = True)
    KEY_SDL = Key((curses.KEY_SDL, ), base_key = True)
    KEY_SELECT = Key((curses.KEY_SELECT, ), base_key = True)
    KEY_SEND = Key((curses.KEY_SEND, ), base_key = True)
    KEY_SEOL = Key((curses.KEY_SEOL, ), base_key = True)
    KEY_SEXIT = Key((curses.KEY_SEXIT, ), base_key = True)
    KEY_SFIND = Key((curses.KEY_SFIND, ), base_key = True)
    KEY_SHELP = Key((curses.KEY_SHELP, ), base_key = True)
    KEY_SHOME = Key((curses.KEY_SHOME, ), base_key = True)
    KEY_SIC = Key((curses.KEY_SIC, ), base_key = True)
    KEY_SLEFT = Key((curses.KEY_SLEFT, ), base_key = True)
    KEY_SMESSAGE = Key((curses.KEY_SMESSAGE, ), base_key = True)
    KEY_SMOVE = Key((curses.KEY_SMOVE, ), base_key = True)
    KEY_SNEXT = Key((curses.KEY_SNEXT, ), base_key = True)
    KEY_SOPTIONS = Key((curses.KEY_SOPTIONS, ), base_key = True)
    KEY_SPREVIOUS = Key((curses.KEY_SPREVIOUS, ), base_key = True)
    KEY_SPRINT = Key((curses.KEY_SPRINT, ), base_key = True)
    KEY_SREDO = Key((curses.KEY_SREDO, ), base_key = True)
    KEY_SREPLACE = Key((curses.KEY_SREPLACE, ), base_key = True)
    KEY_SRIGHT = Key((curses.KEY_SRIGHT, ), base_key = True)
    KEY_SRSUME = Key((curses.KEY_SRSUME, ), base_key = True)
    KEY_SSAVE = Key((curses.KEY_SSAVE, ), base_key = True)
    KEY_SSUSPEND = Key((curses.KEY_SSUSPEND, ), base_key = True)
    KEY_SUNDO = Key((curses.KEY_SUNDO, ), base_key = True)
    KEY_SUSPEND = Key((curses.KEY_SUSPEND, ), base_key = True)
    KEY_UNDO = Key((curses.KEY_UNDO, ), base_key = True)
    KEY_MOUSE = Key((curses.KEY_MOUSE, ), base_key = True)
    KEY_RESIZE = Key((curses.KEY_RESIZE, ), base_key = True)

    KEY_MAX = Key((curses.KEY_MAX, ), base_key = True)

    def KEY_ASCII(key):
        return Keyboard.Key((ord(key), ))

    def KEY_CTRL_(c):
        return Keyboard.Key((ord(c) - ord('a') + 1, ))


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

    #Control messages
    #data = control
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

    #data = (prev_pos, pos, first_pos)
    MSG_DRAG = 1030

    #data = key
    MSG_KEYPRESS = 1100

    #Scoll
    #data = offset
    MSG_SCOLL = 1200

    #User message
    MSG_USER = 20000

    def __init__(self, msg, data):
        self.msg = msg
        self.data = data

    def is_broadcast(self):
        if self.msg >= 1000 and self.msg < Message.MSG_USER:
            return True
        else:
            return False

    def is_control_msg(self):
        if self.msg >= 400 and self.msg < 1000:
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
        if self.lock.locked():
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

    @check_arg_type(rect = (Rect, ), ch = (str, ))
    def rectangle(self, rect, ch, attr):
        for top in range(rect.pos.top, rect.pos.top + rect.size.height):
            self.frame.draw(Pos(top, rect.pos.left), ch[0] * rect.size.width,
                    attr)

class String:
    def __char_width(o):
        o = ord(o)
        widths = [
            (126,  1), (159,  0), (687,   1), (710,  0), (711,  1),
            (727,  0), (733,  1), (879,   0), (1154, 1), (1161, 0),
            (4347,  1), (4447,  2), (7467,  1), (7521, 0), (8369, 1),
            (8426,  0), (9000,  1), (9002,  2), (11021, 1), (12350, 2),
            (12351, 1), (12438, 2), (12442,  0), (19893, 2), (19967, 1),
            (55203, 2), (63743, 1), (64106,  2), (65039, 1), (65059, 0),
            (65131, 2), (65279, 1), (65376,  2), (65500, 1), (65510, 2),
            (120831, 1), (262141, 2), (1114109, 1)]
        if o == 0xe or o == 0xf:
            return 0
        for num, wid in widths:
            if o <= num:
                return wid
        return 1

    @check_arg_type(string = (str, ))
    def width(string):
                
        ret = 0
        for o in string:
            ret += String.__char_width(o)
            
        return ret

    @check_arg_type(string = (str, ), width = (int, ), begin = (int, ))
    def width_split(string, width, begin = 0):
        ret = ""
        w = 0

        for i in range(begin, len(string)):
            w += String.__char_width(string[i])
            if w > width:
                break

            ret += string[i]

        return ret

    @check_arg_type(string = (str, ), width = (int, ), begin = (int, ))
    def width_to_len(string, begin, width):
        index = begin
        total = len(string)
        w = 0

        while index < total:
            w = w + String.__char_width(string[index])
            if w > width:
                return index - begin

            index += 1

        return total - begin

    @check_arg_type(string = (str, ), width = (int, ), begin = (int, ))
    def rwidth_to_len(string, begin, width):
        index = begin
        total = len(string)
        w = 0

        while index > 0:
            w = w + String.__char_width(string[index])
            if w > width:
                return begin - index

            index -= 1

        return begin
