
import os

def fix_file(file_path):
    print(f"修复文件: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修复HTML转义字符
        original = content
        content = content.replace('<', '<')
        content = content.replace('>', '>')
        content = content.replace('&', '&')
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("  ✓ 已修复")
        else:
            print("  - 无需修复")
    except Exception as e:
        print(f"  ✗ 错误: {e}")

if __name__ == "__main__":
    print("=== 修复HTML转义字符 ===")
    
    # 修复所有Python文件
    for filename in os.listdir('.'):
        if filename.endswith('.py'):
            fix_file(filename)
    
    print("\n=== 修复完成 ===")
