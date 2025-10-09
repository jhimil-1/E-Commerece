// Live search test to debug the actual issue
(function() {
    console.log('=== LIVE SEARCH DEBUG TEST ===');
    
    // Wait for everything to load
    setTimeout(async function() {
        console.log('Starting live search test...');
        
        // Check if we're authenticated
        if (!window.jewelryAPI || !window.jewelryAPI.accessToken) {
            console.error('Not authenticated!');
            alert('Please login first, then click OK to run the test');
            return;
        }
        
        console.log('Authenticated, testing search...');
        
        try {
            // Test the searchJewelry method directly
            console.log('Calling searchJewelry...');
            const result = await window.jewelryAPI.searchJewelry({ 
                query: 'gold ring', 
                limit: 5 
            });
            
            console.log('Search result received:', result);
            console.log('Result.success:', result.success);
            console.log('Result.data:', result.data);
            console.log('Result.data.results:', result.data?.results);
            console.log('Result.data.count:', result.data?.count);
            
            if (result.success && result.data?.results) {
                console.log('Search successful, testing displayResults...');
                console.log('Results array:', result.data.results);
                console.log('First product:', result.data.results[0]);
                
                // Test displayResults directly
                console.log('Calling displayResults...');
                window.jewelryUI.displayResults(result.data.results);
                
                console.log('displayResults completed');
                
                // Check if results are visible
                setTimeout(() => {
                    const resultsSection = document.getElementById('resultsSection');
                    const resultsContainer = document.getElementById('searchResults');
                    console.log('Results section display:', resultsSection?.style.display);
                    console.log('Results container content length:', resultsContainer?.innerHTML.length);
                    console.log('Results container HTML:', resultsContainer?.innerHTML);
                }, 1000);
                
            } else {
                console.error('Search failed or no results:', result);
            }
            
        } catch (error) {
            console.error('Test failed with error:', error);
        }
        
    }, 2000); // Wait 2 seconds for everything to load
    
    console.log('Debug test script loaded. It will run automatically in 2 seconds...');
})();