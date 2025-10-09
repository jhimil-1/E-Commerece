// Comprehensive debug script to identify the exact issue
(function() {
    console.log('=== COMPREHENSIVE DEBUG SCRIPT LOADED ===');
    
    // Override the displayResults function with detailed logging
    const originalDisplayResults = window.jewelryUI.displayResults;
    
    window.jewelryUI.displayResults = function(results) {
        console.log('=== DISPLAY RESULTS CALLED ===');
        console.log('Input results:', results);
        console.log('Type of results:', typeof results);
        console.log('Is Array?', Array.isArray(results));
        console.log('Results length:', results ? results.length : 'N/A');
        
        if (results && Array.isArray(results)) {
            console.log('First result:', results[0]);
            console.log('Keys in first result:', results[0] ? Object.keys(results[0]) : 'N/A');
            
            // Check if products have the expected fields
            if (results[0]) {
                console.log('First result name:', results[0].name);
                console.log('First result price:', results[0].price);
                console.log('First result category:', results[0].category);
                console.log('First result image_url:', results[0].image_url);
            }
        }
        
        // Call original function
        const result = originalDisplayResults.call(this, results);
        
        // Check what happened after displayResults
        const resultsContainer = document.getElementById('searchResults');
        const resultsSection = document.getElementById('resultsSection');
        
        console.log('After displayResults:');
        console.log('resultsSection display style:', resultsSection ? resultsSection.style.display : 'N/A');
        console.log('resultsContainer innerHTML length:', resultsContainer ? resultsContainer.innerHTML.length : 'N/A');
        console.log('resultsContainer content preview:', resultsContainer ? resultsContainer.innerHTML.substring(0, 200) : 'N/A');
        
        return result;
    };
    
    // Override performSearch to add logging
    const originalPerformSearch = window.jewelryUI.performSearch;
    
    window.jewelryUI.performSearch = async function() {
        console.log('=== PERFORM SEARCH CALLED ===');
        
        const result = await originalPerformSearch.call(this);
        
        console.log('PerformSearch completed');
        return result;
    };
    
    // Override searchJewelry to add logging
    const originalSearchJewelry = window.jewelryAPI.searchJewelry;
    
    window.jewelryAPI.searchJewelry = async function(searchParams) {
        console.log('=== SEARCH JEWELRY CALLED ===');
        console.log('Search params:', searchParams);
        
        const result = await originalSearchJewelry.call(this, searchParams);
        
        console.log('SearchJewelry result:', result);
        console.log('Result.success:', result.success);
        console.log('Result.data:', result.data);
        
        return result;
    };
    
    // Add a test button
    const debugButton = document.createElement('button');
    debugButton.textContent = 'Debug Test';
    debugButton.style.position = 'fixed';
    debugButton.style.top = '10px';
    debugButton.style.right = '10px';
    debugButton.style.zIndex = '1000';
    debugButton.style.background = '#ff6b6b';
    debugButton.style.color = 'white';
    debugButton.style.border = 'none';
    debugButton.style.padding = '10px';
    debugButton.style.borderRadius = '5px';
    debugButton.style.cursor = 'pointer';
    
    debugButton.onclick = async function() {
        console.log('=== MANUAL DEBUG TEST ===');
        
        // Check authentication
        console.log('Access token:', window.jewelryAPI.accessToken);
        console.log('Is authenticated:', !!window.jewelryAPI.accessToken);
        
        if (!window.jewelryAPI.accessToken) {
            console.error('Not authenticated!');
            return;
        }
        
        try {
            console.log('Performing test search...');
            const result = await window.jewelryAPI.searchJewelry({ query: 'phone', limit: 3 });
            
            console.log('Test search result:', result);
            
            if (result.success && result.data?.results) {
                console.log('Calling displayResults with:', result.data.results);
                window.jewelryUI.displayResults(result.data.results);
            }
            
        } catch (error) {
            console.error('Test failed:', error);
        }
    };
    
    document.body.appendChild(debugButton);
    
    // Add a direct test function to window
    window.runDebugTest = function() {
        debugButton.click();
    };
    
    console.log('Debug button added. Click it or run runDebugTest() to test.');
})();