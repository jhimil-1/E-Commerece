// Simple test to check what's actually happening
async function testSearch() {
    console.log('Starting search test...');
    
    // Check if API is available
    if (!window.jewelryAPI) {
        console.error('jewelryAPI not found');
        return;
    }
    
    if (!window.jewelryUI) {
        console.error('jewelryUI not found');
        return;
    }
    
    // Check authentication
    console.log('Access token available:', !!window.jewelryAPI.accessToken);
    
    try {
        // Perform a simple search
        console.log('Searching for "phone"...');
        const result = await window.jewelryAPI.searchJewelry({ query: 'phone', limit: 5 });
        
        console.log('Search result:', result);
        console.log('Result.success:', result.success);
        console.log('Result.data:', result.data);
        console.log('Result.data.results:', result.data?.results);
        console.log('Result.data.count:', result.data?.count);
        
        if (result.success && result.data?.results) {
            console.log('First product:', result.data.results[0]);
            console.log('Number of products found:', result.data.results.length);
            
            // Try to display results manually
            console.log('Calling displayResults...');
            window.jewelryUI.displayResults(result.data.results);
        } else {
            console.log('Search failed or no results');
        }
        
    } catch (error) {
        console.error('Search test failed:', error);
    }
}

// Add a button to trigger the test
const testButton = document.createElement('button');
testButton.textContent = 'Test Search';
testButton.style.position = 'fixed';
testButton.style.top = '10px';
testButton.style.right = '10px';
testButton.style.zIndex = '1000';
testButton.onclick = testSearch;
document.body.appendChild(testButton);

console.log('Test button added. Click it to run the search test.');