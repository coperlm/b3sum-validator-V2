# 安装依赖并启动BLAKE3文件哈希重命名工具

# 检查是否以管理员身份运行
function Test-Admin {
    $currentUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentUser.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

# 获取脚本所在目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Admin)) {
    Write-Host "请以管理员身份运行此脚本！" -ForegroundColor Red
    Write-Host "请右键点击PowerShell，选择'以管理员身份运行'，然后重新执行此脚本。"
    Read-Host "按Enter键退出"
    exit
}

# 检查Python是否已安装
try {
    $pythonVersion = (python --version 2>&1)
    Write-Host "检测到Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "未检测到Python！请先安装Python 3.6或更高版本。" -ForegroundColor Red
    Write-Host "可以从 https://www.python.org/downloads/ 下载Python。"
    Read-Host "按Enter键退出"
    exit
}

# 安装必要的依赖
Write-Host "安装必要的Python包..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install blake3

Write-Host "`n依赖安装完成！" -ForegroundColor Green
Write-Host "是否要立即启动程序？" -ForegroundColor Yellow

$startNow = Read-Host "是(Y) 或 否(N)"
if ($startNow -eq "Y" -or $startNow -eq "y") {
    Write-Host "启动BLAKE3文件哈希重命名工具..." -ForegroundColor Cyan
    python "$scriptPath\b3sum_rename.py"
}
else {
    Write-Host "您可以随时通过运行'b3sum_rename.py'来启动程序。" -ForegroundColor Cyan
}

Read-Host "按Enter键退出"
