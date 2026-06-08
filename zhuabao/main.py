"""
程序入口
包含依赖检测与自动安装
"""

import sys
import subprocess
import importlib
import webbrowser
from tkinter import messagebox
from settings import REQUIRED_PACKAGES, NPCAP_DOWNLOAD_URL
from utils import check_npcap_installed


def install_package(package):
    """
    安装Python包
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except Exception as e:
        print(f"安装 {package} 失败: {e}")
        return False


def check_dependencies():
    """
    检查并安装依赖
    """
    missing_packages = []

    for package in REQUIRED_PACKAGES:
        package_name = package.split("==")[0].split(">=")[0]
        import_name = package_name.replace("-", "_")
        try:
            importlib.import_module(import_name)
            print(f"依赖 {package_name} 已安装")
        except ImportError:
            print(f"依赖 {package_name} 缺失")
            missing_packages.append(package)

    if missing_packages:
        msg = f"正在安装缺失的依赖包: {', '.join(missing_packages)}\n请稍候..."
        print(msg)

        for package in missing_packages:
            print(f"正在安装 {package}...")
            if not install_package(package):
                messagebox.showerror("安装失败", f"无法安装包: {package}\n\n请尝试手动运行: pip install {package}")
                return False

    return True


def check_npcap_with_guidance():
    """
    检查 Npcap 并提供详细指导
    """
    if check_npcap_installed():
        print("Npcap 已安装")
        return True
    
    # Npcap 未安装，提供详细提示
    npcap_info = """
Npcap 驱动未安装！

为了能正常抓包，特别是抓取 127.0.0.1 (Loopback) 的数据包，请按以下步骤安装 Npcap：

1. 下载 Npcap： https://npcap.com/#download
2. 安装时，请务必勾选以下选项：
   □ "Install Npcap in WinPcap API-compatible Mode"（重要！）
   □ "Support raw 802.11 traffic (and monitor mode) for wireless adapters"（可选）
3. 安装完成后，重新运行本程序

注意：
- 如果只需要抓 Loopback 网卡，安装时确保选择 WinPcap 兼容模式
- 抓包需要管理员权限，请以管理员身份运行本程序
"""
    print(npcap_info)
    
    response = messagebox.askyesno(
        "Npcap 未安装",
        f"{npcap_info}\n\n是否现在访问 Npcap 官网下载？"
    )
    
    if response:
        webbrowser.open(NPCAP_DOWNLOAD_URL)
    
    return False


def is_admin_rights():
    """
    检查是否有管理员权限
    """
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main():
    """
    主函数
    """
    print("="*50)
    print("网络抓包工具启动中...")
    print("="*50)
    
    # 检查管理员权限
    if not is_admin_rights():
        print("警告: 未检测到管理员权限，抓包可能会失败！")
        messagebox.showwarning(
            "权限提示",
            "建议以管理员身份运行此程序，以确保抓包功能正常工作！\n\n方法：右键点击程序或命令行，选择“以管理员身份运行”"
        )
    
    # 检查依赖
    if not check_dependencies():
        print("依赖检查失败，程序退出")
        sys.exit(1)
    
    # 检查 Npcap
    if not check_npcap_with_guidance():
        print("Npcap 检查未通过，程序退出")
        sys.exit(0)
    
    # 导入并运行主应用
    print("启动主界面...")
    from app import App

    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
