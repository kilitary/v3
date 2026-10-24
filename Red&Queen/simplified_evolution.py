#!/usr/bin/env python3
"""
Simplified Compact Evolution Resource Principles
===============================================

Simplified version without complex mathematical abstractions, 
addressing concerns about algorithm conflicts and security weights.
"""

from compact_evolution import CompactEvolutionSystem, CategoryType
from typing import Dict, List

class SimplifiedEvolutionSystem:
    """Simplified version with minimal mathematical operations"""
    
    def __init__(self):
        self.evolution_system = CompactEvolutionSystem()
        self.simple_metrics = self._calculate_simple_metrics()
    
    def _calculate_simple_metrics(self) -> Dict:
        """Calculate simple, single-dimension metrics for each category"""
        metrics = {}
        
        for category in CategoryType:
            words = self.evolution_system.categories[category]
            
            # Single dimension: average word length (simplest measure)
            if words:
                avg_length = sum(len(word) for word in words) / len(words)
                word_count = len(words)
                
                # Simple entropy approximation (word count diversity)
                entropy_simple = word_count / 100.0  # Normalized simple entropy
                
                metrics[category.value] = {
                    "dimension": round(avg_length, 2),  # Single dimension only
                    "word_count": word_count,
                    "entropy": round(entropy_simple, 3),
                    "formula": f"D = {avg_length:.2f}"
                }
            else:
                metrics[category.value] = {
                    "dimension": 0.0,
                    "word_count": 0,
                    "entropy": 0.0,
                    "formula": "D = 0.00"
                }
        
        return metrics
    
    def get_system_summary(self) -> Dict:
        """Get simplified system summary without complex calculations"""
        total_words = sum(self.simple_metrics[cat]["word_count"] 
                         for cat in self.simple_metrics)
        
        avg_dimension = sum(self.simple_metrics[cat]["dimension"] 
                           for cat in self.simple_metrics) / len(self.simple_metrics)
        
        return {
            "total_categories": len(CategoryType),
            "total_words": total_words,
            "average_dimension": round(avg_dimension, 2),
            "system_formula": f"D_system = {avg_dimension:.2f}",
            "complexity": "SIMPLIFIED"  # No complex calculations
        }
    
    def process_request_simple(self, request: str) -> Dict:
        """Process request with simplified approach"""
        # Use the original system for word identification
        result = self.evolution_system.process_request(request)
        
        if result['status'] == 'APPROVE':
            words = result['identified_words']
            
            # Simple dimension calculation (just average length)
            if words:
                avg_length = sum(len(word) for word in words) / len(words)
                simple_formula = f"D = {avg_length:.2f}"
            else:
                avg_length = 0.0
                simple_formula = "D = 0.00"
            
            # Simplified result
            simplified_result = {
                "status": "APPROVE",
                "words": words,
                "compact_representation": result['compact_representation']['mathematical_expression'],
                "simple_dimension": round(avg_length, 2),
                "simple_formula": simple_formula,
                "word_count": len(words),
                "logic_circuit": result['logic_circuit']['name'],
                "operations_count": len(result['logic_circuit']['operations'])
            }
        else:
            simplified_result = {
                "status": "DENY",
                "reason": result['reason'],
                "simple_dimension": 0.0,
                "simple_formula": "D = 0.00"
            }
        
        return simplified_result
    
    def export_simple_analysis(self) -> Dict:
        """Export simplified analysis without complex mathematical abstractions"""
        return {
            "system_summary": self.get_system_summary(),
            "category_metrics": self.simple_metrics,
            "note": "Simplified version - complex mathematical abstractions excluded"
        }

def demonstrate_simplified_system():
    """Demonstrate the simplified system"""
    print("=" * 60)
    print("SIMPLIFIED COMPACT EVOLUTION RESOURCE PRINCIPLES")
    print("Excludes complex mathematical abstractions")
    print("=" * 60)
    
    simple_system = SimplifiedEvolutionSystem()
    
    # System overview
    summary = simple_system.get_system_summary()
    print(f"\n📊 SYSTEM SUMMARY:")
    print(f"  Categories: {summary['total_categories']}")
    print(f"  Total Words: {summary['total_words']}")
    print(f"  Average Dimension: {summary['average_dimension']}")
    print(f"  System Formula: {summary['system_formula']}")
    print(f"  Complexity: {summary['complexity']}")
    
    # Category metrics
    print(f"\n📋 CATEGORY METRICS (Single Dimension Only):")
    for category, metrics in simple_system.simple_metrics.items():
        print(f"  {category.replace('_', ' ').title():20}: {metrics['formula']} ({metrics['word_count']} words)")
    
    # Test requests
    print(f"\n🔍 REQUEST PROCESSING:")
    test_requests = [
        "process neural network with encryption",
        "execute algorithm on data structure",
        "compile secure protocol"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n  Request {i}: {request}")
        result = simple_system.process_request_simple(request)
        
        print(f"    Status: {result['status']}")
        if result['status'] == 'APPROVE':
            print(f"    Words: {result['words']}")
            print(f"    Simple Dimension: {result['simple_dimension']}")
            print(f"    Formula: {result['simple_formula']}")
            print(f"    Operations: {result['operations_count']}")
    
    print(f"\n✅ SIMPLIFIED SYSTEM DEMONSTRATION COMPLETE")
    print("Complex mathematical abstractions excluded as requested")

if __name__ == "__main__":
    demonstrate_simplified_system()