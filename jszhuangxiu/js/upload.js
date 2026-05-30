export class ImageUploader {
    constructor(uploadArea, fileInput) {
        this.uploadArea = uploadArea;
        this.fileInput = fileInput;
        this.imageLoadedCallbacks = [];
        this.uploadErrorCallbacks = [];
        this.currentImage = null;
        
        this.init();
    }
    
    init() {
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        
        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFile(e.target.files[0]);
            }
        });
        
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });
        
        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('dragover');
        });
        
        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFile(files[0]);
            }
        });
    }
    
    handleFile(file) {
        const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        
        if (!validTypes.includes(file.type)) {
            this.emitError('请上传 JPG 或 PNG 格式的图片');
            return;
        }
        
        if (file.size > 10 * 1024 * 1024) {
            this.emitError('图片大小不能超过 10MB');
            return;
        }
        
        const reader = new FileReader();
        
        reader.onload = (e) => {
            this.loadImage(e.target.result);
        };
        
        reader.onerror = () => {
            this.emitError('图片加载失败，请重试');
        };
        
        reader.readAsDataURL(file);
    }
    
    loadImage(dataUrl) {
        const img = new Image();
        
        img.onload = () => {
            this.currentImage = img;
            this.emitImageLoaded(img);
        };
        
        img.onerror = () => {
            this.emitError('图片加载失败，请重试');
        };
        
        img.src = dataUrl;
    }
    
    onImageLoaded(callback) {
        this.imageLoadedCallbacks.push(callback);
    }
    
    onUploadError(callback) {
        this.uploadErrorCallbacks.push(callback);
    }
    
    emitImageLoaded(image) {
        this.imageLoadedCallbacks.forEach(callback => callback(image));
    }
    
    emitError(message) {
        this.uploadErrorCallbacks.forEach(callback => callback(message));
    }
    
    getImageElement() {
        return this.currentImage;
    }
    
    reset() {
        this.currentImage = null;
        this.fileInput.value = '';
    }
}
