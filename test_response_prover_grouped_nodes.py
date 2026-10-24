#!/usr/bin/env python3
"""
Test for 0 level counter-error grouped nodes functionality with verb-logic system
"""

import os
import tempfile
from response_prover_mock import ResponseProverMock


def test_verb_logic_analysis():
    """Test the verb-logic analysis system for error artifacts"""
    print("=== Test: Verb-Logic Analysis System ===")
    prover = ResponseProverMock(repository_path="/home/runner/work/named/named")
    
    # Test the verb analysis on mail2fbi.txt content
    verb_analysis = prover._analyze_verbs_logic(prover.mail_content)
    
    print(f"Total verbs analyzed: {len(verb_analysis)}")
    
    # Count error types
    multi_category = [r for r in verb_analysis if r.error_type == "multi_category"]
    zero_category = [r for r in verb_analysis if r.error_type == "zero_category"] 
    dimension_expansion = [r for r in verb_analysis if r.error_type == "dimension_expansion"]
    normal = [r for r in verb_analysis if r.error_type == "normal"]
    
    print(f"Multi-category conflicts: {len(multi_category)}")
    print(f"Zero-category verbs: {len(zero_category)}")
    print(f"Dimension expansions: {len(dimension_expansion)}")
    print(f"Normal classifications: {len(normal)}")
    
    # Show some examples of multi-category conflicts
    if multi_category:
        print("\nSample multi-category conflicts:")
        for result in multi_category[:3]:
            categories = [cat.value for cat in result.categories]
            print(f"  '{result.verb}' → {categories}")
    
    print()


def test_grouped_nodes_detection():
    """Test that grouped nodes scenarios are properly detected using verb-logic"""
    
    # Test case 1: Original mail2fbi.txt should trigger grouped nodes detection
    print("=== Test 1: Original mail2fbi.txt ===")
    prover = ResponseProverMock(repository_path="/home/runner/work/named/named")
    is_grouped = prover._detect_grouped_nodes_scenario()
    print(f"Grouped nodes detected: {is_grouped}")
    
    response = prover._generate_fsb_response()
    print(f"Response type: {'GROUPED NODES' if 'GROUPED NODES PROTOCOL' in response else 'STANDARD'}")
    print()
    
    # Test case 2: Create a non-grouped scenario 
    print("=== Test 2: Non-grouped scenario ===")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp.write("Simple email about weather and normal topics.")
        tmp_path = tmp.name
    
    try:
        prover_simple = ResponseProverMock(repository_path="/home/runner/work/named/named", mail_file=tmp_path)
        is_grouped_simple = prover_simple._detect_grouped_nodes_scenario()
        print(f"Grouped nodes detected: {is_grouped_simple}")
        
        response_simple = prover_simple._generate_fsb_response()
        print(f"Response type: {'GROUPED NODES' if 'GROUPED NODES PROTOCOL' in response_simple else 'STANDARD'}")
        print()
    finally:
        os.unlink(tmp_path)
    
    # Test case 3: Content with verb-logic conflicts but no infrastructure terms
    print("=== Test 3: Technical content without infrastructure ===")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp.write("Process data using secure encryption and analyze the results systematically.")
        tmp_path = tmp.name
    
    try:
        prover_tech = ResponseProverMock(repository_path="/home/runner/work/named/named", mail_file=tmp_path)
        is_grouped_tech = prover_tech._detect_grouped_nodes_scenario()
        print(f"Grouped nodes detected: {is_grouped_tech}")
        
        # Show verb analysis for this case
        verb_analysis = prover_tech._analyze_verbs_logic(prover_tech.mail_content)
        error_artifacts = [r for r in verb_analysis if r.error_type != "normal"]
        print(f"Error artifacts: {len(error_artifacts)}")
        print()
    finally:
        os.unlink(tmp_path)

    # Test case 4: Infrastructure terms with threat indicators and conflicts
    print("=== Test 4: Infrastructure + threats + verb conflicts ===")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp.write("Multiple systems compromised by rootkit affecting all servers in the network cluster. Process backup data to analyze the attack.")
        tmp_path = tmp.name
    
    try:
        prover_combined = ResponseProverMock(repository_path="/home/runner/work/named/named", mail_file=tmp_path)
        is_combined = prover_combined._detect_grouped_nodes_scenario()
        print(f"Grouped nodes detected: {is_combined}")
        
        response_combined = prover_combined._generate_fsb_response()
        print(f"Response type: {'GROUPED NODES' if 'GROUPED NODES PROTOCOL' in response_combined else 'STANDARD'}")
        
        # Show detailed verb analysis
        verb_analysis = prover_combined._analyze_verbs_logic(prover_combined.mail_content)
        print(f"Total verbs: {len(verb_analysis)}")
        print(f"Error artifacts: {len([r for r in verb_analysis if r.error_type != 'normal'])}")
        print()
    finally:
        os.unlink(tmp_path)


def run_tests():
    """Run all tests"""
    print("🧪 Testing Verb-Logic System for 0 Level Counter-Error Grouped Nodes")
    print("=" * 70)
    
    test_verb_logic_analysis()
    test_grouped_nodes_detection()
    
    print("✅ All verb-logic tests completed!")


if __name__ == "__main__":
    run_tests()