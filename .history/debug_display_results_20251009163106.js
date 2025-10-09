// Debug the displayResults function
console.log('=== DEBUGGING displayResults ===');

// Override the displayResults function to add debugging
if (window.jewelryUI) {
    const originalDisplayResults = window.jewelryUI.displayResults;
    
    window.jewelryUI.displayResults = function(results) {
        console.log('=== DISPLAYRESULTS DEBUG ===');
        console.log('Input results:', results);
        console.log('Type of results:', typeof results);
        console.log('Is array?', Array.isArray(results));
        console.log('Results length:', results ? results.length : 'null/undefined');
        
        if (results && results.length > 0) {
            console.log('First result:', results[0]);
            console.log('First result keys:', Object.keys(results[0]));
            
            // Check if products have the required fields
            results.forEach((result, index) => {
                console.log(`Result ${index}:`, {
                    name: result.name,
                    price: result.price,
                    category: result.category,
                    description: result.description,
                    image_url: result.image_url,
                    image_path: result.image_path,
                    image: result.image,
                    score: result.score
                });
            });
        }
        
        // Call the original function
        return originalDisplayResults.call(this, results);
    };
    
    console.log('displayResults function has been wrapped with debugging');
} else {
    console.log('jewelryUI not available');
}

// Also debug the searchJewelry response
if (window.jewelryAPI) {
    const originalSearchJewelry = window.jewelryAPI.searchJewelry;
    
    window.jewelryAPI.searchJewelry = async function(searchParams) {
        console.log('=== SEARCHJEWELRY DEBUG ===');
        console.log('Input searchParams:', searchParams);
        
        const result = await originalSearchJewelry.call(this, searchParams);
        
        console.log('Search result:', result);
        console.log('Result success:', result.success);
        console.log('Result data:', result.data);
        console.log('Result data results:', result.data?.results);
        console.log('Result data results length:', result.data?.results?.length);
        
        return result;
    };
    
    console.log('searchJewelry function has been wrapped with debugging');
} else {
    console.log('jewelryAPI not available');
}