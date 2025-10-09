// Test to verify the data flow from backend to display
console.log('=== TESTING DATA FLOW ===');

async function testDataFlow() {
    try {
        // Check authentication
        if (!window.jewelryAPI || !window.jewelryAPI.isAuthenticated()) {
            console.error('API not authenticated');
            return;
        }
        
        console.log('API is authenticated');
        
        // Perform search
        console.log('Searching for "phone"...');
        const result = await window.jewelryAPI.searchJewelry({
            query: 'phone',
            limit: 5
        });
        
        console.log('Search result:', result);
        
        if (result.success && result.data && result.data.results) {
            console.log('Found', result.data.results.length, 'products');
            console.log('First product structure:', result.data.results[0]);
            
            // Test displayResults manually
            console.log('Calling displayResults...');
            window.jewelryUI.displayResults(result.data.results);
            
            // Check if results section is visible
            setTimeout(() => {
                const resultsSection = document.getElementById('resultsSection');
                const searchResults = document.getElementById('searchResults');
                
                console.log('Results section display:', resultsSection ? resultsSection.style.display : 'N/A');
                console.log('Search results innerHTML length:', searchResults ? searchResults.innerHTML.length : 'N/A');
                
                if (searchResults) {
                    console.log('Search results content preview:', searchResults.innerHTML.substring(0, 200));
                }
            }, 1000);
            
        } else {
            console.error('Search failed or no results:', result);
        }
        
    } catch (error) {
        console.error('Test failed:', error);
    }
}

// Add test button
const testButton = document.createElement('button');
testButton.textContent = 'Test Data Flow';
testButton.style.position = 'fixed';
testButton.style.top = '50px';
testButton.style.right = '10px';
testButton.style.zIndex = '1000';
testButton.onclick = testDataFlow;
document.body.appendChild(testButton);

console.log('Test button added. Click to test data flow.');