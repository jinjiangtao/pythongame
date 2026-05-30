export class Scene3D {
    constructor(container, canvas) {
        this.container = container;
        this.canvas = canvas;
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.rooms = [];
        this.meshes = [];
        this.isInitialized = false;
        this.currentStyle = null;
        
        this.wallHeight = 2.5;
        this.wallColor = 0xE5E7EB;
        this.floorColor = 0xD1D5DB;
        
        this.furnitureTypes = [
            {
                name: 'bedroom',
                color: 0x8B4513,
                items: [
                    { type: 'bed', size: [1.5, 0.3, 1.0], offset: { x: 0, z: 0 } },
                    { type: 'nightstand', size: [0.4, 0.4, 0.4], offset: { x: -0.6, z: -0.4 } }
                ]
            },
            {
                name: 'living',
                color: 0x4169E1,
                items: [
                    { type: 'sofa', size: [1.2, 0.4, 0.5], offset: { x: 0, z: 0 } },
                    { type: 'table', size: [0.6, 0.3, 0.4], offset: { x: 0, z: -0.6 } }
                ]
            },
            {
                name: 'dining',
                color: 0x228B22,
                items: [
                    { type: 'table', size: [0.8, 0.4, 0.8], offset: { x: 0, z: 0 } },
                    { type: 'chair', size: [0.3, 0.3, 0.3], offset: { x: -0.5, z: 0 } },
                    { type: 'chair', size: [0.3, 0.3, 0.3], offset: { x: 0.5, z: 0 } }
                ]
            }
        ];
    }
    
    init() {
        if (this.isInitialized) return;
        
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xF3F4F6);
        
        const containerRect = this.container.getBoundingClientRect();
        const width = containerRect.width;
        const height = 600;
        
        this.camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        this.camera.position.set(5, 5, 5);
        this.camera.lookAt(0, 0, 0);
        
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            antialias: true
        });
        this.renderer.setSize(width, height);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);
        this.ambientLight = ambientLight;
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 10);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        directionalLight.shadow.camera.near = 0.5;
        directionalLight.shadow.camera.far = 50;
        directionalLight.shadow.camera.left = -20;
        directionalLight.shadow.camera.right = 20;
        directionalLight.shadow.camera.top = 20;
        directionalLight.shadow.camera.bottom = -20;
        this.scene.add(directionalLight);
        this.directionalLight = directionalLight;
        
        const hemisphereLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.4);
        this.scene.add(hemisphereLight);
        
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.minDistance = 2;
        this.controls.maxDistance = 50;
        this.controls.maxPolarAngle = Math.PI / 2;
        
        const gridHelper = new THREE.GridHelper(20, 20, 0xCCCCCC, 0xE5E7EB);
        this.scene.add(gridHelper);
        
        this.isInitialized = true;
        
        this.animate();
    }
    
    buildFromRooms(rooms, imageWidth, imageHeight) {
        console.log('buildFromRooms 被调用', { rooms, imageWidth, imageHeight });
        try {
            if (!this.isInitialized) {
                console.log('初始化3D场景');
                this.init();
            }
            
            this.clearScene();
            this.rooms = rooms;
            
            const scale = 10 / Math.max(imageWidth, imageHeight);
            const offsetX = 0;
            const offsetZ = 0;
            console.log('缩放比例:', scale);
            
            rooms.forEach((room, index) => {
                console.log('处理房间', index, room);
                const furnitureType = this.furnitureTypes[index % this.furnitureTypes.length];
                
                // 使用当前风格的颜色
                const wallColor = this.currentStyle ? this.currentStyle.wallColor : this.wallColor;
                const floorColor = this.currentStyle ? this.currentStyle.floorColor : this.floorColor;
                const furnitureColor = this.currentStyle ? this.currentStyle.furnitureColor : furnitureType.color;
                
                this.addWalls(room.scaledPoints, scale, offsetX, offsetZ, wallColor, room.id);
            
            this.addFloor(room.scaledPoints, scale, offsetX, offsetZ, floorColor, room.id);
            
            this.addFurniture(room.scaledCentroid, scale, offsetX, offsetZ, furnitureType, room.id, furnitureColor);
            });
            
            const centerX = (offsetX + 5);
            const centerZ = (offsetZ + 5);
            this.camera.position.set(centerX + 5, 5, centerZ + 5);
            this.controls.target.set(centerX, 0, centerZ);
            this.controls.update();
            console.log('buildFromRooms 完成');
        } catch (error) {
            console.error('buildFromRooms 出错:', error);
            throw error;
        }
    }
    
    addWalls(points, scale, offsetX, offsetZ, color, roomId) {
        console.log('addWalls 被调用', { points, color, roomId });
        if (points.length < 3) return;
        
        const shape = new THREE.Shape();
        
        const scaledPoints = points.map(p => ({
            x: p.x * scale + offsetX,
            y: p.y * scale + offsetZ
        }));
        
        shape.moveTo(scaledPoints[0].x, scaledPoints[0].y);
        for (let i = 1; i < scaledPoints.length; i++) {
            shape.lineTo(scaledPoints[i].x, scaledPoints[i].y);
        }
        shape.lineTo(scaledPoints[0].x, scaledPoints[0].y);
        
        // 处理颜色：可以是十六进制数字或字符串
        let wallColor = color;
        if (typeof color === 'string' && color.startsWith('#')) {
            wallColor = parseInt(color.replace('#', '0x'));
        }
        
        const wallMaterial = new THREE.MeshStandardMaterial({
            color: wallColor,
            roughness: 0.7,
            metalness: 0.1
        });
        
        for (let i = 0; i < scaledPoints.length; i++) {
            const p1 = scaledPoints[i];
            const p2 = scaledPoints[(i + 1) % scaledPoints.length];
            
            const dx = p2.x - p1.x;
            const dz = p2.y - p1.y;
            const length = Math.sqrt(dx * dx + dz * dz);
            
            if (length < 0.01) continue;
            
            const wallGeometry = new THREE.BoxGeometry(length, this.wallHeight, 0.1);
            const wall = new THREE.Mesh(wallGeometry, wallMaterial);
            
            wall.position.set(
                (p1.x + p2.x) / 2,
                this.wallHeight / 2,
                (p1.y + p2.y) / 2
            );
            
            const angle = Math.atan2(dz, dx);
            wall.rotation.y = -angle;
            
            wall.castShadow = true;
            wall.receiveShadow = true;
            
            wall.userData = {
                type: 'wall',
                roomId: roomId
            };
            
            this.scene.add(wall);
            this.meshes.push(wall);
        }
        console.log('addWalls 完成，添加了', scaledPoints.length, '面墙');
    }
    
    addFloor(points, scale, offsetX, offsetZ, color, roomId) {
        console.log('addFloor 被调用', { points, color, roomId });
        if (points.length < 3) return;
        
        const shape = new THREE.Shape();
        
        const scaledPoints = points.map(p => ({
            x: p.x * scale + offsetX,
            y: p.y * scale + offsetZ
        }));
        
        shape.moveTo(scaledPoints[0].x, scaledPoints[0].y);
        for (let i = 1; i < scaledPoints.length; i++) {
            shape.lineTo(scaledPoints[i].x, scaledPoints[i].y);
        }
        shape.lineTo(scaledPoints[0].x, scaledPoints[0].y);
        
        // 处理颜色
        let floorColor = color;
        if (typeof color === 'string' && color.startsWith('#')) {
            floorColor = parseInt(color.replace('#', '0x'));
        }
        
        const floorGeometry = new THREE.ShapeGeometry(shape);
        const floorMaterial = new THREE.MeshStandardMaterial({
            color: floorColor,
            roughness: 0.9,
            metalness: 0
        });
        
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.rotation.x = -Math.PI / 2;
        floor.position.y = 0.01;
        floor.receiveShadow = true;
        
        floor.userData = {
            type: 'floor',
            roomId: roomId
        };
        
        this.scene.add(floor);
        this.meshes.push(floor);
        console.log('addFloor 完成');
    }
    
    addFurniture(centroid, scale, offsetX, offsetZ, furnitureType, roomId, color) {
        console.log('addFurniture 被调用', { centroid, furnitureType, roomId, color });
        const centerX = centroid.x * scale + offsetX;
        const centerZ = centroid.y * scale + offsetZ;
        
        // 处理颜色
        let furnitureColor = color;
        if (typeof color === 'string' && color.startsWith('#')) {
            furnitureColor = parseInt(color.replace('#', '0x'));
        }
        
        furnitureType.items.forEach(item => {
            const geometry = new THREE.BoxGeometry(item.size[0], item.size[1], item.size[2]);
            const material = new THREE.MeshStandardMaterial({
                color: furnitureColor,
                roughness: 0.6,
                metalness: 0.2
            });
            
            const furniture = new THREE.Mesh(geometry, material);
            
            furniture.position.set(
                centerX + item.offset.x,
                item.size[1] / 2,
                centerZ + item.offset.z
            );
            
            furniture.castShadow = true;
            furniture.receiveShadow = true;
            
            furniture.userData = {
                type: 'furniture',
                itemType: item.type,
                roomId: roomId,
                furnitureType: furnitureType.name
            };
            
            this.scene.add(furniture);
            this.meshes.push(furniture);
        });
        console.log('addFurniture 完成');
    }
    
    clearScene() {
        this.meshes.forEach(mesh => {
            this.scene.remove(mesh);
            if (mesh.geometry) {
                mesh.geometry.dispose();
            }
            if (mesh.material) {
                mesh.material.dispose();
            }
        });
        this.meshes = [];
    }
    
    reset() {
        this.clearScene();
        this.rooms = [];
        
        if (this.camera) {
            this.camera.position.set(5, 5, 5);
            this.controls.target.set(0, 0, 0);
            this.controls.update();
        }
    }
    
    enableControls() {
        if (this.controls) {
            this.controls.enabled = true;
        }
    }
    
    disableControls() {
        if (this.controls) {
            this.controls.enabled = false;
        }
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        if (this.controls) {
            this.controls.update();
        }
        
        if (this.renderer && this.scene && this.camera) {
            this.renderer.render(this.scene, this.camera);
        }
    }
    
    onWindowResize() {
        if (!this.isInitialized) return;
        
        const containerRect = this.container.getBoundingClientRect();
        const width = containerRect.width;
        const height = 600;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }
    
    applyStyle(style) {
        this.currentStyle = style;
        
        if (!this.isInitialized) return;
        
        this.meshes.forEach(mesh => {
            if (mesh.userData.type === 'wall') {
                if (mesh.material) {
                    mesh.material.color.setHex(style.wallColor);
                }
            } else if (mesh.userData.type === 'floor') {
                if (mesh.material) {
                    mesh.material.color.setHex(style.floorColor);
                }
            } else if (mesh.userData.type === 'furniture') {
                if (mesh.material) {
                    mesh.material.color.setHex(style.furnitureColor);
                }
            }
        });
        
        this.scene.children.forEach(child => {
            if (child.type === 'AmbientLight' && this.ambientLight) {
                this.ambientLight.intensity = style.ambientIntensity;
            }
            if (child.type === 'DirectionalLight' && this.directionalLight) {
                this.directionalLight.intensity = style.directionalIntensity;
            }
        });
    }
    
    updateScene() {
        if (this.scene && this.camera && this.renderer) {
            this.renderer.render(this.scene, this.camera);
        }
    }
}
