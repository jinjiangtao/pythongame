import tkinter as tk
from collections import deque

def flood_fill(canvas, x, y, fill_color, tolerance=0):
    image = canvas.image
    if image is None:
        return
    
    width = image.width()
    height = image.height()
    
    if x < 0 or x >= width or y < 0 or y >= height:
        return
    
    target_color = image.get(x, y)
    if target_color == fill_color:
        return
    
    queue = deque()
    queue.append((x, y))
    
    while queue:
        cx, cy = queue.popleft()
        
        if cx < 0 or cx >= width or cy < 0 or cy >= height:
            continue
        
        current_color = image.get(cx, cy)
        
        r1, g1, b1 = current_color
        r2, g2, b2 = target_color
        
        diff = abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)
        
        if diff > tolerance:
            continue
        
        image.put(fill_color, (cx, cy))
        
        queue.append((cx + 1, cy))
        queue.append((cx - 1, cy))
        queue.append((cx, cy + 1))
        queue.append((cx, cy - 1))
    
    canvas.redraw()

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{0:02x}{1:02x}{2:02x}'.format(*rgb)

def get_color_name(color):
    color_map = {
        '#000000': 'black',
        '#ffffff': 'white',
        '#ff0000': 'red',
        '#00ff00': 'green',
        '#0000ff': 'blue',
        '#ffff00': 'yellow',
        '#ff00ff': 'magenta',
        '#00ffff': 'cyan',
        '#ff8800': 'orange',
        '#8800ff': 'purple',
        '#0088ff': 'lightblue',
        '#88ff00': 'lime',
    }
    return color_map.get(color.lower(), 'gray')