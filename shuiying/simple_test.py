
from PIL import Image, ImageDraw, ImageFont

print("=== 简单水印测试 ===")

# 1. 创建测试图片
img = Image.new('RGB', (800, 600), color='lightblue')
draw = ImageDraw.Draw(img)
draw.rectangle([100, 100, 300, 300], fill='red')
img.save('simple_test_input.jpg')
print("创建了测试图片 simple_test_input.jpg")

# 2. 简单的测试 - 直接在图片上绘制文字
print("\n测试1: 直接绘制文字")
test1 = img.copy()
draw = ImageDraw.Draw(test1)
font = ImageFont.load_default()
draw.text((100, 100), "直接测试文字", fill=(0, 0, 0), font=font)
test1.save('simple_test1.jpg')
print("保存到 simple_test1.jpg - 应该能看到文字")

# 3. 测试文字水印方式
print("\n测试2: 使用水印方式")
test2 = img.copy().convert('RGBA')

# 创建文字水印
txt_img = Image.new('RGBA', (200, 100), (0, 0, 0, 0))
draw = ImageDraw.Draw(txt_img)
draw.text((10, 10), "水印测试文字", fill=(0, 0, 0, 255), font=font)

# 粘贴水印
pos = (500, 400)
test2.paste(txt_img, pos, txt_img)

# 保存
background = Image.new('RGB', test2.size, (255, 255, 255))
background.paste(test2, mask=test2.split()[3])
background.save('simple_test2.jpg')
print("保存到 simple_test2.jpg - 应该能看到水印")

print("\n=== 测试完成 ===")
