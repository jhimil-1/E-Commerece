// Test searching for electronics (which we know exist)
async function testElectronicsSearch() {
    console.log('=== Testing Electronics Search ===');
    
    try {
        // Initialize API
        const api = new JewelryAPI();
        
        // Test login
        console.log('Logging in...');
        const loginResult = await api.login('testuser@example.com', 'password123');
        console.log('Login result:', loginResult);
        
        if (!loginResult.success) {
            console.error('Login failed');
            return;
        }
        
        // Test searches for electronics (which should work)
        const electronicsTerms = ['apple', 'iphone', 'watch', 'smartphone', 'headphones'];
        
        for (const term of electronicsTerms) {
            console.log(`\n--- Searching for: "${term}" ---`);
            const result = await api.searchJewelry(term);
            console.log('Search result:', result);
            
            if (result.success && result.data.results.length > 0) {
                console.log(`✅ Found ${result.data.results.length} products for "${term}"`);
                result.data.results.slice(0, 2).forEach((product, i) => {
                    console.log(`  ${i+1}. ${product.name} - ${product.category} - $${product.price}`);
                });
            } else {
                console.log(`❌ No products found for "${term}"`);
            }
        }
        
        // Test searches for jewelry (which should fail)
        console.log('\n=== Testing Jewelry Search (should fail) ===');
        const jewelryTerms = ['gold ring', 'necklace', 'earrings', 'diamond'];
        
        for (const term of jewelryTerms) {
            console.log(`\n--- Searching for: "${term}" ---`);
            const result = await api.searchJewelry(term);
            
            if (result.success && result.data.results.length > 0) {
                console.log(`✅ Found ${result.data.results.length} products for "${term}"`);
                result.data.results.slice(0, 2).forEach((product, i) => {
                    console.log(`  ${i+1}. ${product.name} - ${product.category} - $${product.price}`);
                });
            } else {
                console.log(`❌ No jewelry products found for "${term}"`);
                console.log('This is expected - database contains only electronics!');
            }
        }
        
    } catch (error) {
        console.error('Test failed:', error);
    }
}

// Run the test
testElectronicsSearch();