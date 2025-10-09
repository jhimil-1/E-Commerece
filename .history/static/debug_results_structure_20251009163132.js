// Debug script to check the actual data structure being passed to displayResults
(function() {
    // Store original functions
    const originalDisplayResults = window.jewelryUI.displayResults;
    const originalSearchJewelry = window.jewelryAPI.searchJewelry;
    
    // Override displayResults to log the input
    window.jewelryUI.displayResults = function(results) {
        console.log('=== DISPLAY RESULTS DEBUG ===');
        console.log('Type of results:', typeof results);
        console.log('Results object:', results);
        console.log('Is Array?', Array.isArray(results));
        console.log('Length:', results ? results.length : 'N/A');
        console.log('JSON.stringify:', JSON.stringify(results, null, 2));
        console.log('=== END DEBUG ===');
        
        // Call original function
        return originalDisplayResults.call(this, results);
    };
    
    // Override searchJewelry to log the response
    window.jewelryAPI.searchJewelry = async function(data) {
        console.log('=== SEARCH JEWELRY DEBUG ===');
        console.log('Input data:', data);
        
        const result = await originalSearchJewelry.call(this, data);
        
        console.log('Search result:', result);
        console.log('Result.success:', result.success);
        console.log('Result.data:', result.data);
        console.log('Result.data.results:', result.data?.results);
        console.log('Is Array?', Array.isArray(result.data?.results));
        console.log('=== END SEARCH DEBUG ===');
        
        return result;
    };
    
    console.log('Debug wrappers installed!');
})();