import { ImageUploader } from './upload.js';
import { WallDrawer } from './wall-drawer.js';
import { Scene3D } from './scene-3d.js';
import { WallDetector } from './wall-detector.js';

class App {
    constructor() {
        this.uploader = null;
        this.wallDrawer = null;
        this.scene3D = null;
        this.wallDetector = null;
        this.currentImage = null;
        this.currentStyle = 'modern';
        this.detectedRooms = [];
        
        this.styles = {
            modern: {
                name: '现代简约',
                wallColor: 0xE5E7EB,
                floorColor: 0xD1D5DB,
                furnitureColor: 0x4B5563,
                ambientIntensity: 0.6,
                directionalIntensity: 0.8
            },
            wood: {
                name: '原木日式',
                wallColor: 0xF5F0E8,
                floorColor: 0xC4A484,
                furnitureColor: 0x8B4513,
                ambientIntensity: 0.7,
                directionalIntensity: 0.6
            },
            luxury: {
                name: '轻奢金属',
                wallColor: 0xFAFAFA,
                floorColor: 0x2C2C2C,
                furnitureColor: 0xC0C0C0,
                ambientIntensity: 0.5,
                directionalIntensity: 1.0
            }
        };
        
        this.initElements();
        this.initModules();
        this.bindEvents();
    }
    
    initElements() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.uploadBtn = document.getElementById('uploadBtn');
        
        this.drawingArea = document.getElementById('drawingArea');
        this.canvasContainer = document.getElementById('canvasContainer');
        this.floorPlanImage = document.getElementById('floorPlanImage');
        this.wallCanvas = document.getElementById('wallCanvas');
        
        this.undoBtn = document.getElementById('undoBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.generateBtn = document.getElementById('generateBtn');
        
        this.roomCount = document.getElementById('roomCount');
        
        this.sceneContainer = document.getElementById('sceneContainer');
        this.scenePlaceholder = document.getElementById('scenePlaceholder');
        this.threeCanvas = document.getElementById('threeCanvas');
        this.sceneControls = document.getElementById('sceneControls');
        this.resetSceneBtn = document.getElementById('resetSceneBtn');
        
        this.styleButtons = document.querySelectorAll('.style-btn');
    }
    
    initModules() {
        this.uploader = new ImageUploader(this.uploadArea, this.fileInput);
        this.wallDetector = new WallDetector();
        
        this.uploader.onImageLoaded((image) => {
            this.handleImageLoaded(image);
        });
        
        this.uploader.onUploadError((message) => {
            alert(message);
        });
    }
    
    bindEvents() {
        this.uploadBtn.addEventListener('click', () => {
            this.fileInput.click();
        });
        
        this.undoBtn.addEventListener('click', () => {
            this.handleUndo();
        });
        
        this.clearBtn.addEventListener('click', () => {
            this.handleClear();
        });
        
        this.generateBtn.addEventListener('click', () => {
            this.handleGenerate();
        });
        
        this.resetSceneBtn.addEventListener('click', () => {
            this.handleResetScene();
        });
        
        this.styleButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const style = e.currentTarget.dataset.style;
                this.handleStyleChange(style);
            });
        });
        
        window.addEventListener('resize', () => {
            if (this.scene3D && this.scene3D.isInitialized) {
                this.scene3D.onWindowResize();
            }
        });
    }
    
    async handleImageLoaded(image) {
        this.currentImage = image;
        
        this.floorPlanImage.src = image.src;
        
        this.uploadArea.style.display = 'none';
        this.drawingArea.style.display = 'block';
        
        this.floorPlanImage.onload = async () => {
            this.wallDrawer = new WallDrawer(this.floorPlanImage, this.wallCanvas);
            
            this.scenePlaceholder.style.display = 'none';
            this.threeCanvas.style.display = 'block';
            this.sceneControls.style.display = 'flex';
            
            this.scene3D = new Scene3D(this.sceneContainer, this.threeCanvas);
            this.scene3D.init();
            
            const loadingOverlay = this.createLoadingOverlay();
            document.body.appendChild(loadingOverlay);
            
            try {
                this.detectedRooms = await this.wallDetector.detectWalls(this.floorPlanImage);
                
                this.wallDrawer.rooms = this.detectedRooms;
                this.wallDrawer.roomIdCounter = this.detectedRooms.length;
                this.wallDrawer.redraw();
                
                this.updateRoomCount(this.detectedRooms.length);
                
                this.scene3D.applyStyle(this.styles[this.currentStyle]);
                this.scene3D.buildFromRooms(
                    this.detectedRooms.map(room => ({
                        ...room,
                        scaledPoints: room.points,
                        scaledCentroid: this.calculateCentroid(room.points)
                    })),
                    this.floorPlanImage.naturalWidth,
                    this.floorPlanImage.naturalHeight
                );
                
                loadingOverlay.remove();
                
                const instructions = document.querySelector('.instructions');
                if (instructions) {
                    instructions.innerHTML = `
                        <p><strong>操作说明：</strong></p>
                        <ul>
                            <li>✅ 墙体已自动识别</li>
                            <li>💡 点击画点可手动添加墙体</li>
                            <li>💡 双击闭合当前房间</li>
                            <li>💡 切换装修风格查看效果</li>
                            <li>💡 鼠标拖拽旋转，滚轮缩放</li>
                        </ul>
                    `;
                }
                
            } catch (error) {
                console.error('墙体识别失败:', error);
                loadingOverlay.remove();
                alert('墙体识别遇到问题，已创建默认房间布局');
                
                this.detectedRooms = this.wallDetector.createDefaultRooms(
                    this.floorPlanImage.naturalWidth,
                    this.floorPlanImage.naturalHeight
                );
                this.wallDrawer.rooms = this.detectedRooms;
                this.wallDrawer.roomIdCounter = this.detectedRooms.length;
                this.wallDrawer.redraw();
                this.updateRoomCount(this.detectedRooms.length);
                
                this.scene3D.applyStyle(this.styles[this.currentStyle]);
                this.scene3D.buildFromRooms(
                    this.detectedRooms.map(room => ({
                        ...room,
                        scaledPoints: room.points,
                        scaledCentroid: this.calculateCentroid(room.points)
                    })),
                    this.floorPlanImage.naturalWidth,
                    this.floorPlanImage.naturalHeight
                );
            }
        };
    }
    
    createLoadingOverlay() {
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        `;
        
        overlay.innerHTML = `
            <div style="font-size: 4rem; margin-bottom: 20px;">🔍</div>
            <div style="font-size: 1.5rem; margin-bottom: 15px;">正在智能识别墙体...</div>
            <div style="font-size: 1rem; opacity: 0.8;">请稍候</div>
        `;
        
        return overlay;
    }
    
    calculateCentroid(points) {
        let sumX = 0, sumY = 0;
        points.forEach(p => {
            sumX += p.x;
            sumY += p.y;
        });
        return {
            x: sumX / points.length,
            y: sumY / points.length
        };
    }
    
    handleStyleChange(style) {
        if (!this.styles[style]) return;
        
        this.currentStyle = style;
        
        this.styleButtons.forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.style === style) {
                btn.classList.add('active');
            }
        });
        
        if (this.scene3D && this.detectedRooms.length > 0) {
            this.scene3D.applyStyle(this.styles[style]);
            this.scene3D.updateScene();
        }
    }
    
    handleUndo() {
        if (this.wallDrawer) {
            const undone = this.wallDrawer.undoLastPoint();
            if (undone) {
                this.updateRoomCount(this.wallDrawer.getRoomCount());
                this.detectedRooms = this.wallDrawer.getRooms();
                
                if (this.scene3D && this.detectedRooms.length > 0) {
                    this.scene3D.applyStyle(this.styles[this.currentStyle]);
                    this.scene3D.buildFromRooms(
                        this.detectedRooms,
                        this.floorPlanImage.naturalWidth,
                        this.floorPlanImage.naturalHeight
                    );
                }
            }
        }
    }
    
    handleClear() {
        if (this.wallDrawer) {
            this.wallDrawer.clearAll();
            this.updateRoomCount(0);
            this.detectedRooms = [];
        }
        
        if (this.scene3D) {
            this.scene3D.reset();
        }
    }
    
    handleGenerate() {
        if (!this.wallDrawer) {
            alert('请先上传户型图');
            return;
        }
        
        const roomCount = this.wallDrawer.getRoomCount();
        if (roomCount < 1) {
            alert('未检测到有效房间，请重新上传图片');
            return;
        }
        
        const rooms = this.wallDrawer.getRooms();
        this.detectedRooms = rooms;
        
        this.scene3D.applyStyle(this.styles[this.currentStyle]);
        this.scene3D.buildFromRooms(
            rooms.map(room => ({
                ...room,
                scaledPoints: room.points,
                scaledCentroid: this.calculateCentroid(room.points)
            })),
            this.floorPlanImage.naturalWidth,
            this.floorPlanImage.naturalHeight
        );
        
        alert(`🎉 3D场景生成成功！共 ${roomCount} 个房间\n\n当前风格：${this.styles[this.currentStyle].name}\n\n操作提示：\n• 鼠标左键拖拽旋转视角\n• 鼠标滚轮缩放\n• 右键拖拽平移\n• 上方可切换不同装修风格`);
    }
    
    handleResetScene() {
        if (this.scene3D) {
            this.scene3D.reset();
        }
        
        if (this.currentImage) {
            this.handleImageLoaded(this.currentImage);
        }
        
        alert('场景已重置，图片将重新识别');
    }
    
    updateRoomCount(count) {
        this.roomCount.textContent = count;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new App();
});
