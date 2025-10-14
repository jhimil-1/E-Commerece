# 🤖 Chatbot Widget Testing Guide

## Overview
This guide explains how to test the jewellery chatbot widget functionality. The widget provides an AI-powered assistant for jewellery e-commerce websites.

## 🚀 Quick Start Testing

### 1. Start the Backend Server
First, ensure your FastAPI backend is running:
```bash
python main.py
```

### 2. Start the Test Website Server
In a separate terminal, start the HTTP server for the test website:
```bash
cd test-website
python -m http.server 8080
```

### 3. Access Test Pages
- **Test Widget Page**: http://localhost:8080/test_widget.html
- **Demo Website**: http://localhost:8080/

## 🧪 Testing Scenarios

### Basic Functionality Tests

#### Widget Appearance
- ✅ Widget button appears in bottom-right corner
- ✅ Button shows chat icon (💬)
- ✅ Button is circular and properly styled
- ✅ Button is clickable and responsive

#### Widget Opening/Closing
- ✅ Click widget button to open chat window
- ✅ Chat window opens smoothly
- ✅ Click minimize button to minimize
- ✅ Click close button to close
- ✅ Click outside to close (if configured)

#### Chat Interface
- ✅ Welcome message displays correctly
- ✅ Input field is visible and functional
- ✅ Send button is visible and clickable
- ✅ File attachment button is available
- ✅ Typing indicator works when bot responds

### Authentication Tests

#### User Registration
1. Open widget
2. Click "Sign Up" if not authenticated
3. Enter username, email, and password
4. Submit registration form
5. ✅ User should be logged in automatically

#### User Login
1. Open widget  
2. Click "Login" if not authenticated
3. Enter username and password
4. Submit login form
5. ✅ User should be authenticated
6. ✅ Chat interface should appear

**Test Credentials** (if using existing test user):
- Username: `test_user_02ff81cd`
- Password: `test123`

### Jewelry Search Tests

#### Standard Jewelry Queries
Test these queries to verify basic functionality:
- "Show me some jewelry"
- "What rings do you have?"
- "Show me necklaces under $500"
- "I need a gift for my wife"

#### Spelling Correction Tests
**Critical Test**: Verify the "jewellry" spelling fix works:
- ✅ Type: "Show me jewellry" (with double 'l')
- ✅ Should return jewelry products
- ✅ Should work exactly like "jewelry" spelling

#### Advanced Queries
- "What would look good with a black dress?"
- "Show me gold wedding rings"
- "I need something for a birthday gift"
- "What are your most popular items?"

### Feature Tests

#### Theme Customization
```javascript
// Test different themes
window.JewelleryChatbot.setTheme('blue');
window.JewelleryChatbot.setTheme('purple');
window.JewelleryChatbot.setTheme('green');

// Test custom theme
window.JewelleryChatbot.setTheme('custom', {
    customColors: {
        primary: '#ff6b6b',
        secondary: '#4ecdc4'
    }
});
```

#### Position Changes
```javascript
// Test different positions
window.JewelleryChatbot.setPosition('bottom-right');
window.JewelleryChatbot.setPosition('bottom-left');
window.JewelleryChatbot.setPosition('top-right');
window.JewelleryChatbot.setPosition('top-left');
```

#### Programmatic Control
```javascript
// Open/close widget
window.JewelleryChatbot.open();
window.JewelleryChatbot.close();

// Send message programmatically
window.JewelleryChatbot.send('Show me jewelry');

// Check authentication status
console.log(window.JewelleryChatbot.state.isAuthenticated);
```

## 📋 Test Checklist

### Core Functionality
- [ ] Widget loads without errors
- [ ] Widget button is visible and styled correctly
- [ ] Widget opens and closes smoothly
- [ ] Chat interface displays properly
- [ ] Input field accepts text
- [ ] Send button works
- [ ] Messages appear in chat window

### Authentication
- [ ] Login form displays when needed
- [ ] Registration form works
- [ ] Authentication persists
- [ ] User can access chat after login

### Jewelry Search
- [ ] "jewelry" spelling works
- [ ] "jewellry" spelling works (✅ **Critical**)
- [ ] Product results display correctly
- [ ] Prices are shown
- [ ] Product categories are correct
- [ ] Search results are relevant

### Advanced Features
- [ ] File upload works (if implemented)
- [ ] Theme customization works
- [ ] Position changes work
- [ ] Typing indicator displays
- [ ] Chat history is maintained
- [ ] Widget responds to programmatic commands

## 🔧 Manual Testing Steps

### Step 1: Visual Inspection
1. Load the test page
2. Verify widget button appears in corner
3. Check button styling and positioning
4. Ensure no console errors

### Step 2: Basic Interaction
1. Click widget button to open
2. Verify chat window opens
3. Check welcome message displays
4. Test closing the widget

### Step 3: Authentication Test
1. Try to send a message (should prompt for login)
2. Use test credentials to login
3. Verify authentication succeeds
4. Check that chat interface appears

### Step 4: Jewelry Query Test
1. Type: "Show me jewellry" (with double 'l')
2. Press send or hit Enter
3. Wait for response
4. Verify jewelry products are returned
5. Check that products have correct category

### Step 5: Response Validation
1. Verify response contains product names
2. Check that prices are displayed
3. Ensure products are jewelry category
4. Test multiple different queries

## 🚨 Common Issues and Solutions

### Widget Not Loading
- **Check**: Backend server is running
- **Check**: No JavaScript errors in console
- **Check**: Script path is correct

### Authentication Fails
- **Check**: Backend API is accessible
- **Check**: Database connection is working
- **Check**: Test user credentials are correct

### No Product Results
- **Check**: Products exist in database
- **Check**: Product categories are set correctly
- **Check**: Search functionality is working

### "Jewellry" Spelling Not Working
- **Check**: Spelling correction is implemented
- **Check**: Category detection includes "jewellry"
- **Check**: Database has jewelry products

## 🧪 Automated Testing

Use the provided test files:
- `test_widget.html` - Interactive testing page
- `test_jewellry_spelling.py` - Specific spelling test
- `test_jewelry_comprehensive.py` - Comprehensive jewelry tests

## 📊 Test Results Documentation

When testing, document:
- Test date and time
- Browser used
- Test scenarios performed
- Results (pass/fail)
- Any issues encountered
- Screenshots of problems

## 🎯 Success Criteria

The widget is considered working when:
- ✅ Widget loads without errors
- ✅ User can authenticate successfully
- ✅ Jewelry queries return relevant products
- ✅ "Jewellry" spelling works exactly like "jewelry"
- ✅ Chat interface is responsive and functional
- ✅ All test scenarios pass

## 📝 Notes

- Test in multiple browsers (Chrome, Firefox, Safari)
- Test on mobile devices for responsiveness
- Verify widget works with slow network connections
- Check accessibility features
- Test with different screen sizes