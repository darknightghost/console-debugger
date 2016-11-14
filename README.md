# console-debugger
A general debugging foreground.

##依赖包
ncurses
python
python-watchdog

##用法
```
cdbg -a 适配器 适配器参数 调试目标 参数
```

##操作方法
###模式切换

```
该调试前端分为两种模式, 命令模式与编辑模式, 编辑模式下操作由焦点所在窗口获得, 命令模式用来输入命令,两种模式用ESC键切换.
```

###窗口操作

```
水平分割窗口 : sp
垂直分割窗口 : vs
上一个标签 : pt
下一个标签 : nt
进入窗口操作模式 : Ctrl + w
在窗口操作模式下:
    切换当前窗口 : 方向键或hjkl, 具体参照vim
    垂直缩放窗口 : =/-
    水平缩放窗口 : ./,
退出窗口操作模式 : Esc
也可以点鼠标或者拖拽.

关闭view:qv
```

###调试操作

```
```
