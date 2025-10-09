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
            // First, create or get a session
            const sessionResponse = await fetch(`${this.baseURL}/chat/sessions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.accessToken}`
                }
            });

            if (!sessionResponse.ok) {
                const error = await sessionResponse.json();
                throw new Error(error.detail || 'Failed to create chat session');
            }

            const { session_id } = await sessionResponse.json();

            // Now use the chat query endpoint with the session ID
            const response = await fetch(`${this.baseURL}/chat/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.accessToken}`
                },
                body: JSON.stringify({
                    query: searchParams.query || '',
                    session_id: session_id,
                    limit: searchParams.limit || 10
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Check if the response contains products or similar_products
                let products = data.products || data.similar_products || [];
                
                // Remove duplicate products based on product ID or name
                const uniqueProducts = [];
                const seenIds = new Set();
                
                products.forEach(product => {
                    const idKey = product.id || product.name; // Use ID if available, otherwise name
                    if (!seenIds.has(idKey)) {
                        seenIds.add(idKey);
                        uniqueProducts.push(product);
                    }
                });
                
                return { 
                    success: true, 
                    data: {
                        results: uniqueProducts,
                        count: uniqueProducts.length
                    } 
                };
            } else {
                return { 
                    success: false, 
                    error: data.detail || 'Search failed' 
                };
            }
        } catch (error) {
            console.error('Search error:', error);
            return { 
                success: false, 
                error: error.message || 'Failed to perform search' 
            };
        }
    }

    async uploadProducts(productsData) {
        if (!this.accessToken) {
            return { success: false, error: 'Please login first' };
        }

        try {
            // Extract the products array if it's wrapped in an object
            let productsArray;
            if (productsData && productsData.products && Array.isArray(productsData.products)) {
                productsArray = productsData.products;
            } else if (Array.isArray(productsData)) {
                productsArray = productsData;
            } else {
                return { success: false, error: 'Invalid products data format' };
            }

            // Create a JSON file for upload
            const jsonContent = JSON.stringify(productsArray, null, 2);
            const blob = new Blob([jsonContent], { type: 'application/json' });
            const file = new File([blob], 'products.json', { type: 'application/json' });
            
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${this.baseURL}/products/upload`, {
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
            // First, create or get a session
            const sessionResponse = await fetch(`${this.baseURL}/chat/sessions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.accessToken}`
                }
            });

            if (!sessionResponse.ok) {
                const error = await sessionResponse.json();
                throw new Error(error.detail || 'Failed to create chat session');
            }

            const { session_id } = await sessionResponse.json();

            // Now use the chat query endpoint with the session ID and image
            const response = await fetch(`${this.baseURL}/chat/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.accessToken}`
                },
                body: JSON.stringify({
                    query: "", // Empty query for image search
                    image: imageData,
                    session_id: session_id,
                    limit: searchParams.limit || 10
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Check if the response contains products or similar_products
                const products = data.products || data.similar_products || [];
                
                return { 
                    success: true, 
                    data: {
                        results: products,
                        count: products.length
                    } 
                };
            } else {
                return { success: false, error: data.detail || 'Image search failed' };
            }
        } catch (error) {
            console.error('Image search error:', error);
            return { success: false, error: error.message || 'Failed to perform image search' };
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
        this.jsonData = null;
        this.jsonFile = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateUI();
        this.setupDragAndDrop();
        // Initialize upload section
        this.setUploadMode('json');
        // Setup periodic authentication check
        this.setupAuthCheck();
        // Setup global error handler for 401 responses
        this.setupGlobalErrorHandler();
    }

    setupAuthCheck() {
        // Check authentication status every 30 seconds
        setInterval(() => {
            if (this.api.isAuthenticated() && !this.api.getUserInfo()) {
                // Token exists but user info is missing, might be expired
                this.api.logout();
                this.updateUI();
                this.showStatus('Session expired. Please login again.', 'error');
            }
        }, 30000);
    }

    setupGlobalErrorHandler() {
        // Intercept fetch responses to catch 401 errors globally
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            const response = await originalFetch(...args);
            if (response.status === 401) {
                // Auto logout on 401 response
                this.api.logout();
                this.updateUI();
                this.showStatus('Session expired. Please login again.', 'error');
            }
            return response;
        };
    }

    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', (e) => this.switchTab(e.target.textContent.toLowerCase(), e));
        });

        // Search mode switching
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.setSearchMode(e.target.textContent.toLowerCase().split(' ')[0], e));
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

        // Prevent upload button clicks if not authenticated
        this.setupUploadButtonProtection();
    }

    setupUploadButtonProtection() {
        // Add authentication check to upload buttons
        const uploadJsonBtn = document.querySelector('#jsonUpload .btn');
        if (uploadJsonBtn) {
            uploadJsonBtn.addEventListener('click', (e) => {
                if (!this.api.isAuthenticated()) {
                    e.preventDefault();
                    this.showStatus('Please login first to upload products', 'error');
                    return;
                }
            });
        }

        const uploadManualBtn = document.querySelector('#manualEntry .btn');
        if (uploadManualBtn) {
            uploadManualBtn.addEventListener('click', (e) => {
                if (!this.api.isAuthenticated()) {
                    e.preventDefault();
                    this.showStatus('Please login first to add products', 'error');
                    return;
                }
            });
        }
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
        const uploadSection = document.getElementById('uploadSection');
        const uploadLoginRequired = document.getElementById('uploadLoginRequired');

        if (isAuthenticated) {
            authSection.style.display = 'none';
            userInfoSection.classList.add('active');
            searchSection.classList.add('active');
            uploadSection.classList.add('active'); // Show upload section for authenticated users
            
            if (uploadLoginRequired) {
                uploadLoginRequired.style.display = 'none';
            }
            
            if (userInfo) {
                document.getElementById('usernameDisplay').textContent = userInfo.username;
                document.getElementById('emailDisplay').textContent = userInfo.email;
            }
        } else {
            authSection.style.display = 'block';
            userInfoSection.classList.remove('active');
            searchSection.classList.remove('active');
            uploadSection.classList.remove('active'); // Hide upload section for unauthenticated users
            document.getElementById('resultsSection').style.display = 'none';
            
            if (uploadLoginRequired) {
                uploadLoginRequired.style.display = 'block';
            }
        }
    }

    switchTab(tab, event) {
        // Update tab buttons
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        if (event && event.target) {
            event.target.classList.add('active');
        }

        // Show/hide forms
        if (tab === 'login') {
            document.getElementById('loginForm').style.display = 'block';
            document.getElementById('registerForm').style.display = 'none';
        } else {
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('registerForm').style.display = 'block';
        }
    }

    setSearchMode(mode, event) {
        this.currentSearchMode = mode;
        
        // Update button states
        document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
        if (event && event.target) {
            event.target.classList.add('active');
        }

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

    setUploadMode(mode, event = null) {
        // Update button states
        document.querySelectorAll('#uploadSection .mode-btn').forEach(btn => btn.classList.remove('active'));
        if (event && event.target) {
            event.target.classList.add('active');
        } else {
            // Set default active button
            const defaultBtn = mode === 'json' ? 
                document.querySelector('#uploadSection .mode-btn:first-child') :
                document.querySelector('#uploadSection .mode-btn:last-child');
            if (defaultBtn) defaultBtn.classList.add('active');
        }

        // Show/hide upload sections
        const jsonUpload = document.getElementById('jsonUpload');
        const manualEntry = document.getElementById('manualEntry');

        if (mode === 'json') {
            jsonUpload.style.display = 'block';
            manualEntry.style.display = 'none';
        } else {
            jsonUpload.style.display = 'none';
            manualEntry.style.display = 'block';
        }
    }

    async uploadJsonProducts() {
        if (!this.api.isAuthenticated()) {
            this.showStatus('Please login first to upload products', 'error');
            return;
        }
        
        if (!this.jsonData) {
            this.showStatus('Please select a JSON file first', 'error');
            return;
        }
        
        this.showLoading('Uploading products...');
        
        try {
            const result = await this.api.uploadProducts({ products: this.jsonData });
            
            if (result.success) {
                this.showStatus(`Successfully uploaded ${result.details?.inserted_count || 0} products!`, 'success');
                // Clear the form
                this.jsonData = null;
                this.jsonFile = null;
                document.getElementById('jsonFile').value = '';
                const jsonPreview = document.getElementById('jsonPreview');
                if (jsonPreview) {
                    jsonPreview.style.display = 'none';
                }
            } else {
                this.showStatus('Upload failed: ' + result.error, 'error');
            }
        } catch (error) {
            this.showStatus('Upload error: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    addManualProduct() {
        this.handleManualProductSubmit();
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
            const loginTab = document.querySelector('.tab');
            if (loginTab) {
                loginTab.click();
            }
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
        // Map frontend categories to backend categories
        const categoryMapping = {
            'electronics': 'Smartphones',  // Map electronics to Smartphones as primary electronics category
            'clothing': 'Smartwatches',    // Map clothing to Smartwatches as closest wearable tech
            'home': 'Smart Speakers',      // Map home to Smart Speakers as smart home devices
            'books': 'Tablets',            // Map books to Tablets as reading devices
            'sports': 'Smartwatches'       // Map sports to Smartwatches as fitness tracking
        };
        
        const backendCategory = categoryMapping[category] || category;
        
        // Set the search query to a generic term and use the backend category as the category filter
        const searchQuery = document.getElementById('searchQuery');
        if (searchQuery) {
            searchQuery.value = 'products';
        }
        
        // Perform search with the mapped category
        this.performSearchWithCategory(backendCategory);
    }
    
    async performSearchWithCategory(category) {
        if (!this.api.isAuthenticated()) {
            this.showStatus('Please login first', 'error');
            return;
        }

        const limit = parseInt(document.getElementById('limit')?.value) || 10;

        this.showLoading(true);

        let searchParams = {
            query: 'products',  // Generic query
            category: category,  // Use the specific category
            limit: limit
        };

        try {
            const result = await this.api.searchJewelry(searchParams);
            
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

    handleImageUpload(event) {
        const file = event.target.files[0];
        if (file) {
            this.handleImageFile(file);
        }
    }

    async handleJSONUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        this.jsonFile = file;
        this.showLoading('Processing JSON file...');
        
        try {
            const fileContent = await this.readFileAsText(file);
            this.jsonData = JSON.parse(fileContent);
            
            // Show preview
            const jsonPreview = document.getElementById('jsonPreview');
            const jsonContent = document.getElementById('jsonContent');
            
            if (jsonPreview && jsonContent) {
                jsonContent.textContent = JSON.stringify(this.jsonData, null, 2);
                jsonPreview.style.display = 'block';
            }
            
            this.showStatus(`JSON file loaded: ${Array.isArray(this.jsonData) ? this.jsonData.length : 'Unknown'} products found`, 'success');
        } catch (error) {
            this.showStatus('Error processing JSON file: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async handleManualProductSubmit() {
        if (!this.api.isAuthenticated()) {
            this.showStatus('Please login first to add products', 'error');
            return;
        }
        
        // Get values directly from form fields since they don't have name attributes
        const productName = document.getElementById('productName');
        const productCategory = document.getElementById('productCategory');
        const productDescription = document.getElementById('productDescription');
        const productPrice = document.getElementById('productPrice');
        const productImage = document.getElementById('productImage');

        if (!productName || !productCategory || !productDescription || !productPrice || !productImage) {
            this.showStatus('Form fields not found', 'error');
            return;
        }

        const product = {
            name: productName.value,
            category: productCategory.value,
            description: productDescription.value,
            price: parseFloat(productPrice.value) || 0,
            image_url: productImage.value
        };

        this.showLoading('Adding product...');
        
        try {
            const result = await this.api.uploadProducts({ products: [product] });
            
            if (result.success) {
                this.showStatus('Product added successfully!', 'success');
                // Clear form fields
                productName.value = '';
                productCategory.value = '';
                productDescription.value = '';
                productPrice.value = '';
                productImage.value = '';
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
            const uploadText = document.getElementById('uploadText');
            const imagePreview = document.getElementById('imagePreview');
            if (uploadText && imagePreview) {
                uploadText.style.display = 'none';
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
            }
            this.uploadedImage = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    async performSearch() {
        const searchQuery = document.getElementById('searchQuery');
        const minScore = document.getElementById('minScore');
        const limit = document.getElementById('limit');

        if (!searchQuery || !minScore || !limit) {
            this.showStatus('Search form elements not found', 'error');
            return;
        }

        const query = searchQuery.value;
        const minScoreValue = parseFloat(minScore.value);
        const limitValue = parseInt(limit.value);

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
            limit: limitValue
        };

        try {
            let result;
            
            if (this.currentSearchMode === 'text' || this.currentSearchMode === 'smart') {
                searchParams.query = query;
                result = await this.api.searchJewelry(searchParams);
            } else if (this.currentSearchMode === 'image') {
                result = await this.api.searchByImage(this.uploadedImage, {
                    limit: limitValue
                });
            }

            if (result && result.success) {
                this.displayResults(result.data.results || result.data);
            } else {
                this.showStatus(result?.error || 'Search failed', 'error');
            }
        } catch (error) {
            this.showStatus('Search failed. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    handleSearchResult(result) {
        if (result && result.success) {
            this.displayResults(result.data.results || result.data);
        } else {
            this.showStatus(result?.error || 'Search failed', 'error');
        }
    }

    displayResults(results) {
        const resultsContainer = document.getElementById('resultsContainer');
        const resultsSection = document.getElementById('resultsSection');

        if (!resultsContainer || !resultsSection) {
            console.error('Results container or section not found');
            return;
        }

        if (!results || results.length === 0) {
            resultsContainer.innerHTML = '<p style="text-align: center; color: #666;">No results found. Try adjusting your search criteria.</p>';
            resultsSection.style.display = 'block';
            return;
        }

        resultsContainer.innerHTML = results.map(item => {
            // Determine the image source
            let imageSrc = '';
            
            if (item.image_path) {
                imageSrc = item.image_path;
            } else if (item.image_url) {
                // Check if it's base64 data (starts with common base64 patterns)
                if (item.image_url.match(/^[A-Za-z0-9+/]{20,}/)) {
                    // It's base64 data, create a data URI
                    imageSrc = `data:image/jpeg;base64,${item.image_url}`;
                } else {
                    // It's a regular URL
                    imageSrc = item.image_url;
                }
            } else if (item.image) {
                imageSrc = item.image;
            } else {
                // Fallback to placeholder
                imageSrc = `https://via.placeholder.com/300x200?text=${encodeURIComponent(item.name)}`;
            }
            
            return `
            <div class="result-card">
                <img src="${imageSrc}" 
                     alt="${item.name}"
                     onerror="this.onerror=null; this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDMwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjRjBGMEYwIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTAwIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiM2NjY2NjYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2Vt">${encodeURIComponent(item.name)}</text>
                </svg>';">
                <h3>${item.name}</h3>
                <p><strong>Category:</strong> ${item.category}</p>
                <p><strong>Description:</strong> <span class="description">${item.description || 'No description available'}</span></p>
                <p><strong>Price:</strong> <span class="price">$${item.price || 'N/A'}</span></p>
                <p><strong>Similarity:</strong> <span class="score">${item.similarity_score ? `${(item.similarity_score * 100).toFixed(1)}%` : 'N/A'}</span></p>
            </div>
        `;
        }).join('');

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