# b3sum-validator-V2
跨平台 BLAKE3 哈希文件重命名工具

## 功能介绍
计算文件的 BLAKE3 哈希值，并将前16位添加到文件名：`原文件名(BLAKE3：哈希值前16位).扩展名`

**支持平台**：Windows、Linux、macOS

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 使用方式

**命令行（所有平台）**
```bash
python b3sum_rename.py <文件路径>
```

**右键菜单（推荐）**
- **Windows**: 以管理员身份运行 `start_tool.bat`，点击"注册到右键菜单"
- **Linux**: 运行 `sudo python b3sum_rename.py`，点击"注册到右键菜单"，重启文件管理器后生效
- **macOS**: 暂不支持，请使用命令行

注册后，右键点击文件选择"使用BLAKE3计算哈希并重命名"即可。

### 3. 卸载右键菜单
- **Windows**: 以管理员身份运行 `start_tool.bat`，点击"从右键菜单移除"
- **Linux**: 运行 `sudo python b3sum_rename.py`，点击"从右键菜单移除"
- **macOS**: 直接删除程序文件夹

---

备注：实则我还没有测试过linux和mac下的可用性