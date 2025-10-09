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
        console.log('=== MANUAL SEARCH TEST STARTED ===');
        
        // Check authentication
        if (!window.jewelryAPI || !window.jewelryAPI.accessToken) {
            alert('Please login first!');
            console.error('Not authenticated');
            return;
        }
        
        console.log('Authenticated, starting test search...');
        
        try {
            // Test search
            console.log('Calling searchJewelry with query "gold ring"...');
            const result = await window.jewelryAPI.searchJewelry({ 
                query: 'gold ring', 
                limit: 3 
            });
            
            console.log('Search result:', result);
            console.log('Success:', result.success);
            console.log('Data:', result.data);
            console.log('Results:', result.data?.results);
            console.log('Count:', result.data?.count);
            
            if (result.success && result.data?.results) {
                console.log('Search successful! Testing displayResults...');
                console.log('Results to display:', result.data.results);
                console.log('First product:', result.data.results[0]);
                
                // Test displayResults
                window.jewelryUI.displayResults(result.data.results);
                
                console.log('displayResults called successfully');
                
                // Check visibility after a short delay
                setTimeout(() => {
                    const resultsSection = document.getElementById('resultsSection');
                    const resultsContainer = document.getElementById('searchResults');
                    
                    console.log('Results section visible:', resultsSection?.style.display === 'block');
                    console.log('Results container has content:', resultsContainer?.innerHTML.length > 0);
                    
                    if (resultsSection?.style.display === 'block' && resultsContainer?.innerHTML.length > 0) {
                        console.log('✅ SUCCESS: Results are visible!');
                        alert('✅ Search test successful! Check the console for details.');
                    } else {
                        console.error('❌ FAILED: Results not visible');
                        alert('❌ Search test failed: Results not visible. Check console for details.');
                    }
                }, 1000);
                
            } else {
                console.error('Search failed:', result);
                alert('Search failed. Check console for details.');
            }
            
        } catch (error) {
            console.error('Test failed with error:', error);
            alert('Test failed with error. Check console for details.');
        }
        
        console.log('=== MANUAL SEARCH TEST COMPLETED ===');
    };
    
    // Add button to page
    document.body.appendChild(testButton);
    console.log('Manual test button added! Click it to test search functionality.');
})();