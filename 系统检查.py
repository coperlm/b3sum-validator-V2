import sys
import os
import ctypes
import platform

def check_python():
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {platform.python_version()}")
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        return False
    return True

def check_dependencies():
    """检查依赖项"""
    try:
        import blake3
        print(f"BLAKE3库已安装: {blake3.__version__}")
        return True
    except ImportError:
        print("未安装BLAKE3库，请运行'安装依赖.bat'")
        return False

def check_admin():
    """检查是否有管理员权限"""
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        print(f"管理员权限: {'是' if is_admin else '否'}")
        return is_admin
    except Exception:
        print("无法检查管理员权限")
        return False

def main():
    """执行所有检查"""
    print("===== BLAKE3文件哈希重命名工具 - 系统检查 =====")
    print(f"操作系统: {platform.system()} {platform.version()}")
    
    python_ok = check_python()
    deps_ok = check_dependencies()
    admin_ok = check_admin()
    
    print("\n===== 检查结果 =====")
    if all([python_ok, deps_ok]):
        print("✓ 基本环境配置正确")
    else:
        print("✗ 发现环境问题，请查看上方详细信息")
    
    if admin_ok:
        print("✓ 有管理员权限，可以注册右键菜单")
    else:
        print("✗ 没有管理员权限，注册右键菜单时需要提升权限")
    
    print("\n如需注册右键菜单，请运行'启动工具.bat'并点击'注册到右键菜单'按钮")

if __name__ == "__main__":
    main()
    print("\n按Enter键退出...")
    input()
