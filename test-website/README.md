# Jewellery Chatbot Test Website

This is a complete test website demonstrating the integration of the AI-powered jewellery chatbot widget. The website showcases how the chatbot can be seamlessly integrated into a jewellery e-commerce site.

## 📁 File Structure

```
test-website/
├── index.html                    # Homepage with hero section and features
├── products.html                 # Product catalog with chatbot integration
├── contact.html                  # Contact page with form and AI assistant
├── README.md                     # This documentation file
└── assets/                       # (Optional) Images and other assets
```

## 🚀 Quick Start

1. **Ensure your chatbot server is running**:
   ```bash
   cd ..  # Go back to main directory
   python main.py
   ```

2. **Open the test website**:
   - Open `index.html` in your web browser
   - Or use a local web server:
     ```bash
     # Python 3
     python -m http.server 8080
     
     # Python 2
     python -m SimpleHTTPServer 8080
     
     # Then visit http://localhost:8080/test-website/
     ```

## 🎯 Features Demonstrated

### Homepage (`index.html`)
- **Hero Section**: Beautiful jewellery showcase with chatbot integration
- **Feature Cards**: Interactive cards with chatbot triggers
- **Chat Demo Section**: Pre-configured chat scenarios
- **Responsive Design**: Mobile-friendly layout

### Products Page (`products.html`)
- **Product Catalog**: Grid layout with jewellery items
- **Category Filtering**: Tabs for different jewellery types
- **Product Actions**: "Ask AI" buttons for each product
- **Chat Suggestions**: Quick question buttons
- **AI Integration**: Direct product inquiries to chatbot

### Contact Page (`contact.html`)
- **Contact Form**: Complete form with validation
- **Business Information**: Store details and hours
- **Quick Questions**: Pre-defined questions for AI assistant
- **Form Integration**: AI suggestions for form completion

## 🤖 Chatbot Widget Integration

Each page includes the chatbot widget with custom configurations:

### Homepage Configuration
```javascript
window.JewelleryChatbot.init({
    apiUrl: 'http://localhost:8000',
    position: 'bottom-right',
    theme: 'purple',
    welcomeMessage: 'Welcome to Elegant Jewels! 💎 I can help you explore our collection, answer questions, and find the perfect piece for you.',
    placeholderText: 'Ask about our jewellery, services, or products...',
    autoOpen: false
});
```

### Products Page Configuration
```javascript
window.JewelleryChatbot.init({
    apiUrl: 'http://localhost:8000',
    position: 'bottom-right',
    theme: 'purple',
    welcomeMessage: 'Welcome to our collection! 💎 I can help you choose the perfect jewellery piece. Ask me about any item or let me know what you\'re looking for!',
    placeholderText: 'Ask about rings, necklaces, earrings...',
    autoOpen: false
});
```

### Contact Page Configuration
```javascript
window.JewelleryChatbot.init({
    apiUrl: 'http://localhost:8000',
    position: 'bottom-right',
    theme: 'purple',
    welcomeMessage: 'Welcome! 💎 I\'m here to help with any questions about our store, services, or products. Feel free to ask me anything!',
    placeholderText: 'Ask about store hours, services, appointments...',
    autoOpen: false
});
```

## 🎨 Customization Options

### Themes
The widget supports different themes:
- `purple` (default)
- `blue`
- `green`
- `red`
- `gold`

### Positions
Available widget positions:
- `bottom-right` (default)
- `bottom-left`
- `top-right`
- `top-left`

### Custom Messages
You can customize:
- `welcomeMessage`: Initial greeting
- `placeholderText`: Input field placeholder
- `autoOpen`: Whether to open automatically

## 🔧 API Endpoints Used

The widget connects to these endpoints on your backend:

- `POST /auth/signup` - User registration
- `POST /auth/login` - User authentication
- `POST /chat/sessions` - Create chat session
- `POST /chat/query` - Send chat messages
- `GET /chat/history/{session_id}` - Get chat history
- `GET /health` - Health check

## 📱 Testing Features

### 1. Basic Chat Functionality
- Click the chat widget icon
- Type a message about jewellery
- Test product recommendations
- Try image upload (if enabled)

### 2. Product-Specific Queries
- Go to products.html
- Click "Ask AI" on any product
- Ask about materials, sizing, or styling
- Request similar product suggestions

### 3. Contact Form Integration
- Visit contact.html
- Fill out the form
- Use quick question buttons
- Test AI form suggestions

### 4. Responsive Testing
- Test on different screen sizes
- Check mobile chat widget behavior
- Verify touch interactions

## 🚀 Advanced Testing

### Custom Styling
Add custom CSS to override default styles:

```css
/* Custom widget styling */
.jewellery-chatbot-widget {
    --primary-color: #your-color;
    --secondary-color: #your-color;
    --border-radius: 15px;
}
```

### Event Handling
Listen to widget events:

```javascript
window.addEventListener('jewelleryChatbotReady', function() {
    console.log('Chatbot is ready!');
});

window.addEventListener('jewelleryChatbotMessage', function(event) {
    console.log('New message:', event.detail);
});
```

### Programmatic Control
Control the widget via JavaScript:

```javascript
// Open widget
window.JewelleryChatbot.open();

// Close widget
window.JewelleryChatbot.close();

// Send message
window.JewelleryChatbot.send('Hello, I need help!');

// Check status
console.log(window.JewelleryChatbot.state.isOpen);
```

## 🐛 Troubleshooting

### Widget Not Loading
1. Check browser console for errors
2. Verify `jewellery-chatbot-widget.js` path is correct
3. Ensure backend server is running
4. Check CORS configuration

### Chat Not Working
1. Verify API endpoints are accessible
2. Check network requests in browser dev tools
3. Ensure user authentication is working
4. Test with `test_cloud_functionality.py`

### Styling Issues
1. Check for CSS conflicts
2. Verify custom CSS is loaded after widget
3. Use browser dev tools to inspect elements
4. Check z-index values

## 📊 Analytics Integration

Add analytics tracking:

```javascript
// Track widget interactions
window.addEventListener('jewelleryChatbotOpen', function() {
    gtag('event', 'chatbot_opened');
});

window.addEventListener('jewelleryChatbotMessage', function(event) {
    gtag('event', 'chatbot_message', {
        'message_type': event.detail.type
    });
});
```

## 🔒 Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **CORS**: Configure proper CORS settings
3. **Rate Limiting**: Implement rate limiting on backend
4. **Input Validation**: Validate all user inputs
5. **Authentication**: Secure API endpoints properly

## 🎉 Next Steps

1. **Customize the Design**: Modify colors, fonts, and layout
2. **Add More Products**: Expand the product catalog
3. **Implement Search**: Add product search functionality
4. **Add Reviews**: Include customer review system
5. **Mobile Optimization**: Enhance mobile experience
6. **Performance**: Optimize loading times
7. **SEO**: Add meta tags and structured data

## 📞 Support

For issues with the test website:
1. Check the main README.md for backend setup
2. Verify all dependencies are installed
3. Test with the provided test scripts
4. Check browser console for JavaScript errors

Happy testing! 🎉