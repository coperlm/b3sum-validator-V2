import os
import sys
import hashlib
import re
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import winreg
import ctypes

try:
    import blake3
except ImportError:
    print("安装 blake3 库...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "blake3"])
    import blake3

def is_admin():
    """检查程序是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def calculate_hash(file_path):
    """计算文件的BLAKE3哈希值"""
    hasher = blake3.blake3()
    with open(file_path, 'rb') as f:
        chunk = f.read(8192)
        while chunk:
            hasher.update(chunk)
            chunk = f.read(8192)
    return hasher.hexdigest()

def rename_file(file_path):
    """计算哈希值并重命名文件"""
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        return f"错误: 文件不存在: {file_path}"
    
    try:
        # 计算BLAKE3哈希值
        hash_value = calculate_hash(file_path)
        hash_prefix = hash_value[:16]  # 获取前16位
        
        # 解析文件路径
        path_obj = Path(file_path)
        directory = path_obj.parent
        name = path_obj.stem
        extension = path_obj.suffix
        
        # 检查文件名是否已经包含哈希值
        pattern = r'\(BLANK3：[a-f0-9]{16}\)'
        if re.search(pattern, name):
            # 移除旧的哈希值标记
            name = re.sub(pattern, '', name).strip()
        
        # 创建新文件名
        new_name = f"{name}(BLANK3：{hash_prefix}){extension}"
        new_path = directory / new_name
        
        # 重命名文件
        os.rename(file_path, new_path)
        
        return f"已成功重命名文件:\n{os.path.basename(file_path)} → {new_name}"
    
    except Exception as e:
        return f"重命名时出错: {str(e)}"

def register_context_menu():
    """注册右键菜单"""
    if not is_admin():
        # 如果不是以管理员身份运行，重新以管理员身份启动
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return
    
    try:
        script_path = os.path.abspath(sys.argv[0])
        
        # 为所有文件创建右键菜单
        key_path = r'*\\shell\\B3SumRename'
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "使用BLAKE3计算哈希并重命名")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, sys.executable)
        
        # 添加命令
        command_key_path = f'{key_path}\\command'
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_key_path) as key:
            command = f'"{sys.executable}" "{script_path}" "%1"'
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)
        
        return "成功注册到右键菜单！"
    except Exception as e:
        return f"注册右键菜单时出错: {str(e)}"

def unregister_context_menu():
    """移除右键菜单"""
    if not is_admin():
        # 如果不是以管理员身份运行，重新以管理员身份启动
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return
    
    try:
        key_path = r'*\\shell\\B3SumRename'
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, f'{key_path}\\command')
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
        return "成功移除右键菜单！"
    except Exception as e:
        return f"移除右键菜单时出错: {str(e)}"

def show_gui():
    """显示简单的GUI界面用于注册/移除右键菜单"""
    root = tk.Tk()
    root.title("BLAKE3 哈希重命名工具")
    root.geometry("400x200")
    root.resizable(False, False)
    
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    title = tk.Label(frame, text="BLAKE3 文件哈希重命名工具", font=("Arial", 14, "bold"))
    title.pack(pady=10)
    
    register_btn = tk.Button(frame, text="注册到右键菜单", width=20, height=2,
                           command=lambda: messagebox.showinfo("结果", register_context_menu()))
    register_btn.pack(pady=5)
    
    unregister_btn = tk.Button(frame, text="从右键菜单移除", width=20, height=2,
                             command=lambda: messagebox.showinfo("结果", unregister_context_menu()))
    unregister_btn.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        show_gui()
    elif len(sys.argv) == 2:
        file_path = sys.argv[1]
        # 直接重命名，不显示任何弹窗
        rename_file(file_path)
    else:
        print("用法: b3sum_rename.py [文件路径]")
