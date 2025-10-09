// Jewelry Store API Client
class JewelryAPI {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
        this.accessToken = null;
        this.userInfo = null;
        this.loadAuthData();
    }

    // Authentication methods
    async login(username, password) {
        try {
            // Send as JSON since backend expects JSON with username field
            const loginData = {
                username: username,
                password: password
            };

            const response = await fetch(`${this.baseURL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loginData)
            });

            const data = await response.json();

            if (response.ok) {
                this.accessToken = data.access_token;
                this.userInfo = { username, email: data.email || username };
                this.saveAuthData();
                return { success: true, data };
            } else {
                return { success: false, error: data.detail || 'Login failed' };
            }
        } catch (error) {
            return { success: false, error: 'Connection error. Please check if the server is running.' };
        }
    }

    async register(userData) {
        try {
            const response = await fetch(`${this.baseURL}/auth/signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (response.ok) {
                return { success: true, data };
            } else {
                return { success: false, error: data.detail || 'Registration failed' };
            }
        } catch (error) {
            return { success: false, error: 'Connection error. Please check if the server is running.' };
        }
    }

    logout() {
        this.accessToken = null;
        this.userInfo = null;
        this.clearAuthData();
    }

    // Search methods
    async searchJewelry(searchParams) {
        if (!this.accessToken) {
            return { success: false, error: 'Please login first' };
        }

        try {
            // Create FormData to match backend expectations
            const formData = new FormData();
            if (searchParams.query) formData.append('query', searchParams.query);
            if (searchParams.category) formData.append('category', searchParams.category);
            if (searchParams.limit) formData.append('limit', searchParams.limit || 10);

            const response = await fetch(`${this.baseURL}/jewelry/search`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.accessToken}`
                    // Don't set Content-Type for FormData - let browser set it
                },
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                return { success: true, data };
            } else {
                return { success: false, error: data.detail || 'Search failed' };
            }
        } catch (error) {
            return { success: false, error: 'Connection error. Please check if the server is running.' };
        }
    }

    async uploadProducts(productsData) {
        if (!this.accessToken) {
            return { success: false, error: 'Please login first' };
        }

        try {
            const response = await fetch(`${this.baseURL}/products/upload`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.accessToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(productsData)
            });

            const data = await response.json();

            if (response.ok) {
                return { success: true, data };
            } else {
                return { success: false, error: data.detail || 'Upload failed' };
            }
        } catch (error) {
            return { success: false, error: 'Connection error. Please check if the server is running.' };
        }
    }

    async searchByImage(imageData, searchParams = {}) {
        if (!this.accessToken) {
            return { success: false, error: 'Please login first' };
        }

        try {
            // Create FormData for multipart/form-data request
            const formData = new FormData();
            
            // Convert base64 image to blob and append as file
            const imageResponse = await fetch(imageData);
            const blob = await imageResponse.blob();
            
            // Determine the correct file type from the data URL
            const mimeType = imageData.split(';')[0].split(':')[1] || 'image/jpeg';
            const extension = mimeType.split('/')[1];
            const fileName = `search_image.${extension}`;
            
            const file = new File([blob], fileName, { type: mimeType });
            formData.append('image', file);
            
            // Add other parameters
            if (searchParams.query) formData.append('query', searchParams.query);
            if (searchParams.category) formData.append('category', searchParams.category);
            if (searchParams.limit) formData.append('limit', searchParams.limit.toString());

            const response = await fetch(`${this.baseURL}/jewelry/search`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.accessToken}`
                    // Don't set Content-Type for FormData, let browser set it
                },
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                return { success: true, data };
            } else {
                return { success: false, error: data.detail || 'Image search failed' };
            }
        } catch (error) {
            return { success: false, error: 'Connection error. Please check if the server is running.' };
        }
    }

    // Utility methods
    saveAuthData() {
        if (this.accessToken && this.userInfo) {
            localStorage.setItem('access_token', this.accessToken);
            localStorage.setItem('user_info', JSON.stringify(this.userInfo));
        }
    }

    loadAuthData() {
        const token = localStorage.getItem('access_token');
        const user = localStorage.getItem('user_info');
        
        if (token && user) {
            this.accessToken = token;
            this.userInfo = JSON.parse(user);
        }
    }

    clearAuthData() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_info');
    }

    isAuthenticated() {
        return !!this.accessToken;
    }

    getUserInfo() {
        return this.userInfo;
    }
}

// UI Controller
class UIController {
    constructor(api) {
        this.api = api;
        this.currentSearchMode = 'text';
        this.uploadedImage = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateUI();
        this.setupDragAndDrop();
    }

    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', (e) => this.switchTab(e.target.textContent.toLowerCase()));
        });

        // Search mode switching
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.setSearchMode(e.target.textContent.toLowerCase().split(' ')[0]));
        });

        // Quick filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.quickSearch(e.target.textContent.toLowerCase().split(' ')[1]));
        });

        // Form submissions
        document.getElementById('loginBtn')?.addEventListener('click', () => this.login());
        document.getElementById('registerBtn')?.addEventListener('click', () => this.register());
        document.getElementById('logoutBtn')?.addEventListener('click', () => this.logout());
        document.getElementById('searchBtn')?.addEventListener('click', () => this.performSearch());

        // Enter key handling
        document.getElementById('searchQuery')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && this.currentSearchMode === 'text') {
                this.performSearch();
            }
        });

        // Image upload
        document.getElementById('imageFile')?.addEventListener('change', (e) => this.handleImageUpload(e));

        // JSON file upload
        document.getElementById('jsonFile')?.addEventListener('change', (e) => this.handleJSONUpload(e));

        // Manual product form
        document.getElementById('manualProductForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleManualProductSubmit();
        });
    }

    setupDragAndDrop() {
        const uploadArea = document.querySelector('.file-upload');
        if (uploadArea) {
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });

            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.handleImageFile(files[0]);
                }
            });
        }
    }

    // UI Update methods
    updateUI() {
        const isAuthenticated = this.api.isAuthenticated();
        const userInfo = this.api.getUserInfo();

        // Update auth section visibility
        const authSection = document.getElementById('authSection');
        const userInfoSection = document.getElementById('userInfo');
        const searchSection = document.getElementById('searchSection');

        if (isAuthenticated) {
            authSection.style.display = 'none';
            userInfoSection.classList.add('active');
            searchSection.classList.add('active');
            
            if (userInfo) {
                document.getElementById('usernameDisplay').textContent = userInfo.username;
                document.getElementById('emailDisplay').textContent = userInfo.email;
            }
        } else {
            authSection.style.display = 'block';
            userInfoSection.classList.remove('active');
            searchSection.classList.remove('active');
            document.getElementById('resultsSection').style.display = 'none';
        }
    }

    switchTab(tab) {
        // Update tab buttons
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        event.target.classList.add('active');

        // Show/hide forms
        if (tab === 'login') {
            document.getElementById('loginForm').style.display = 'block';
            document.getElementById('registerForm').style.display = 'none';
        } else {
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('registerForm').style.display = 'block';
        }
    }

    setSearchMode(mode) {
        this.currentSearchMode = mode;
        
        // Update button states
        document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');

        // Show/hide input fields
        const textInput = document.getElementById('textSearchInput');
        const imageInput = document.getElementById('imageSearchInput');

        if (mode === 'text' || mode === 'smart') {
            textInput.style.display = 'block';
            imageInput.style.display = 'none';
        } else {
            textInput.style.display = 'none';
            imageInput.style.display = 'block';
        }
    }

    // Authentication methods
    async login() {
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        if (!username || !password) {
            this.showStatus('Please enter both username and password', 'error');
            return;
        }

        const result = await this.api.login(username, password);
        
        if (result.success) {
            this.showStatus('Login successful!', 'success');
            this.updateUI();
        } else {
            this.showStatus(result.error, 'error');
        }
    }

    async register() {
        const userData = {
            username: document.getElementById('regUsername').value,
            email: document.getElementById('regEmail').value,
            password: document.getElementById('regPassword').value,
            full_name: document.getElementById('regFullName').value
        };

        if (!userData.username || !userData.email || !userData.password) {
            this.showStatus('Please fill in all required fields', 'error');
            return;
        }

        const result = await this.api.register(userData);
        
        if (result.success) {
            this.showStatus('Registration successful! Please login.', 'success');
            // Switch to login tab
            document.querySelector('.tab').click();
        } else {
            this.showStatus(result.error, 'error');
        }
    }

    logout() {
        this.api.logout();
        this.showStatus('Logged out successfully', 'info');
        this.updateUI();
    }

    // Search methods
    quickSearch(category) {
        document.getElementById('searchQuery').value = category;
        this.performSearch();
    }

    handleImageUpload(event) {
        const file = event.target.files[0];
        if (file) {
            this.handleImageFile(file);
        }
    }

    async handleJSONUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        this.showLoading('Uploading products...');
        
        try {
            const fileContent = await this.readFileAsText(file);
            const productsData = JSON.parse(fileContent);
            
            const result = await this.api.uploadProducts(productsData);
            
            if (result.success) {
                this.showStatus(`Successfully uploaded ${result.data.products_uploaded || 0} products!`, 'success');
            } else {
                this.showStatus('Upload failed: ' + result.error, 'error');
            }
        } catch (error) {
            this.showStatus('Error processing file: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async handleManualProductSubmit() {
        const form = document.getElementById('manualProductForm');
        const formData = new FormData(form);
        
        const product = {
            name: formData.get('productName'),
            category: formData.get('productCategory'),
            description: formData.get('productDescription'),
            price: parseFloat(formData.get('productPrice')) || 0,
            image_url: formData.get('productImageUrl')
        };

        this.showLoading('Adding product...');
        
        try {
            const result = await this.api.uploadProducts({ products: [product] });
            
            if (result.success) {
                this.showStatus('Product added successfully!', 'success');
                form.reset();
            } else {
                this.showStatus('Failed to add product: ' + result.error, 'error');
            }
        } catch (error) {
            this.showStatus('Error adding product: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async readFileAsText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = e => resolve(e.target.result);
            reader.onerror = reject;
            reader.readAsText(file);
        });
    }

    handleImageFile(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('uploadText').style.display = 'none';
            document.getElementById('imagePreview').src = e.target.result;
            document.getElementById('imagePreview').style.display = 'block';
            this.uploadedImage = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    async performSearch() {
        const query = document.getElementById('searchQuery').value;
        const minScore = parseFloat(document.getElementById('minScore').value);
        const limit = parseInt(document.getElementById('limit').value);

        if (!this.api.isAuthenticated()) {
            this.showStatus('Please login first', 'error');
            return;
        }

        if (!query.trim() && this.currentSearchMode !== 'image') {
            this.showStatus('Please enter a search query', 'error');
            return;
        }

        if (this.currentSearchMode === 'image' && !this.uploadedImage) {
            this.showStatus('Please upload an image first', 'error');
            return;
        }

        this.showLoading(true);

        let searchParams = {
            limit: limit
        };

        try {
            let result;
            
            if (this.currentSearchMode === 'text' || this.currentSearchMode === 'smart') {
                searchParams.query = query;
                result = await this.api.searchJewelry(searchParams);
            } else if (this.currentSearchMode === 'image') {
                result = await this.api.searchByImage(this.uploadedImage, {
                    limit: limit
                });
            }

            if (result.success) {
                this.displayResults(result.data.results || result.data);
            } else {
                this.showStatus(result.error, 'error');
            }
        } catch (error) {
            this.showStatus('Search failed. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    handleSearchResult(result) {
        if (result.success) {
            this.displayResults(result.data.results || result.data);
        } else {
            this.showStatus(result.error, 'error');
        }
    }

    displayResults(results) {
        const resultsContainer = document.getElementById('resultsContainer');
        const resultsSection = document.getElementById('resultsSection');

        if (!results || results.length === 0) {
            resultsContainer.innerHTML = '<p style="text-align: center; color: #666;">No results found. Try adjusting your search criteria.</p>';
            resultsSection.style.display = 'block';
            return;
        }

        resultsContainer.innerHTML = results.map(item => `
            <div class="result-card">
                <img src="${item.image_url || 'https://via.placeholder.com/300x200?text=Product'}" 
                     alt="${item.name}" 
                     onerror="this.src='https://via.placeholder.com/300x200?text=Product'">
                <h3>${item.name}</h3>
                <p><strong>Category:</strong> ${item.category}</p>
                <p><strong>Description:</strong> ${item.description || 'No description available'}</p>
                <p><strong>Price:</strong> <span class="price">$${item.price || 'N/A'}</span></p>
                <p><strong>Similarity:</strong> <span class="score">${(item.similarity_score * 100).toFixed(1)}%</span></p>
            </div>
        `).join('');

        resultsSection.style.display = 'block';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Utility methods
    showStatus(message, type) {
        const statusElement = document.getElementById('statusMessage');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.className = `status ${type}`;
            statusElement.style.display = 'block';
            
            setTimeout(() => {
                statusElement.style.display = 'none';
            }, 5000);
        }
    }

    showLoading(show) {
        const loadingElement = document.getElementById('loadingIndicator');
        const searchBtn = document.getElementById('searchBtn');
        
        if (loadingElement && searchBtn) {
            if (show) {
                loadingElement.style.display = 'block';
                searchBtn.disabled = true;
            } else {
                loadingElement.style.display = 'none';
                searchBtn.disabled = false;
            }
        }
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    const api = new JewelryAPI();
    const ui = new UIController(api);
    
    // Make API globally available for debugging
    window.jewelryAPI = api;
    window.jewelryUI = ui;
});