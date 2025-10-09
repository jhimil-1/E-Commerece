// Manual test button for debugging search functionality
(function() {
    // Create a test button
    const testButton = document.createElement('button');
    testButton.textContent = '🔍 Test Search';
    testButton.style.position = 'fixed';
    testButton.style.bottom = '20px';
    testButton.style.right = '20px';
    testButton.style.zIndex = '1000';
    testButton.style.background = '#4CAF50';
    testButton.style.color = 'white';
    testButton.style.border = 'none';
    testButton.style.padding = '12px 20px';
    testButton.style.borderRadius = '25px';
    testButton.style.cursor = 'pointer';
    testButton.style.fontSize = '14px';
    testButton.style.fontWeight = 'bold';
    testButton.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
    
    testButton.onclick = async function() {
        console.log('=== Manual Test Started ===');
        
        // Test login
        console.log('Testing login...');
        const loginResult = await api.login('testuser@example.com', 'password123');
        console.log('Login result:', loginResult);
        
        if (!loginResult.success) {
            console.error('Login failed, trying signup...');
            const signupResult = await api.signup('testuser@example.com', 'password123', 'testuser');
            console.log('Signup result:', signupResult);
            
            if (!signupResult.success) {
                console.error('Both login and signup failed');
                return;
            }
        }
        
        // Test search
        console.log('\nTesting search...');
        const searchResult = await api.searchJewelry('gold ring');
        console.log('Search result:', searchResult);
        
        // Test display
        console.log('\nTesting display...');
        if (searchResult.success && searchResult.data.results.length > 0) {
            displayResults(searchResult.data.results);
            
            // Check if results are visible
            setTimeout(() => {
                const resultsContainer = document.querySelector('.results-container, #results, [class*="results"]');
                if (resultsContainer && resultsContainer.children.length > 0) {
                    console.log('✅ Results are visible in DOM');
                } else {
                    console.log('❌ Results not visible in DOM');
                }
            }, 1000);
        }
        
        console.log('=== Manual Test Completed ===');
    };
    
    // Add electronics test button
    const electronicsButton = document.createElement('button');
    electronicsButton.textContent = 'Test Electronics Search';
    electronicsButton.style.position = 'fixed';
    electronicsButton.style.bottom = '80px';
    electronicsButton.style.right = '20px';
    electronicsButton.style.zIndex = '1000';
    electronicsButton.style.padding = '10px 15px';
    electronicsButton.style.backgroundColor = '#28a745';
    electronicsButton.style.color = 'white';
    electronicsButton.style.border = 'none';
    electronicsButton.style.borderRadius = '5px';
    electronicsButton.style.cursor = 'pointer';
    
    document.body.appendChild(electronicsButton);
    
    electronicsButton.addEventListener('click', () => {
        testElectronicsSearch();
    });
    
    // Add button to page
    document.body.appendChild(testButton);
    console.log('Manual test button added! Click it to test search functionality.');
})();