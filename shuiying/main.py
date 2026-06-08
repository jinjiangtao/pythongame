
import subprocess
import sys
import os


def install_dependencies():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if not os.path.exists(requirements_path):
        print('requirements.txt not found')
        return
    
    print('正在检查依赖...')
    try:
        import customtkinter
        import PIL
        print('依赖已安装')
        return
    except ImportError:
        print('正在安装依赖...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        print('依赖安装完成')


if __name__ == '__main__':
    install_dependencies()
    from app import run
    run()
