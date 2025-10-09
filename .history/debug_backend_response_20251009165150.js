// Debug script to see exactly what the backend returns
console.log('=== BACKEND RESPONSE DEBUG ===');

async function debugBackendResponse() {
    try {
        // Check if authenticated
        if (!window.jewelryAPI || !window.jewelryAPI.isAuthenticated()) {
            console.error('Not authenticated');
            return;
        }
        
        console.log('Performing search for "phone"...');
        
        // Perform the search
        const result = await window.jewelryAPI.searchJewelry({ query: 'phone', limit: 5 });
        
        console.log('Full search result:', JSON.stringify(result, null, 2));
        console.log('Result.success:', result.success);
        console.log('Result.data:', result.data);
        console.log('Result.data.results:', result.data?.results);
        console.log('Result.data.count:', result.data?.count);
        
        if (result.success && result.data) {
            const results = result.data.results || result.data;
            console.log('Results array:', results);
            console.log('Results length:', results.length);
            
            if (results.length > 0) {
                console.log('First result structure:', JSON.stringify(results[0], null, 2));
                console.log('First result keys:', Object.keys(results[0]));
                console.log('First result name:', results[0].name);
                console.log('First result price:', results[0].price);
                console.log('First result category:', results[0].category);
                console.log('First result image_url:', results[0].image_url);
            }
        }
        
    } catch (error) {
        console.error('Debug failed:', error);
    }
}

// Run the debug
debugBackendResponse();