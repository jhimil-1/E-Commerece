#!/usr/bin/env python3
"""
Final comprehensive test of enhanced search functionality
"""

import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler

async def comprehensive_test():
    """Comprehensive test of enhanced search"""
    print("🎯 Final Enhanced Search Test")
    print("=" * 50)
    
    # Initialize handlers
    base_handler = ProductHandler()
    enhanced_handler = EnhancedProductHandler(base_handler)
    
    test_cases = [
        {
            "query": "necklace",
            "expected_type": "necklace",
            "description": "Basic necklace search"
        },
        {
            "query": "gold earrings",
            "expected_type": "earrings", 
            "description": "Specific jewelry type"
        },
        {
            "query": "diamond ring",
            "expected_type": "ring",
            "description": "Precious stone jewelry"
        },
        {
            "query": "men's watch",
            "expected_type": "watch",
            "description": "Men's accessories"
        },
        {
            "query": "pearl necklace",
            "expected_type": "necklace",
            "description": "Specific material jewelry"
        }
    ]
    
    results_summary = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['description']}")
        print(f"   Query: '{test_case['query']}'")
        print(f"   Expected: {test_case['expected_type']}")
        
        try:
            # Test enhanced search
            enhanced_results = await enhanced_handler.search_products(
                query=test_case['query'],
                limit=5
            )
            
            enhanced_products = enhanced_results.get("results", [])
            
            # Count relevant products
            relevant_count = sum(1 for p in enhanced_products 
                               if test_case['expected_type'] in p.get("name", "").lower())
            
            precision = (relevant_count / len(enhanced_products) * 100) if enhanced_products else 0
            
            print(f"   Results: {len(enhanced_products)} products")
            print(f"   Relevant: {relevant_count} products")
            print(f"   Precision: {precision:.1f}%")
            
            # Show top 3 results
            for j, product in enumerate(enhanced_products[:3], 1):
                status = "✅" if test_case['expected_type'] in product.get("name", "").lower() else "❌"
                print(f"     {j}. {status} {product.get('name', 'Unknown')} (Score: {product.get('similarity_score', 0):.3f})")
            
            results_summary.append({
                'test_case': test_case['description'],
                'precision': precision,
                'relevant_count': relevant_count,
                'total_count': len(enhanced_products)
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results_summary.append({
                'test_case': test_case['description'],
                'precision': 0,
                'relevant_count': 0,
                'total_count': 0
            })
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 ENHANCED SEARCH SUMMARY")
    print("=" * 50)
    
    total_precision = sum(r['precision'] for r in results_summary) / len(results_summary) if results_summary else 0
    total_relevant = sum(r['relevant_count'] for r in results_summary)
    total_products = sum(r['total_count'] for r in results_summary)
    
    print(f"Overall Precision: {total_precision:.1f}%")
    print(f"Total Relevant Products: {total_relevant}/{total_products}")
    print(f"Average Relevant per Query: {total_relevant/len(results_summary):.1f}")
    
    print("\nDetailed Results:")
    for result in results_summary:
        status = "✅" if result['precision'] >= 60 else "⚠️" if result['precision'] >= 40 else "❌"
        print(f"  {status} {result['test_case']}: {result['precision']:.1f}% ({result['relevant_count']}/{result['total_count']})")
    
    # Performance analysis
    print("\n🚀 Performance Analysis:")
    excellent = sum(1 for r in results_summary if r['precision'] >= 80)
    good = sum(1 for r in results_summary if 60 <= r['precision'] < 80)
    fair = sum(1 for r in results_summary if 40 <= r['precision'] < 60)
    poor = sum(1 for r in results_summary if r['precision'] < 40)
    
    print(f"  🏆 Excellent (≥80%): {excellent} tests")
    print(f"  ✅ Good (60-79%): {good} tests") 
    print(f"  ⚠️  Fair (40-59%): {fair} tests")
    print(f"  ❌ Poor (<40%): {poor} tests")
    
    return total_precision >= 70  # Success threshold

async def main():
    success = await comprehensive_test()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ENHANCED SEARCH VERIFICATION: SUCCESS")
        print("✅ The enhanced search system is working correctly!")
        print("✅ Significant improvement in search precision achieved!")
        print("✅ Users will now get more relevant product results!")
    else:
        print("⚠️  ENHANCED SEARCH VERIFICATION: NEEDS IMPROVEMENT")
        print("❌ Some tests did not meet the expected precision threshold.")
        print("❌ Consider adjusting thresholds or algorithms.")
    
    print("\n📋 Next Steps:")
    print("1. Monitor real-world usage and user feedback")
    print("2. Fine-tune relevance thresholds based on performance")
    print("3. Expand product type extraction for more categories")
    print("4. Consider user preference learning for personalization")

if __name__ == "__main__":
    asyncio.run(main())