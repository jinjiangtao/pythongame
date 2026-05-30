export class WallDetector {
    constructor() {
        this.threshold = 30;
        this.minLineLength = 50;
        this.maxLineGap = 20;
        this.wallColor = '#4F46E5';
    }

    async detectWalls(imageElement) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        canvas.width = imageElement.naturalWidth;
        canvas.height = imageElement.naturalHeight;
        
        ctx.drawImage(imageElement, 0, 0);
        
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const edges = this.detectEdges(imageData);
        
        const lines = this.extractLines(edges, canvas.width, canvas.height);
        
        const rooms = this.createRoomsFromLines(lines, canvas.width, canvas.height);
        
        return rooms;
    }

    detectEdges(imageData) {
        const width = imageData.width;
        const height = imageData.height;
        const data = imageData.data;
        
        const gray = new Uint8Array(width * height);
        for (let i = 0; i < data.length; i += 4) {
            const idx = i / 4;
            gray[idx] = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
        }
        
        const edges = new Uint8Array(width * height);
        
        for (let y = 1; y < height - 1; y++) {
            for (let x = 1; x < width - 1; x++) {
                const idx = y * width + x;
                
                const gx = 
                    -1 * gray[idx - width - 1] + 1 * gray[idx - width + 1] +
                    -2 * gray[idx - 1] + 2 * gray[idx + 1] +
                    -1 * gray[idx + width - 1] + 1 * gray[idx + width + 1];
                
                const gy = 
                    -1 * gray[idx - width - 1] - 2 * gray[idx - width] - 1 * gray[idx - width + 1] +
                    1 * gray[idx + width - 1] + 2 * gray[idx + width] + 1 * gray[idx + width + 1];
                
                const magnitude = Math.sqrt(gx * gx + gy * gy);
                edges[idx] = magnitude > this.threshold ? 255 : 0;
            }
        }
        
        return edges;
    }

    extractLines(edges, width, height) {
        const lines = [];
        const visited = new Set();
        
        const threshold = this.threshold * 3;
        
        for (let y = 0; y < height; y += 5) {
            for (let x = 0; x < width; x += 5) {
                const idx = y * width + x;
                
                if (edges[idx] > 0 && !visited.has(idx)) {
                    const line = this.traceLine(edges, visited, x, y, width, height);
                    
                    if (line && line.length > this.minLineLength) {
                        lines.push(line);
                    }
                }
            }
        }
        
        return this.mergeLines(lines);
    }

    traceLine(edges, visited, startX, startY, width, height) {
        const points = [];
        const stack = [[startX, startY]];
        
        while (stack.length > 0 && points.length < 500) {
            const [x, y] = stack.pop();
            const idx = y * width + x;
            
            if (x < 0 || x >= width || y < 0 || y >= height) continue;
            if (visited.has(idx)) continue;
            if (edges[idx] === 0) continue;
            
            visited.add(idx);
            points.push({ x, y });
            
            for (let dy = -3; dy <= 3; dy += 2) {
                for (let dx = -3; dx <= 3; dx += 2) {
                    if (Math.abs(dx) + Math.abs(dy) === 4) continue;
                    stack.push([x + dx, y + dy]);
                }
            }
        }
        
        return points.length > 2 ? points : null;
    }

    mergeLines(lines) {
        if (lines.length === 0) return [];
        
        const mergedLines = [];
        
        for (const line of lines) {
            if (line.length < 3) continue;
            
            let minX = Infinity, maxX = -Infinity;
            let minY = Infinity, maxY = -Infinity;
            
            for (const point of line) {
                minX = Math.min(minX, point.x);
                maxX = Math.max(maxX, point.x);
                minY = Math.min(minY, point.y);
                maxY = Math.max(maxY, point.y);
            }
            
            const widthSpan = maxX - minX;
            const heightSpan = maxY - minY;
            
            if (widthSpan > heightSpan && widthSpan > 30) {
                mergedLines.push({
                    type: 'horizontal',
                    y: Math.round((minY + maxY) / 2),
                    x1: Math.round(minX),
                    x2: Math.round(maxX)
                });
            } else if (heightSpan > 30) {
                mergedLines.push({
                    type: 'vertical',
                    x: Math.round((minX + maxX) / 2),
                    y1: Math.round(minY),
                    y2: Math.round(maxY)
                });
            }
        }
        
        return mergedLines;
    }

    createRoomsFromLines(lines, width, height) {
        if (lines.length === 0) {
            return this.createDefaultRooms(width, height);
        }
        
        const horizontalLines = lines.filter(l => l.type === 'horizontal');
        const verticalLines = lines.filter(l => l.type === 'vertical');
        
        horizontalLines.sort((a, b) => a.y - b.y);
        verticalLines.sort((a, b) => a.x - b.x);
        
        const roomColors = [
            '#4F46E5', '#10B981', '#F59E0B', '#EF4444', 
            '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16'
        ];
        
        const rooms = [];
        let roomIdCounter = 0;
        
        const topY = horizontalLines.length > 0 ? horizontalLines[0].y : height * 0.1;
        const bottomY = horizontalLines.length > 0 ? horizontalLines[horizontalLines.length - 1].y : height * 0.9;
        
        const leftX = verticalLines.length > 0 ? verticalLines[0].x : width * 0.1;
        const rightX = verticalLines.length > 0 ? verticalLines[verticalLines.length - 1].x : width * 0.9;
        
        if (horizontalLines.length >= 2 && verticalLines.length >= 2) {
            for (let i = 0; i < Math.min(horizontalLines.length - 1, 3); i++) {
                for (let j = 0; j < Math.min(verticalLines.length - 1, 3); j++) {
                    if (i * 3 + j >= 8) break;
                    
                    const y1 = horizontalLines[i].y;
                    const y2 = horizontalLines[i + 1].y;
                    const x1 = verticalLines[j].x;
                    const x2 = verticalLines[j + 1].x;
                    
                    if (y2 - y1 > 50 && x2 - x1 > 50) {
                        rooms.push({
                            id: `room_${roomIdCounter++}`,
                            points: [
                                { x: x1, y: y1 },
                                { x: x2, y: y1 },
                                { x: x2, y: y2 },
                                { x: x1, y: y2 }
                            ],
                            color: roomColors[rooms.length % roomColors.length]
                        });
                    }
                }
            }
        } else {
            const gridSize = Math.min(3, Math.max(1, Math.floor(Math.sqrt(lines.length))));
            const cellWidth = (rightX - leftX) / gridSize;
            const cellHeight = (bottomY - topY) / gridSize;
            
            for (let i = 0; i < gridSize && rooms.length < 8; i++) {
                for (let j = 0; j < gridSize && rooms.length < 8; j++) {
                    const x1 = leftX + j * cellWidth;
                    const y1 = topY + i * cellHeight;
                    const x2 = x1 + cellWidth;
                    const y2 = y1 + cellHeight;
                    
                    rooms.push({
                        id: `room_${roomIdCounter++}`,
                        points: [
                            { x: x1, y: y1 },
                            { x: x2, y: y1 },
                            { x: x2, y: y2 },
                            { x: x1, y: y2 }
                        ],
                        color: roomColors[rooms.length % roomColors.length]
                    });
                }
            }
        }
        
        if (rooms.length === 0) {
            return this.createDefaultRooms(width, height);
        }
        
        return rooms;
    }

    createDefaultRooms(width, height) {
        const roomColors = [
            '#4F46E5', '#10B981', '#F59E0B', '#EF4444', 
            '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16'
        ];
        
        const rooms = [];
        const padding = Math.min(width, height) * 0.1;
        const roomWidth = (width - padding * 3) / 2;
        const roomHeight = (height - padding * 3) / 2;
        
        for (let i = 0; i < 2; i++) {
            for (let j = 0; j < 2; j++) {
                const x1 = padding + j * (roomWidth + padding);
                const y1 = padding + i * (roomHeight + padding);
                
                rooms.push({
                    id: `room_${i * 2 + j}`,
                    points: [
                        { x: x1, y: y1 },
                        { x: x1 + roomWidth, y: y1 },
                        { x: x1 + roomWidth, y: y1 + roomHeight },
                        { x: x1, y: y1 + roomHeight }
                    ],
                    color: roomColors[rooms.length % roomColors.length]
                });
            }
        }
        
        return rooms;
    }
}
