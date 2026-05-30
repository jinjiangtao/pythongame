# 3D装修效果图生成工具 - 技术架构文档

## 1. 项目概述

### 项目名称
3D装修效果图生成工具(Floor Plan to 3D Decorator)

### 项目类型
前端单页应用(Web Application)

### 核心功能
用户上传平面图图片,通过手动绘制墙体轮廓,自动生成3D装修效果场景,包含立体墙壁、地板和家具布置。

### 目标用户
- 室内设计师
- 装修业主
- 房产中介

## 2. 技术栈

### 前端框架
- **HTML5**: 页面结构
- **CSS3**: 样式和布局(采用Flexbox布局)
- **JavaScript(ES6+)**: 业务逻辑
- **Three.js**: 3D渲染引擎(v0.150+)
- **OrbitControls.js**: Three.js相机控制插件

### 依赖库
- Three.js (通过CDN引入)
- OrbitControls (Three.js附加组件)

### 无需构建工具
- 所有代码通过原生JS编写
- 通过CDN引入第三方库
- 可直接在浏览器中打开运行

## 3. 文件结构

```
jszhuangxiu/
├── index.html          # 主页面文件
├── css/
│   └── style.css       # 样式文件
├── js/
│   ├── main.js         # 主逻辑入口
│   ├── upload.js       # 图片上传模块
│   ├── wall-drawer.js  # 墙体绘制模块
│   └── scene-3d.js     # Three.js 3D场景模块
└── prd-01.md           # 产品需求文档
```

## 4. 模块设计

### 4.1 图片上传模块(upload.js)
**功能:**
- 支持拖拽上传
- 支持点击选择文件
- 验证文件类型(JPG/PNG)
- 显示上传进度
- 预览图片

**主要API:**
```javascript
class ImageUploader {
    constructor(domElement)
    onImageLoaded(callback)
    getImageElement()
    reset()
}
```

**事件:**
- `imageLoaded`: 图片加载完成后触发
- `uploadError`: 上传错误时触发

### 4.2 墙体绘制模块(wall-drawer.js)
**功能:**
- 在图片上叠加Canvas层
- 鼠标点击添加墙体点
- 双击闭合房间轮廓
- 绘制墙体线段
- 保存所有房间的多边形坐标
- 至少绘制2-3个房间

**主要API:**
```javascript
class WallDrawer {
    constructor(imageElement, canvasElement)
    enableDrawing()
    disableDrawing()
    getRooms()  // 返回所有房间的多边形坐标数组
    clearAll()
    reset()
}
```

**数据结构:**
```javascript
// 房间数据格式
{
    id: string,
    points: [{x: number, y: number}, ...],  // 相对于图片的坐标
    color: string
}
```

### 4.3 3D场景模块(scene-3d.js)
**功能:**
- 初始化Three.js场景
- 创建相机(透视相机)
- 创建渲染器
- 添加光源(环境光+平行光)
- 渲染墙壁(ExtrudeGeometry)
- 渲染地板(PlaneGeometry)
- 自动放置家具
- 启用OrbitControls

**主要API:**
```javascript
class Scene3D {
    constructor(domElement)
    buildFromRooms(rooms, imageWidth, imageHeight)
    addWalls(rooms, imageWidth, imageHeight)
    addFloor(rooms, imageWidth, imageHeight)
    addFurniture(rooms, imageWidth, imageHeight)
    reset()
    enableControls()
    disableControls()
}
```

**墙壁生成算法:**
1. 遍历所有房间
2. 对每个房间的多边形,提取边界线段
3. 使用THREE.ExtrudeGeometry沿边界挤出
4. 设置墙体高度为2-3个单位
5. 设置墙体颜色和材质

**家具生成逻辑:**
1. 计算每个房间的中心点
2. 根据房间大小,自动选择家具类型
3. 生成简单的几何体组合:
   - 卧室: 床(大立方体) + 床头柜(小立方体)
   - 客厅: 沙发(大立方体) + 茶几(小立方体)
   - 餐厅: 餐桌(立方体) + 椅子(小立方体)
4. 设置不同颜色区分

**家具类型映射:**
```javascript
{
    'bedroom': { color: 0x8B4513, items: ['bed', 'nightstand'] },
    'living': { color: 0x4169E1, items: ['sofa', 'table'] },
    'dining': { color: 0x228B22, items: ['table', 'chairs'] }
}
```

### 4.4 主逻辑模块(main.js)
**功能:**
- 初始化所有模块
- 协调模块间的通信
- 响应用户操作
- 处理全局状态

**主要流程:**
1. 页面加载完成后初始化UI
2. 监听上传模块的imageLoaded事件
3. 初始化墙体绘制模块
4. 监听墙体绘制完成事件
5. 调用3D场景模块生成模型

## 5. 用户交互流程

```
1. 用户打开页面
   ↓
2. 用户上传平面图图片(拖拽或点击)
   ↓
3. 图片显示在左侧画布
   ↓
4. 用户在图片上绘制墙体(点击画点)
   ↓
5. 用户双击闭合房间(至少2-3个房间)
   ↓
6. 程序自动生成3D场景
   ↓
7. 用户通过鼠标旋转/缩放查看效果
```

## 6. UI布局设计

### 整体布局
- 左侧面板(40%宽度): 上传区 + 墙体绘制区
- 右侧面板(60%宽度): 3D场景渲染区
- 底部控制栏: 操作提示和功能按钮

### 左侧面板
```
┌─────────────────────┐
│    上传区域          │
│  (拖拽或点击上传)    │
└─────────────────────┘
┌─────────────────────┐
│    图片预览区        │
│  + Canvas绘制层      │
│  (点击画点,双击闭合) │
└─────────────────────┘
```

### 右侧面板
```
┌─────────────────────┐
│                     │
│   Three.js 3D场景    │
│                     │
│   (自动生成墙壁/地板)│
│   (自动放置家具)     │
│                     │
└─────────────────────┘
```

## 7. 坐标映射算法

### 从2D到3D的映射
1. **原点定位**: 3D场景的原点(0,0,0)对应图片的左下角
2. **X轴映射**: 图片X轴 → 3D X轴(保持比例)
3. **Y轴映射**: 图片Y轴 → 3D Z轴(保持比例)
4. **Z轴**: 用于墙体高度(2-3个单位)

### 比例计算
```javascript
const scaleX = 10 / imageWidth;   // 假设场景宽度为10个单位
const scaleY = 10 / imageHeight;
const wallHeight = 2.5;            // 墙体高度2.5个单位
```

## 8. 性能优化

### 绘制优化
- Canvas仅在需要时重绘
- 使用requestAnimationFrame优化渲染

### 3D优化
- 使用BufferGeometry减少内存占用
- 合理设置材质和光照
- 启用抗锯齿

### 内存管理
- 及时清理未使用的Three.js对象
- 重置时完全销毁旧场景

## 9. 浏览器兼容性

### 支持的浏览器
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### 必需功能
- HTML5 Canvas
- WebGL 2.0
- ES6 Modules(通过script type="module")

## 10. 错误处理

### 上传错误
- 文件类型错误: 提示"JPG/PNG格式"
- 文件读取失败: 提示"图片加载失败"
- 文件过大: 提示文件大小限制

### 绘制错误
- 点数过少: 提示"至少需要3个点"
- 房间数不足: 提示"请绘制至少2-3个房间"
- 重叠绘制: 允许但不处理

### 3D生成错误
- 坐标无效: 跳过该房间
- WebGL不支持: 提示浏览器不支持

## 11. 扩展性设计

### 预留接口
- 可扩展的家具库(添加更多家具类型)
- 可配置的墙体材质
- 可调整的墙体高度
- 可选择的家具布局算法

### 模块化设计
- 各模块独立,可通过API交互
- 便于后续功能扩展
- 便于维护和调试

## 12. 测试计划

### 功能测试
- [ ] 图片上传功能(拖拽+点击)
- [ ] 墙体绘制(点击画点)
- [ ] 房间闭合(双击)
- [ ] 3D墙壁生成
- [ ] 3D地板生成
- [ ] 家具自动放置
- [ ] 相机旋转和缩放

### 边界测试
- [ ] 空图片上传
- [ ] 极小/大图片处理
- [ ] 绘制少于3个点的房间
- [ ] 绘制重叠的房间
- [ ] 浏览器不支持WebGL

## 13. 部署方式

### 运行方式
1. 直接打开index.html(通过本地服务器或file协议)
2. 推荐使用本地服务器避免CORS问题:
   ```bash
   # Python
   python -m http.server 8000
   
   # Node.js
   npx http-server
   ```

### CDN依赖
- Three.js: https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js
- OrbitControls: https://unpkg.com/three@0.128.0/examples/js/controls/OrbitControls.js

## 14. 总结

本项目采用纯前端实现,无需后端支持,具有良好的可移植性和易用性。通过模块化设计,代码结构清晰,便于后续扩展和维护。Three.js提供了强大的3D渲染能力,能够满足室内装修效果展示的需求。
