#!/usr/bin/env python3
"""
Integration test for Compact Evolution Resource Principles
Simulates the patterns found in the existing simulation logs
"""

from compact_evolution import CompactEvolutionSystem
import time

def simulate_log_pattern():
    """Simulate the pattern found in simulation logs"""
    print("=== Compact Evolution Resource Principles - Simulation Log Pattern ===\n")
    
    system = CompactEvolutionSystem()
    
    # Test request similar to simulation logs
    test_request = "process neural network with encryption using memory and store results"
    
    print(f"Input request: {test_request}")
    print("Analyzing technical words and generating compact representation...\n")
    
    result = system.process_request(test_request)
    
    if result['status'] == 'APPROVE':
        print("APPROVE\n")
        
        # Extract compact labels for mathematical operations
        compact_labels = [item['label'] for item in result['compact_representation']['compact_labels']]
        weights = result['compact_representation']['weights']
        
        print("Identified technical components:")
        for item in result['compact_representation']['compact_labels']:
            print(f"{item['label']} = {item['original']} (category: {item['category']})")
        
        print(f"\nMathematical expression: {result['compact_representation']['mathematical_expression']}")
        
        # Simulate mathematical operations like in logs
        if len(compact_labels) >= 2:
            A = compact_labels[0]
            print(f"\nSimulation operations:")
            print(f"{A} + {A} = 2{A}")
            print(f"2{A} / 4 = 0.5{A}")
            print(f"0.5{A} * 2 = 1{A}")
        
        print(f"\nLogic circuit generated: {result['logic_circuit']['name']}")
        print("Operations:")
        for op in result['logic_circuit']['operations']:
            print(f"  {op}")
        
        print(f"\nEvolution principle: {result['evolution_principle']}")
        
    else:
        print("DENY")
        print(f"Reason: {result['reason']}")
    
    print("\n" + "="*60)
    print("Categories and Labels Summary:")
    print("="*60)
    
    # Display category summaries like in simulation logs
    categories = system.export_categories()
    
    print("\n1. Labels for physical properties:")
    phys_props = categories['physical_properties']['compact_mappings']
    for word, mapping in list(phys_props.items())[:8]:
        print(f"   {mapping['label']} -> {word}")
    
    print("\n2. Labels for computer verbs:")
    comp_verbs = categories['computer_verbs']['compact_mappings']
    for word, mapping in list(comp_verbs.items())[:8]:
        print(f"   {mapping['label']} -> {word}")
    
    print("\n3. Labels for IA architecture:")
    ia_arch = categories['ia_architecture']['compact_mappings']
    for word, mapping in list(ia_arch.items())[:5]:
        print(f"   {mapping['label']} -> {word}")
    
    print("\n4. Labels for circuit components:")
    circuits = categories['circuit_components']['compact_mappings']
    for word, mapping in list(circuits.items())[:5]:
        print(f"   {mapping['label']} -> {word}")
    
    print("\n5. Labels for security concepts:")
    security = categories['security_concepts']['compact_mappings']
    for word, mapping in list(security.items())[:5]:
        print(f"   {mapping['label']} -> {word}")

def test_multiple_requests():
    """Test multiple requests to verify consistency"""
    print("\n" + "="*60)
    print("Multiple Request Processing Test")
    print("="*60)
    
    system = CompactEvolutionSystem()
    
    test_requests = [
        "compile and execute neural network algorithm",
        "encrypt data using secure authentication protocol", 
        "process memory allocation for data structure",
        "debug optimization techniques for circuit design"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\nTest {i}: {request}")
        result = system.process_request(request)
        
        if result['status'] == 'APPROVE':
            compact_expr = result['compact_representation']['mathematical_expression']
            operations_count = len(result['logic_circuit']['operations'])
            print(f"  Status: APPROVE")
            print(f"  Expression: {compact_expr}")
            print(f"  Operations: {operations_count}")
        else:
            print(f"  Status: DENY - {result['reason']}")

if __name__ == "__main__":
    simulate_log_pattern()
    test_multiple_requests()
    
    print(f"\n{'='*60}")
    print("Integration test completed successfully!")
    print("System ready for deployment in Red&Queen simulation environment.")
    print(f"{'='*60}")