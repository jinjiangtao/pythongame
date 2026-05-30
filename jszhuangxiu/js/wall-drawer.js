export class WallDrawer {
    constructor(imageElement, canvasElement) {
        this.imageElement = imageElement;
        this.canvasElement = canvasElement;
        this.ctx = canvasElement.getContext('2d');
        this.rooms = [];
        this.currentRoom = [];
        this.isDrawing = false;
        this.roomIdCounter = 0;
        
        this.roomColors = [
            '#4F46E5', '#10B981', '#F59E0B', '#EF4444', 
            '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16'
        ];
        
        this.init();
    }
    
    init() {
        this.updateCanvasSize();
        this.bindEvents();
    }
    
    updateCanvasSize() {
        const rect = this.imageElement.getBoundingClientRect();
        
        this.canvasElement.width = this.imageElement.naturalWidth;
        this.canvasElement.height = this.imageElement.naturalHeight;
        
        this.canvasElement.style.width = rect.width + 'px';
        this.canvasElement.style.height = rect.height + 'px';
        
        this.imageWidth = this.imageElement.naturalWidth;
        this.imageHeight = this.imageElement.naturalHeight;
        this.displayWidth = rect.width;
        this.displayHeight = rect.height;
        this.scaleX = this.imageWidth / this.displayWidth;
        this.scaleY = this.imageHeight / this.displayHeight;
    }
    
    bindEvents() {
        this.canvasElement.addEventListener('click', (e) => this.handleClick(e));
        this.canvasElement.addEventListener('dblclick', (e) => this.handleDoubleClick(e));
        
        window.addEventListener('resize', () => {
            this.redraw();
        });
    }
    
    handleClick(e) {
        if (!this.isDrawing) return;
        
        const rect = this.canvasElement.getBoundingClientRect();
        const displayX = e.clientX - rect.left;
        const displayY = e.clientY - rect.top;
        
        const x = displayX * this.scaleX;
        const y = displayY * this.scaleY;
        
        this.currentRoom.push({ x, y });
        this.redraw();
    }
    
    handleDoubleClick(e) {
        if (!this.isDrawing || this.currentRoom.length < 3) return;
        
        this.closeRoom();
    }
    
    closeRoom() {
        const room = {
            id: `room_${this.roomIdCounter++}`,
            points: [...this.currentRoom],
            color: this.roomColors[this.rooms.length % this.roomColors.length]
        };
        
        this.rooms.push(room);
        this.currentRoom = [];
        this.redraw();
        this.notifyRoomCountChange(this.rooms.length);
        
        return room;
    }
    
    enableDrawing() {
        this.isDrawing = true;
        this.canvasElement.style.cursor = 'crosshair';
    }
    
    disableDrawing() {
        this.isDrawing = false;
        this.canvasElement.style.cursor = 'default';
    }
    
    undoLastPoint() {
        if (this.currentRoom.length > 0) {
            this.currentRoom.pop();
            this.redraw();
            return true;
        } else if (this.rooms.length > 0) {
            this.rooms.pop();
            this.roomIdCounter--;
            this.redraw();
            return true;
        }
        return false;
    }
    
    clearAll() {
        this.rooms = [];
        this.currentRoom = [];
        this.roomIdCounter = 0;
        this.redraw();
        this.notifyRoomCountChange(0);
    }
    
    redraw() {
        this.updateCanvasSize();
        this.ctx.clearRect(0, 0, this.canvasElement.width, this.canvasElement.height);
        
        this.rooms.forEach((room, index) => {
            this.drawRoom(room.points, room.color, index + 1);
        });
        
        if (this.currentRoom.length > 0) {
            this.drawRoom(this.currentRoom, '#6B7280', null);
        }
    }
    
    drawRoom(points, color, roomNumber) {
        if (points.length < 2) return;
        
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = 3;
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';
        
        this.ctx.beginPath();
        this.ctx.moveTo(points[0].x, points[0].y);
        
        for (let i = 1; i < points.length; i++) {
            this.ctx.lineTo(points[i].x, points[i].y);
        }
        
        if (roomNumber !== null) {
            this.ctx.closePath();
        }
        
        this.ctx.stroke();
        
        points.forEach((point, index) => {
            this.ctx.fillStyle = color;
            this.ctx.beginPath();
            this.ctx.arc(point.x, point.y, 5, 0, Math.PI * 2);
            this.ctx.fill();
            
            if (index === 0) {
                this.ctx.fillStyle = 'white';
                this.ctx.beginPath();
                this.ctx.arc(point.x, point.y, 2, 0, Math.PI * 2);
                this.ctx.fill();
            }
        });
        
        if (roomNumber !== null) {
            const center = this.calculateCentroid(points);
            this.drawRoomLabel(center.x, center.y, `房间${roomNumber}`, color);
        }
    }
    
    drawRoomLabel(x, y, text, bgColor) {
        this.ctx.font = 'bold 16px Arial';
        const metrics = this.ctx.measureText(text);
        const padding = 6;
        const width = metrics.width + padding * 2;
        const height = 24;
        
        this.ctx.fillStyle = bgColor;
        this.ctx.fillRect(x - width/2, y - height/2, width, height);
        
        this.ctx.strokeStyle = 'white';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(x - width/2, y - height/2, width, height);
        
        this.ctx.fillStyle = 'white';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(text, x, y);
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
    
    getRooms() {
        return this.rooms.map(room => ({
            ...room,
            scaledPoints: room.points.map(p => ({
                x: p.x,
                y: p.y
            })),
            scaledCentroid: {
                x: this.calculateCentroid(room.points).x,
                y: this.calculateCentroid(room.points).y
            }
        }));
    }
    
    getRoomCount() {
        return this.rooms.length;
    }
    
    onRoomCountChange(callback) {
        this.roomCountCallbacks = this.roomCountCallbacks || [];
        this.roomCountCallbacks.push(callback);
    }
    
    notifyRoomCountChange(count) {
        if (this.roomCountCallbacks) {
            this.roomCountCallbacks.forEach(cb => cb(count));
        }
    }
    
    getImageDimensions() {
        return {
            width: this.imageWidth,
            height: this.imageHeight
        };
    }
    
    reset() {
        this.rooms = [];
        this.currentRoom = [];
        this.roomIdCounter = 0;
        this.isDrawing = false;
        this.ctx.clearRect(0, 0, this.canvasElement.width, this.canvasElement.height);
    }
}
