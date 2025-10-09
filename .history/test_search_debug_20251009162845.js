// Test script to debug the search functionality
console.log('=== SEARCH DEBUG TEST ===');

// Check which API is being used
console.log('window.jewelryAPI:', window.jewelryAPI);
console.log('window.jewelryUI:', window.jewelryUI);

// Test the search functionality
async function testSearch() {
    if (window.jewelryAPI && window.jewelryAPI.isAuthenticated()) {
        console.log('API is authenticated, testing search...');
        
        try {
            const result = await window.jewelryAPI.searchJewelry({
                query: 'phone',
                limit: 5
            });
            
            console.log('Search result:', result);
            
            if (result.success) {
                console.log('Products found:', result.data.results);
                console.log('Number of products:', result.data.count);
                
                // Test displayResults
                if (window.jewelryUI) {
                    console.log('Calling displayResults...');
                    window.jewelryUI.displayResults(result.data.results);
                }
            } else {
                console.log('Search failed:', result.error);
            }
        } catch (error) {
            console.error('Search error:', error);
        }
    } else {
        console.log('API not available or not authenticated');
    }
}

// Run the test
testSearch();