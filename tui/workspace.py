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
import threading
import datetime
import time
import _thread
import log

from tui import *
from tui.tagsview import *
from tui.popup import *

class Workspace:
    COMMAND_MODE = 0
    EDIT_MODE = 1

    BTN_L_PRESSED = 0
    BTN_L_RELEASED = 1
    BTN_M_PRESSED = 2
    BTN_M_RELEASED = 3
    BTN_R_PRESSED = 4
    BTN_R_RELEASED = 5
    
    def __new__(cls, *args, **kwargs):
        if "_instance" not in Workspace.__dict__:
            Workspace._instance = object.__new__(cls)
            cls.initialized = False

        return Workspace._instance

    def __is_btn_l(btn):
        return btn in (Workspace.BTN_L_PRESSED, Workspace.BTN_L_RELEASED)

    def __is_btn_m(btn):
        return btn in (Workspace.BTN_M_PRESSED, Workspace.BTN_M_RELEASED)

    def __is_btn_r(btn):
        return btn in (Workspace.BTN_R_PRESSED, Workspace.BTN_R_RELEASED)

    def is_same_btn(btn1,  btn2):
        if (Workspace.__is_btn_l(btn1) and Workspace.__is_btn_l(btn2)) \
                or (Workspace.__is_btn_m(btn1) and Workspace.__is_btn_m(btn2)) \
                or (Workspace.__is_btn_r(btn1) and Workspace.__is_btn_r(btn2)):
            return True

        else:
            return False

    def __is_btn_press(btn):
        return btn in (Workspace.BTN_L_PRESSED, Workspace.BTN_M_PRESSED,
                Workspace.BTN_R_PRESSED)

    def __is_btn_release(btn):
        return btn in (Workspace.BTN_L_RELEASED, Workspace.BTN_M_RELEASED,
                Workspace.BTN_R_RELEASED)

    def trans_btn_click_message(self, btn):
        ret = 0
        if Workspace.__is_btn_l(btn):
            ret = Message.MSG_LCLICK

        elif Workspace.__is_btn_m(btn):
            ret = Message.MSG_MCLICK

        elif Workspace.__is_btn_r(btn):
            ret = Message.MSG_RCLICK

        if self.click_count > 1:
            ret += 1

        self.click_count = 0

        return ret

    def trans_btn_press_messgae(self, btn):
        ret = 0

        if Workspace.__is_btn_l(btn):
            ret = Message.MSG_LCLICK

        elif Workspace.__is_btn_m(btn):
            ret = Message.MSG_MCLICK

        elif Workspace.__is_btn_r(btn):
            ret = Message.MSG_RCLICK

        if Workspace.__is_btn_press(btn):
            ret += 2

        elif Workspace.__is_btn_release(btn):
            ret += 3

        return ret

    def __init__(self, max_history = 256):
        if type(self).initialized:
            return

        else:
            type(self).initialized = True

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
        self.mouse_interval = 1 / 4
        self.prev_btn = None
        self.current_btn = None
        self.current_pos = Pos(0, 0)
        self.prev_pos = Pos(0, 0)
        self.click_count = 0
        self.clicktime = 0.0
        self.inputlock = TicketLock()
        self.cmd_dict = {}
        self.shotcutkey_dict = {}

        return

    def winmain(self):
        try:
            #Begin TUI
            self.stdscr = curses.initscr()

            wnd_size = self.stdscr.getmaxyx()
            self.size = Size(wnd_size[1], wnd_size[0])
            self.client_size = Size(self.size.width, self.size.height - 1)

            curses.noecho()
            curses.cbreak()
            self.stdscr.keypad(1)

            #Enable mouse
            curses.mouseinterval(0)
            self.old_mask = curses.mousemask(curses.ALL_MOUSE_EVENTS \
                    | curses.REPORT_MOUSE_POSITION)[1]

            #Color
            Color.init_color()

            #Background
            self.stdscr.bkgd(' ', Color.get_color(Color.WHITE,Color.BLACK))
            curses.curs_set(0)
            self.cmdline_refresh()

            #Main view
            main_view = self.create_init_view()
            self.focused_view = main_view
            main_view.dispatch_msg(Message(Message.MSG_CREATE, None))
            main_view.redraw()
            main_view.set_focus(True)
            main_view.update()

            self.on_create()
            
            self.update()

            #Input loop
            self.input_loop()

        finally:
            #End GUI
            curses.mousemask(self.old_mask)
            self.stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            sys.stdin.flush()

        return self.exit_code

    def show_text(self, txt):
        #Clear screen
        curses.mousemask(self.old_mask)
        self.stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        sys.stdin.flush()

        #Show text
        print(txt)
        input("\nPress <Enter> to continue...")

        #Redraw
        self.stdscr = curses.initscr()

        wnd_size = self.stdscr.getmaxyx()
        self.size = Size(wnd_size[1], wnd_size[0])
        self.client_size = Size(self.size.width, self.size.height - 1)

        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        self.stdscr.nodelay(0)

        #Enable mouse
        curses.mouseinterval(0)
        curses.mousemask(curses.ALL_MOUSE_EVENTS \
                | curses.REPORT_MOUSE_POSITION)[1]

        #Color
        Color.init_color()

        #Background
        self.stdscr.bkgd(' ', Color.get_color(Color.WHITE,Color.BLACK))
        curses.curs_set(0)
        self.cmdline_refresh()
        self.redraw()
        self.update()

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
                key = self.get_input()
                self.inputlock.acquire()
                try:
                    self.dispatch_input(key[0], key[1])
                finally:
                    self.inputlock.release()

            except curses.error:
                continue

        return

    def get_input(self):
        try:
            key = self.stdscr.get_wch()
            if isinstance(key, str):
                key = list(key.encode(errors = "ignore"))

            elif isinstance(key, int):
                key = [key]

            self.stdscr.nodelay(1)
            while True:
                ch = self.stdscr.getch()
                if ch == -1:
                    break

                key.append(ch)

            self.stdscr.nodelay(0)

            if key[0] == curses.KEY_MOUSE:
                return (Keyboard.Key(key), curses.getmouse())

            else:
                return (Keyboard.Key(key), None)

        except KeyboardInterrupt:
            key = list(b'\x03')
            return (Keyboard.Key(key), None)

    def dispatch_input(self, key, mouse):
        if (key.is_ctrl_key() and key != Keyboard.KEY_LF \
                or key.is_function_key()) \
                and key != Keyboard.KEY_HT:
            #Shotcut key
            self.dispatch_shotcut_key(key)

        elif key == Keyboard.KEY_RESIZE:
            wnd_size = self.stdscr.getmaxyx()
            self.resize(Size(wnd_size[1], wnd_size[0]))

        elif key == Keyboard.KEY_ESC:
            if self.mode != self.COMMAND_MODE:
                self.mode = self.COMMAND_MODE
            else:
                self.mode = self.EDIT_MODE
            self.cmdline_refresh()

        elif key == Keyboard.KEY_MOUSE:
            self.dispatch_mouse(key, mouse)

        else:
            if self.mode == self.COMMAND_MODE:
                #Command mode
                self.get_command(key)

            else:
                #Edit mode
                if self.focused_view != None:
                    self.focused_view.dispatch_msg(Message(Message.MSG_KEYPRESS,
                        key))
        return

    def get_command(self, key):
        if key == Keyboard.KEY_LF:
            #Enter
            if self.command_buf == "":
                if len(self.history) > 0:
                    self.command_buf = self.history[-1]

                else:
                    return

            self.add_history()
            stat = self.on_command(Command(self.command_buf))
            self.command_buf = ""
            self.command_curser = 0
            self.cmd_show_begin = 0

            if stat != None:
                self.print_stat(stat)
                return

        elif key in (Keyboard.KEY_DEL, Keyboard.KEY_BACKSPACE):
            #Backspace
            if self.command_curser > 0:
                self.command_buf = self.command_buf[: self.command_curser - 1] \
                        + self.command_buf[self.command_curser :]
                self.command_curser = self.command_curser - 1
                if self.cmd_show_begin > 0:
                    self.cmd_show_begin = self.cmd_show_begin - 1

        elif key == Keyboard.KEY_DC:
            #Delete
            if self.command_curser < len(self.command_buf):
                self.command_buf = self.command_buf[: self.command_curser] \
                        + self.command_buf[self.command_curser + 1 :]
                if self.cmd_show_begin > 0 \
                        and self.command_curser < self.cmd_show_begin:
                    self.cmd_show_begin = self.command_curser

        elif key == Keyboard.KEY_UP:
            #Up
            s = self.prev_history()
            if s != None:
                self.command_buf = s
            self.command_curser = len(self.command_buf)

        elif key == Keyboard.KEY_DOWN:
            #Down
            s = self.next_history()
            if s != None:
                self.command_buf = s
            self.command_curser = len(self.command_buf)

        elif key == Keyboard.KEY_LEFT:
            #Left
            if self.command_curser > 0:
                self.command_curser = self.command_curser - 1
                
                if self.command_curser < self.cmd_show_begin:
                    self.cmd_show_begin = self.command_curser

        elif key == Keyboard.KEY_RIGHT:
            #Right
            if self.command_curser < len(self.command_buf):
                self.command_curser = self.command_curser + 1

                if self.command_curser - self.cmd_show_begin + 2 \
                        > self.size.width:
                    self.cmd_show_begin = self.command_curser - self.size.width + 2

        elif key == Keyboard.KEY_HOME:
            #Home
            self.command_curser = 0
            self.cmd_show_begin = 0

        elif key == Keyboard.KEY_END:
            #End
            self.command_curser = len(self.command_buf)
            if self.command_curser - self.cmd_show_begin \
                    > self.size.width:
                self.cmd_show_begin = self.command_curser - self.size.width + 2

        elif key == Keyboard.KEY_HT:
            #Tab
            #Auto-complete
            try:
                comp_str = self.command_buf[: self.command_curser]

            except IndexError:
                comp_str = self.command_buf[: self.command_curser - 1]

            comp_cmds = Command(comp_str)

            do_cmd_complete = False
            if len(comp_cmds) == 0:
                do_cmd_complete = True

            elif len(comp_cmds) == 1:
                if Command.get_last_str(comp_str) == comp_cmds[0]:
                    do_cmd_complete = True

            complete_lst = []
            if do_cmd_complete:
                #Complete command
                for c in self.cmd_dict:
                    if c[: len(comp_str)] == comp_str.strip():
                        complete_lst.append(c)

                complete_lst.sort()

            else:
                #Complete arguments
                try:
                    hndlr = self.cmd_dict[comp_cmds[0]][1]

                except KeyError:
                    hndlr = None

                if hndlr != None:
                    complete_lst = hndlr(comp_str)

                complete_lst.sort()

            if len(complete_lst) > 0:
                comp_index = self.popup(complete_lst, Pos(self.size.height - 1,
                    self.command_curser))

                if comp_index != None:
                    fill_str = complete_lst[comp_index]

                    #Remove inputed charachers
                    remove_str = Command.get_last_str(comp_str)

                    fill_str = fill_str[len(remove_str) :]

                    #Insert string
                    self.command_buf = self.command_buf[: self.command_curser] \
                            + fill_str \
                            + self.command_buf[self.command_curser :]
                    self.command_curser += len(fill_str)

        else:
            self.command_buf = self.command_buf[: self.command_curser] \
                    + key.get_wch() \
                    + self.command_buf[self.command_curser :]
            self.command_curser = self.command_curser + len(key.get_wch())

            print_width = String.width(self.command_buf[self.cmd_show_begin : self.command_curser + 1])
            if self.command_curser == len(self.command_buf):
                print_width += 1

            if  print_width > self.size.width:
                if self.command_curser == len(self.command_buf):
                    self.cmd_show_begin = len(self.command_buf) \
                        - String.rwidth_to_len(self.command_buf,
                            self.command_curser - 1,
                            self.size.width - 1)

                else:
                    self.cmd_show_begin = len(self.command_buf[: self.command_curser + 1]) \
                        - String.rwidth_to_len(self.command_buf,
                            self.command_curser,
                            self.size.width)

        self.cmdline_refresh()

        return
        
    def add_history(self):
        try:
            if self.command_buf == "" or self.command_buf == self.history[-1]:
                return

        except IndexError:
            pass

        self.history.append(self.command_buf)
        if len(self.history) > self.max_history:
            self.history = self.history[len(self.history) - self.max_history :]
        self.current_history = len(self.history)

    def prev_history(self):
        if self.current_history <= 0:
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
        try:
            self.stdscr.addstr(self.size.height - 1, 0, " " * (self.size.width - 1), 
                    attr);
            self.stdscr.addnstr(self.size.height - 1, 0, info, self.size.width - 1,
                    attr);

        except Exception:
            pass

    def cmdline_refresh(self):
        #Draw command line
        attr = Color.get_color(Color.WHITE, Color.BLACK) | curses.A_BOLD

        try:
            self.stdscr.addstr(self.size.height - 1, 0, 
                    ' ' * (self.size.width), attr)

        except Exception:
            pass

        string = String.width_split(self.command_buf, self.size.width, 
                begin = self.cmd_show_begin)

        for i in range(0, len(string)):
            attr = Color.get_color(Color.WHITE, Color.BLACK)
            if i + self.cmd_show_begin \
                    == self.command_curser and self.mode == self.COMMAND_MODE:
                attr = attr | curses.A_REVERSE | curses.A_BOLD 

            else:
                attr = attr | curses.A_BOLD

            c = string[i]
            try:
                self.stdscr.addstr(self.size.height - 1, String.width(string[: i]),
                        c, attr)

            except Exception:
                pass

        if self.command_curser == len(self.command_buf):
            attr = Color.get_color(Color.WHITE, Color.BLACK) | curses.A_BOLD | curses.A_REVERSE
            try:
                self.stdscr.addstr(self.size.height - 1, String.width(string),
                        ' ', attr)

            except Exception:
                pass

        self.update()

        return

    def resize(self, size):
        old_size = self.size
        self.size = size
        self.client_size = Size(self.size.width, self.size.height - 1)
        self.stdscr.erase()
        self.cmdline_refresh()

        x_rate = size.width / old_size.width
        y_rate = size.height / old_size.height

        #Resize child views
        for v in self.views:
            if v.rect.pos.left == 0:
                v.workspace_w_resize(0, x_rate)

            if v.rect.pos.top == 0:
                v.workspace_h_resize(0, y_rate)

        for v in self.views:
            v.resize(v.rect)
            v.redraw()

        self.update()
        return

    def redraw(self):
        for v in self.views:
            v.redraw()

        self.cmdline_refresh()

    def draw(self, pos, string, attr):
        try:
            if len(string) + pos.left > self.size.width:
                string = string[: self.size.width - pos.left]

            self.stdscr.addstr(pos.top, pos.left, string, attr)
        except Exception:
            pass
        return

    def add_child(self, child):
        self.views.append(child)

    def switch_focused(self, view):
        view.set_focus(True)

    def remove_child(self, child):
        self.views.remove(child)

    def on_command(self, command):
        try:
            return self.cmd_dict[command[0]][0](command)

        except KeyError:
            return "Unknow command."

    def reg_command(self, cmd, hndlr, autocompile):
        if cmd in self.cmd_dict:
            return False

        else:
            self.cmd_dict[cmd] = (hndlr, autocompile)
            return True
        
    def unreg_command(self, cmd):
        self.cmd_dict.pop(cmd)

    def on_create(self):
        raise NotImplementedError() 

    def dispatch_shotcut_key(self, key):
        if key == Keyboard.KEY_CTRL_("w"):
            #Tab view control
            while True:
                key = self.get_input()[0]

                if key in (Keyboard.KEY_UP, Keyboard.KEY_ASCII("k")):
                    next_view = self.focused_view.next_view(TagsView.TOP)
                    if next_view != None:
                        self.switch_focused(next_view)

                elif key in (Keyboard.KEY_DOWN, Keyboard.KEY_ASCII("j")):
                    next_view = self.focused_view.next_view(TagsView.BOTTOM)
                    if next_view != None:
                        self.switch_focused(next_view)

                elif key in (Keyboard.KEY_LEFT, Keyboard.KEY_ASCII("h")):
                    next_view = self.focused_view.next_view(TagsView.LEFT)
                    if next_view != None:
                        self.switch_focused(next_view)

                elif key in (Keyboard.KEY_RIGHT, Keyboard.KEY_ASCII("l")):
                    next_view = self.focused_view.next_view(TagsView.RIGHT)
                    if next_view != None:
                        self.switch_focused(next_view)

                elif key == Keyboard.KEY_ASCII("="):
                    self.focused_view.change_height(1)

                elif key == Keyboard.KEY_ASCII("-"):
                    self.focused_view.change_height(-1)

                elif key == Keyboard.KEY_ASCII("."):
                    self.focused_view.change_width(1)

                elif key == Keyboard.KEY_ASCII(","):
                    self.focused_view.change_width(-1)

                elif key == Keyboard.KEY_ESC:
                    break

        else:
            self.on_shotcut_key(key)

        return

    def on_shotcut_key(self, key):
        try:
            self.shotcutkey_dict[key[0]](key)

        except KeyError:
            pass

    def reg_shotcut_key(self, key, hndlr):
        if key in self.shotcutkey_dict:
            return False
        else:
            self.shotcutkey_dict[key] = hndlr
            return True

    def reg_shotcut_key(self, key):
        self.shotcutkey_dict.pop(key)

    def create_init_view(self):
        raise NotImplementedError() 

    def set_current_btn(self, btn, pos):
        self.clicktime = time.time()
        self.prev_btn = self.current_btn
        self.current_btn = btn
        self.prev_pos = self.current_pos
        self.current_pos = pos

        if btn == None and self.prev_btn != None:
            if self.click_count > 0:
                msg = Message(self.trans_btn_click_message(self.prev_btn),
                    Pos(self.prev_pos.top - self.focused_view.rect.pos.top,
                        self.prev_pos.left - self.focused_view.rect.pos.left))
                self.focused_view.dispatch_msg(msg)

            elif Workspace.__is_btn_press(self.prev_btn):
                msg = Message(self.trans_btn_press_messgae(self.prev_btn),
                    Pos(self.prev_pos.top - self.focused_view.rect.pos.top,
                        self.prev_pos.left - self.focused_view.rect.pos.left))
                self.focused_view.dispatch_msg(msg)

        elif Workspace.__is_btn_release(btn) and Workspace.__is_btn_press(self.prev_btn) \
                and Workspace.is_same_btn(btn, self.prev_btn):
            self.click_count += 1

        return

    def dispatch_mouse(self, key, mouse):
        if mouse[4] == curses.BUTTON1_PRESSED:
            #Left button pressed
            self.awake_view_by_pos(Pos(mouse[2], mouse[1]))
            self.drag_begin = Pos(mouse[2], mouse[1])
            self.set_current_btn(Workspace.BTN_L_PRESSED, Pos(mouse[2], mouse[1]))
            t = threading.Timer(self.mouse_interval, self.mouse_alam, (None,))
            t.start()

        elif mouse[4] == curses.BUTTON1_RELEASED:
            #Left button released
            self.set_current_btn(Workspace.BTN_L_RELEASED, Pos(mouse[2], mouse[1]))
            t = threading.Timer(self.mouse_interval, self.mouse_alam, (None,))
            t.start()

        elif mouse[4] == curses.BUTTON2_PRESSED:
            #Mid button pressed
            self.awake_view_by_pos(Pos(mouse[2], mouse[1]))
            self.drag_begin = Pos(mouse[2], mouse[1])
            self.set_current_btn(Workspace.BTN_M_PRESSED, Pos(mouse[2], mouse[1]))
            t = threading.Timer(self.mouse_interval, self.mouse_alam, (None,))
            t.start()

        elif mouse[4] == curses.BUTTON2_RELEASED:
            #Mid button released
            self.set_current_btn(Workspace.BTN_M_RELEASED, Pos(mouse[2], mouse[1]))
            t = threading.Timer(self.mouse_interval, self.mouse_alam, (None,))
            t.start()

        elif mouse[4] == curses.BUTTON3_PRESSED:
            #Right button pressed
            self.awake_view_by_pos(Pos(mouse[2], mouse[1]))
            self.drag_begin = Pos(mouse[2], mouse[1])
            self.set_current_btn(Workspace.BTN_R_PRESSED, Pos(mouse[2], mouse[1]))
            t = threading.Timer(self.mouse_interval, self.mouse_alam, (None,))
            t.start()

        elif mouse[4] == curses.BUTTON3_RELEASED:
            #Right button released
            self.set_current_btn(Workspace.BTN_R_RELEASED, Pos(mouse[2], mouse[1]))
            t = threading.Timer(self.mouse_interval, self.mouse_alam, (None,))
            t.start()
            pass

        elif mouse[4] == curses.BUTTON4_PRESSED:
            #Scoll up
            self.set_current_btn(None, None)
            self.focused_view.dispatch_msg(Message(Message.MSG_SCOLL,
                1))

        elif mouse[4] == 2097152:
            #Scoll down
            self.set_current_btn(None, None)
            self.focused_view.dispatch_msg(Message(Message.MSG_SCOLL,
                -1))

        elif mouse[4] == curses.REPORT_MOUSE_POSITION:
            #Drag
            self.set_current_btn(None, None)
            self.focused_view.dispatch_msg(Message(Message.MSG_DRAG,
                (Pos(self.drag_begin.top - self.focused_view.rect.pos.top,
                    self.drag_begin.left - self.focused_view.rect.pos.left),
                    Pos(mouse[2] - self.focused_view.rect.pos.top,
                        mouse[1] - self.focused_view.rect.pos.left)
                    )))
            self.drag_begin = Pos(mouse[2], mouse[1])

        return

    def mouse_alam(self, unused):
        self.inputlock.acquire()
        try:
            if time.time() - self.clicktime > self.mouse_interval:
                self.set_current_btn(None,None)

        except Exception:
            log.debug_log(traceback.format_exc())
            self.close()

        finally:
            self.inputlock.release()
        return

    def thread_frame(self, func, *args, **kwargs):
        self.inputlock.acquire()
        try:
            func(*args, **kwargs)

        except Exception:
            log.debug_log(traceback.format_exc())
            self.close()

        finally:
            self.inputlock.release()
        return


    def awake_view_by_pos(self, pos):
        if pos.top == self.size.height - 1:
            #Enter command mode
            if self.mode != Workspace.COMMAND_MODE:
                self.mode = Workspace.COMMAND_MODE
            self.command_curser = pos.left + self.cmd_show_begin

            if self.command_curser > len(self.command_buf):
                self.command_curser = len(self.command_buf)

            self.cmdline_refresh()

        else:
            if self.mode != Workspace.EDIT_MODE:
                self.mode = Workspace.EDIT_MODE
                self.cmdline_refresh()

            if not pos in self.focused_view.rect:
                for v in self.views:
                    if pos in v.rect:
                        self.switch_focused(v)
                        break

        return

    def msg_inject(self, msg, target):
        self.inputlock.acquire()
        ret = None
        try:
            target.dispatch_msg(msg)
        except Exception:
            log.debug_log(traceback.format_exc())
            self.close()

        finally:
            self.inputlock.release()

        return ret

    def popup(self, lst, pos):
        menu = Popup(lst, self)
        ret = menu.pop(pos)
        self.redraw()
        self.update()
        return ret
