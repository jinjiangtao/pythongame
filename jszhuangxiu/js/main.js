import { ImageUploader } from './upload.js';
import { WallDrawer } from './wall-drawer.js';
import { Scene3D } from './scene-3d.js';

class App {
    constructor() {
        this.uploader = null;
        this.wallDrawer = null;
        this.scene3D = null;
        this.currentImage = null;
        
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
    }
    
    initModules() {
        this.uploader = new ImageUploader(this.uploadArea, this.fileInput);
        
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
        
        window.addEventListener('resize', () => {
            if (this.scene3D && this.scene3D.isInitialized) {
                this.scene3D.onWindowResize();
            }
        });
    }
    
    handleImageLoaded(image) {
        this.currentImage = image;
        
        this.floorPlanImage.src = image.src;
        
        this.uploadArea.style.display = 'none';
        this.drawingArea.style.display = 'block';
        
        this.floorPlanImage.onload = () => {
            this.wallDrawer = new WallDrawer(this.floorPlanImage, this.wallCanvas);
            this.wallDrawer.enableDrawing();
            
            this.wallDrawer.onRoomCountChange((count) => {
                this.updateRoomCount(count);
            });
        };
        
        this.scenePlaceholder.style.display = 'none';
        this.threeCanvas.style.display = 'block';
        this.sceneControls.style.display = 'flex';
        
        this.scene3D = new Scene3D(this.sceneContainer, this.threeCanvas);
        this.scene3D.init();
    }
    
    handleUndo() {
        if (this.wallDrawer) {
            const undone = this.wallDrawer.undoLastPoint();
            if (undone) {
                this.updateRoomCount(this.wallDrawer.getRoomCount());
            }
        }
    }
    
    handleClear() {
        if (this.wallDrawer) {
            this.wallDrawer.clearAll();
            this.updateRoomCount(0);
        }
        
        if (this.scene3D) {
            this.scene3D.reset();
        }
    }
    
    handleGenerate() {
        if (!this.wallDrawer) {
            alert('请先上传图片并绘制墙体');
            return;
        }
        
        const roomCount = this.wallDrawer.getRoomCount();
        if (roomCount < 2) {
            alert(`请至少绘制 2 个房间，当前已绘制 ${roomCount} 个房间`);
            return;
        }
        
        const rooms = this.wallDrawer.getRooms();
        const dimensions = this.wallDrawer.getImageDimensions();
        
        this.scene3D.buildFromRooms(rooms, dimensions.width, dimensions.height);
        
        alert(`🎉 3D场景生成成功！共 ${roomCount} 个房间\n\n操作提示：\n• 鼠标左键拖拽旋转视角\n• 鼠标滚轮缩放\n• 右键拖拽平移`);
    }
    
    handleResetScene() {
        if (this.scene3D) {
            this.scene3D.reset();
        }
        
        alert('场景已重置，可以重新绘制墙体');
    }
    
    updateRoomCount(count) {
        this.roomCount.textContent = count;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new App();
});
