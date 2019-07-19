# sword
自动检查《剑来》是否更新。

# 提示
提醒对话框使用了pywin32模块，通过命令`pip install pywin32`安装。  
如果不想弹出提醒对话框可注释掉相关语句。  
1、 `import win32api,win32con`
2、 `win32api.MessageBox(None, "好好工作！", "提醒", win32con.MB_ICONASTERISK)`