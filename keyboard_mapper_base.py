import keyboard
import time
import sys
import os
import re

# 定义键盘映射指令数组
# 格式: "Alt+键=目标键(说明)"
KEYBOARD_MAPPINGS = [
    "Alt+Q=Ctrl+C(复制)",
    "Alt+W=Ctrl+V(粘贴)",
    "Alt+A=Ctrl+A(全选)",
    "Alt+E=F2(保存)",
    "Alt+D=Backspace(删除)",
    "Alt+S=Enter(回车)"
    "Alt+Z=Delete(删除)"
]

# 程序状态变量
mapping_active = False  # 键盘映射是否激活
registered_hotkeys = []  # 已注册的热键列表

def setup_key_mappings():
    """
    设置键盘映射：
    从KEYBOARD_MAPPINGS数组中读取指令并自动注册
    """
    global mapping_active
    
    print("键盘映射程序已启动:")
    print("按Alt+4激活/取消键盘映射")
    print("按Alt+0退出程序")
    print("注意：在某些应用程序中可能需要以管理员权限运行此程序")
    
    # 注册Alt+4切换映射状态
    keyboard.add_hotkey('alt+4', toggle_mapping)
    
    # 注册Alt+0退出程序
    keyboard.add_hotkey('alt+0', exit_program, suppress=True)
    
    # 保持程序运行
    keyboard.wait('alt+0')

def toggle_mapping():
    """
    切换键盘映射的激活状态
    """
    global mapping_active
    
    if not mapping_active:
        # 激活键盘映射
        activate_mappings()
        mapping_active = True
        print("键盘映射已激活")
    else:
        # 取消键盘映射
        deactivate_mappings()
        mapping_active = False
        print("键盘映射已取消")

def activate_mappings():
    """
    激活所有键盘映射
    """
    global registered_hotkeys
    
    # 动态注册所有映射
    for mapping in KEYBOARD_MAPPINGS:
        print(mapping)
        # 解析映射字符串
        hotkey, target_key, description = parse_mapping(mapping)
        # 注册热键
        hotkey_id = register_hotkey(hotkey, target_key, description)
        registered_hotkeys.append(hotkey_id)

def deactivate_mappings():
    """
    取消所有键盘映射
    """
    global registered_hotkeys
    
    # 取消注册所有热键
    for hotkey_id in registered_hotkeys:
        keyboard.remove_hotkey(hotkey_id)
    
    # 清空热键列表
    registered_hotkeys.clear()
    print("键盘映射已取消")

def parse_mapping(mapping):
    """
    解析映射字符串
    格式: "Alt+Q=Ctrl+C(复制)" -> ("alt+q", "ctrl+c", "复制")
    """
    # 使用正则表达式解析映射字符串
    pattern = r'(.+?)=(.+?)\((.+?)\)'
    match = re.match(pattern, mapping)
    if match:
        hotkey = match.group(1).lower()
        target_key = match.group(2).lower()
        description = match.group(3)
        return hotkey, target_key, description
    else:
        raise ValueError(f"无法解析映射字符串: {mapping}")

def register_hotkey(hotkey, target_key, description):
    """
    注册热键
    """
    # 创建一个闭包来捕获当前循环的target_key值
    def send_key():
        time.sleep(0.01)  # 短暂延迟确保按键被正确处理
        keyboard.send(target_key)
        print(f"执行{description} ({target_key.upper()})")
    
    # 注册热键并返回热键ID，使用suppress=True屏蔽原始按键
    return keyboard.add_hotkey(hotkey, send_key, suppress=True)

def exit_program():
    """
    退出程序
    """
    print("程序即将退出...")
    keyboard.unhook_all()

def check_admin_privileges():
    """检查是否以管理员权限运行"""
    try:
        return os.getuid() == 0
    except AttributeError:
        # Windows系统
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

if __name__ == "__main__":
    # 检查管理员权限
    if not check_admin_privileges():
        print("警告：建议以管理员权限运行此程序以获得最佳效果")
        print("在Windows上，右键点击命令提示符并选择'以管理员身份运行'，然后再次运行此脚本")
    
    try:
        setup_key_mappings()
        print("程序正常退出")
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        keyboard.unhook_all()
    except Exception as e:
        print(f"程序出现错误: {e}")
        import traceback
        traceback.print_exc()