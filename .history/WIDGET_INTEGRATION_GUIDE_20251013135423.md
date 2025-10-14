# 💎 Jewellery Chatbot Widget Integration Guide

## Overview

The Jewellery Chatbot Widget is a powerful, customizable chatbot that can be easily integrated into any website to provide AI-powered jewellery assistance. This widget connects to your existing chatbot API and provides a seamless conversational experience for your customers.

## 🚀 Quick Start (2 Minutes)

### Step 1: Copy the Widget Script
Download the `jewellery-chatbot-widget.js` file and place it in your website's directory.

### Step 2: Add to Your HTML
Add these two lines to your HTML page:

```html
<!-- Add before closing </body> tag -->
<script src="jewellery-chatbot-widget.js"></script>
<script>
    window.JewelleryChatbot.init({
        apiUrl: 'http://localhost:8000',  // Your API URL
        position: 'bottom-right',        // Widget position
        theme: 'blue'                      // Color theme
    });
</script>
```

### Step 3: That's It! 🎉
Your chatbot widget is now live on your website!

## 📋 Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `apiUrl` | string | **Required** | Your API base URL (e.g., 'https://your-domain.com/api') |
| `position` | string | 'bottom-right' | Widget position: 'bottom-right', 'bottom-left', 'top-right', 'top-left' |
| `theme` | string | 'blue' | Color theme: 'blue', 'purple', 'green', 'custom' |
| `welcomeMessage` | string | 'Hello! I'm here to help...' | Custom welcome message |
| `placeholderText` | string | 'Ask about jewellery...' | Input placeholder text |
| `autoOpen` | boolean | false | Auto-open widget on page load |
| `customColors` | object | {} | Custom color scheme (when theme is 'custom') |
| `maxFileSize` | number | 5242880 | Maximum file size for uploads (5MB default) |
| `allowedFileTypes` | array | ['image/jpeg', ...] | Allowed file types for uploads |

## 🎨 Themes and Customization

### Built-in Themes
```javascript
// Blue theme (default)
theme: 'blue'

// Purple theme
theme: 'purple'

// Green theme  
theme: 'green'
```

### Custom Theme
```javascript
theme: 'custom',
customColors: {
    primary: '#ff6b6b',      // Main color
    secondary: '#4ecdc4'     // Secondary color
}
```

### Position Options
```javascript
position: 'bottom-right'   // Default
position: 'bottom-left'
position: 'top-right'
position: 'top-left'
```

## 🔧 Advanced Integration Examples

### Example 1: E-commerce Product Page
```html
<!DOCTYPE html>
<html>
<head>
    <title>Gold Rings - Jewellery Store</title>
</head>
<body>
    <!-- Your product page content -->
    
    <!-- Chatbot Widget -->
    <script src="jewellery-chatbot-widget.js"></script>
    <script>
        window.JewelleryChatbot.init({
            apiUrl: 'https://api.yourstore.com',
            position: 'bottom-right',
            theme: 'purple',
            welcomeMessage: 'Looking for the perfect gold ring? I can help!',
            placeholderText: 'Ask about gold rings, sizes, or customization...'
        });
    </script>
</body>
</html>
```

### Example 2: Multi-page Website
```html
<!-- Add to your shared footer template -->
<script src="/assets/js/jewellery-chatbot-widget.js"></script>
<script>
    // Configuration can be different per page
    const pageConfig = {
        '/rings': {
            welcomeMessage: 'Find your perfect ring!',
            placeholderText: 'Ask about engagement rings...'
        },
        '/necklaces': {
            welcomeMessage: 'Discover beautiful necklaces!',
            placeholderText: 'Ask about necklace styles...'
        }
    };
    
    const currentPage = window.location.pathname;
    const config = {
        apiUrl: 'https://api.yourstore.com',
        position: 'bottom-right',
        theme: 'blue',
        ...pageConfig[currentPage]
    };
    
    window.JewelleryChatbot.init(config);
</script>
```

### Example 3: Dynamic Loading
```javascript
// Load widget only when needed
function loadChatbot() {
    const script = document.createElement('script');
    script.src = 'jewellery-chatbot-widget.js';
    script.onload = function() {
        window.JewelleryChatbot.init({
            apiUrl: 'https://api.yourstore.com',
            position: 'bottom-right',
            theme: 'blue'
        });
    };
    document.head.appendChild(script);
}

// Load when user clicks "Chat with us" button
document.getElementById('chat-button').addEventListener('click', loadChatbot);
```

## 📱 Responsive Design

The widget is fully responsive and adapts to different screen sizes:

- **Desktop**: 380px × 600px chat window
- **Mobile**: Full-screen overlay with swipe gestures
- **Tablet**: Optimized layout for touch interaction

## 🔒 Security Considerations

### CORS Configuration
Ensure your API server has proper CORS headers:
```
Access-Control-Allow-Origin: https://your-domain.com
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

### HTTPS
Always use HTTPS in production:
```javascript
// ✅ Good
apiUrl: 'https://api.yourstore.com'

// ❌ Avoid in production
apiUrl: 'http://localhost:8000'
```

### Rate Limiting
Implement rate limiting on your API endpoints to prevent abuse.

## 🛠️ API Endpoints Required

The widget expects these endpoints on your API server:

```
POST   /auth/signup          - User registration
POST   /auth/login           - User authentication  
POST   /chat/sessions        - Create chat session
POST   /chat/query           - Send chat message
GET    /chat/history/{id}    - Get chat history
GET    /health               - API health check
```

### Expected Response Formats

#### Login Response
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user_id": "12345",
    "token_type": "bearer"
}
```

#### Chat Query Response
```json
{
    "response": "Here are some beautiful gold rings...",
    "products": [
        {
            "name": "Classic Gold Ring",
            "price": 299.99,
            "description": "18k gold ring with elegant design",
            "image_url": "https://example.com/ring.jpg"
        }
    ]
}
```

## 🎯 JavaScript API Methods

### Public Methods
```javascript
// Open chat window
window.JewelleryChatbot.open();

// Close chat window
window.JewelleryChatbot.close();

// Send a message programmatically
window.JewelleryChatbot.send('Show me diamond necklaces');

// Change theme dynamically
window.JewelleryChatbot.setTheme('purple');

// Change position
window.JewelleryChatbot.setPosition('bottom-left');
```

### Event Handling
```javascript
// Listen for widget events (future enhancement)
document.addEventListener('jewelleryChatbot:open', function() {
    console.log('Chat widget opened');
});

document.addEventListener('jewelleryChatbot:message', function(event) {
    console.log('New message:', event.detail);
});
```

## 🎨 Custom Styling

### Override CSS Classes
```css
/* Custom widget button */
.jewellery-chatbot-button {
    background: linear-gradient(45deg, #ff6b6b, #ff8e8e) !important;
    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3) !important;
}

/* Custom chat header */
.jewellery-chatbot-header {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
}

/* Custom message bubbles */
.jewellery-chatbot-message.user .jewellery-chatbot-message-bubble {
    background: #ff6b6b !important;
}
```

### Custom Product Cards
```css
.jewellery-chatbot-product {
    border: 2px solid #ff6b6b !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
}
```

## 🔧 Troubleshooting

### Common Issues

#### Widget Not Appearing
```javascript
// Check browser console for errors
console.log(window.JewelleryChatbot);

// Verify API URL is accessible
fetch('http://localhost:8000/health')
    .then(response => console.log('API Status:', response.status))
    .catch(error => console.error('API Error:', error));
```

#### CORS Errors
- Ensure your API server allows cross-origin requests
- Check that the API URL is correct and accessible
- Verify HTTPS/HTTP protocol matches

#### Authentication Issues
- Check that signup/login endpoints are working
- Verify JWT token generation and validation
- Ensure session management is properly configured

### Debug Mode
```javascript
// Enable debug logging (future enhancement)
window.JewelleryChatbot.init({
    apiUrl: 'http://localhost:8000',
    debug: true,  // Enable detailed logging
    // ... other options
});
```

## 📊 Analytics Integration

### Google Analytics
```javascript
// Track widget interactions
gtag('event', 'chatbot_open', {
    'event_category': 'Chatbot',
    'event_label': 'Jewellery Widget'
});

// Track messages
gtag('event', 'chatbot_message', {
    'event_category': 'Chatbot',
    'event_label': 'User Message'
});
```

### Custom Analytics
```javascript
// Send analytics to your server
function trackChatbotEvent(event, data) {
    fetch('/analytics/track', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            event: event,
            data: data,
            timestamp: new Date().toISOString()
        })
    });
}
```

## 🌐 Browser Support

- **Chrome**: 60+
- **Firefox**: 55+
- **Safari**: 12+
- **Edge**: 79+
- **Mobile browsers**: iOS Safari 12+, Chrome Mobile 60+

## 📦 File Size

- **Minified**: ~25KB
- **Gzipped**: ~8KB
- **Dependencies**: None (vanilla JavaScript)

## 🔒 Security Features

- Input sanitization to prevent XSS attacks
- File upload validation and size limits
- Secure token storage (sessionStorage)
- CORS protection
- Rate limiting support

## 🚀 Performance Optimization

### Lazy Loading
```javascript
// Load widget only when user scrolls to bottom
const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
        loadChatbot();
        observer.disconnect();
    }
});

observer.observe(document.querySelector('#footer'));
```

### Conditional Loading
```javascript
// Load only on product pages
if (window.location.pathname.includes('/products/')) {
    loadChatbot();
}
```

## 📞 Support and Customization

For custom features, additional integrations, or technical support:

1. **Check the browser console** for error messages
2. **Verify API connectivity** using the health endpoint
3. **Test with the example HTML** provided in `widget-integration-example.html`
4. **Review the API documentation** at `http://localhost:8000/docs`

## 🎯 Next Steps

1. **Test the widget** on your development environment
2. **Customize the appearance** to match your brand
3. **Deploy to production** with proper HTTPS and CORS setup
4. **Monitor performance** and user interactions
5. **Collect feedback** and iterate on the experience

---

**Happy integrating!** 🎉 The jewellery chatbot widget is now ready to help your customers find their perfect pieces.