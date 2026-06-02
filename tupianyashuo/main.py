# ========== main.py ==========
"""
程序入口：启动图片批量压缩工具
"""
from app import ImageCompressorApp


def main():
    """主函数"""
    app = ImageCompressorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
