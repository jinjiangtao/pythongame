
"""
程序入口
包含依赖检测与自动安装
"""

import sys
import subprocess
import importlib
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
    except subprocess.CalledProcessError:
        return False


def check_dependencies():
    """
    检查并安装依赖
    """
    missing_packages = []

    for package in REQUIRED_PACKAGES:
        package_name = package.split("==")[0].split(">=")[0]
        try:
            importlib.import_module(package_name.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        msg = f"正在安装缺失的依赖包: {', '.join(missing_packages)}\n请稍候..."
        print(msg)

        for package in missing_packages:
            if not install_package(package):
                messagebox.showerror("安装失败", f"无法安装包: {package}")
                return False

    return True


def main():
    """
    主函数
    """
    if not check_dependencies():
        sys.exit(1)

    if not check_npcap_installed():
        response = messagebox.askyesno(
            "Npcap未安装",
            f"检测到未安装Npcap驱动，这是抓包功能所必需的。\n"
            f"是否现在访问 {NPCAP_DOWNLOAD_URL} 下载安装？\n\n"
            f"安装完成后请重新运行此程序。"
        )
        if response:
            import webbrowser
            webbrowser.open(NPCAP_DOWNLOAD_URL)
        sys.exit(0)

    from app import App

    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
