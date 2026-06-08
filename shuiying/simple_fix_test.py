
from PIL import Image, ImageDraw, ImageFont
import os

print("简单直接的水印测试")
print("-" * 40)

# 1. 创建测试图片
img = Image.new('RGB', (600, 400), color='white')
draw = ImageDraw.Draw(img)
draw.rectangle([50, 50, 550, 350], fill='lightblue')
img.save('test_base.jpg')
print("创建 test_base.jpg")

# 2. 直接方法 - 直接在图片上画水印
print("\n方法1: 直接绘制")
result1 = img.copy()
draw1 = ImageDraw.Draw(result1)
try:
    font = ImageFont.truetype("arial", 50)
except:
    font = ImageFont.load_default()
draw1.text((100, 150), "直接绘制水印", fill=(255, 0, 0), font=font)
result1.save('test_direct.jpg')
print("保存 test_direct.jpg - 应该能看到红色文字")

# 3. 水印方法 - 我们的模块
print("\n方法2: 水印模块")

# 手动实现水印逻辑
base_img = Image.open('test_base.jpg').convert('RGBA')

# 创建文字水印
txt_img = Image.new('RGBA', (400, 100), (0, 0, 0, 0))
txt_draw = ImageDraw.Draw(txt_img)
txt_draw.text((20, 20), "水印模块文字", fill=(255, 0, 0, 255), font=font)

# 粘贴水印
x = 100
y = 150
result2 = base_img.copy()
result2.paste(txt_img, (x, y), txt_img)

# 保存
background = Image.new('RGB', result2.size, (255, 255, 255))
background.paste(result2, (0, 0), mask=result2.split()[3])
background.save('test_watermark.jpg', 'JPEG', quality=95)

print("保存 test_watermark.jpg - 也应该能看到红色文字")

# 4. 验证文件
print("\n验证:")
for f in ['test_direct.jpg', 'test_watermark.jpg']:
    if os.path.exists(f):
        print(f"✓ {f} 已生成")
    else:
        print(f"✗ {f} 未生成")

print("\n请手动检查这两张图片，都应该能看到红色文字水印！")
