#!/usr/bin/env python3
"""
Compact Evolution Resource Principles - Demonstration Script
===========================================================

This script demonstrates the Compact Evolution Resource Principles system
with various examples showing categorization, compact representation, and
logic circuit generation for technical term processing.
"""

from compact_evolution import CompactEvolutionSystem, CategoryType
import json

def print_separator(title: str):
    """Print a formatted separator for demo sections"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)

def demonstrate_categorization(system: CompactEvolutionSystem):
    """Demonstrate the categorization system"""
    print_separator("CATEGORIZATION SYSTEM")
    
    print("Available categories and sample words:")
    for category, words in system.categories.items():
        print(f"\n{category.value.upper().replace('_', ' ')}:")
        # Show first 5 words from each category
        for word in words[:5]:
            compact_word = system.compact_mappings[word]
            print(f"  {word:20} -> {compact_word.compact_label} (weight: {compact_word.weight})")
        if len(words) > 5:
            print(f"  ... and {len(words) - 5} more words")

def demonstrate_subword_splitting(system: CompactEvolutionSystem):
    """Demonstrate sub-word splitting functionality"""
    print_separator("SUB-WORD DECOMPOSITION")
    
    sample_words = [
        "NeuralNetwork", "ConvolutionalLayer", "BinarySearch", 
        "QuickSort", "DigitalSignature", "AttentionMechanism"
    ]
    
    print("Sub-word decomposition examples:")
    for word in sample_words:
        if word in system.compact_mappings:
            compact_word = system.compact_mappings[word]
            print(f"{word:20} -> {compact_word.sub_words} (ratio: {compact_word.ratio})")

def demonstrate_compact_representation(system: CompactEvolutionSystem):
    """Demonstrate compact representation generation"""
    print_separator("COMPACT REPRESENTATION")
    
    test_cases = [
        ["Memory", "Process", "Store"],
        ["NeuralNetwork", "Encryption", "Bandwidth"],
        ["Execute", "Compile", "Debug", "Optimize"],
        ["TCP", "HTTP", "SSL", "DNS"]
    ]
    
    for i, words in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {words}")
        # Convert words to (word, category) tuples
        items = []
        for word in words:
            for category, category_words in system.categories.items():
                if word in category_words:
                    items.append((word, category))
                    break
        compact_rep = system.get_compact_representation(items)
        
        print(f"  Mathematical Expression: {compact_rep['mathematical_expression']}")
        print(f"  Compact Labels: {[item['label'] for item in compact_rep['compact_labels']]}")
        print(f"  Average Ratio: {sum(compact_rep['ratios']) / len(compact_rep['ratios']):.2f}")
        print(f"  Total Weight: {sum(compact_rep['weights']):.2f}")

def demonstrate_logic_circuits(system: CompactEvolutionSystem):
    """Demonstrate logic circuit generation"""
    print_separator("LOGIC CIRCUIT GENERATION")
    
    circuit_examples = [
        ("neural_processing", ["NeuralNetwork", "Process", "Memory"]),
        ("secure_communication", ["Encryption", "TCP", "Authentication"]),
        ("data_analysis", ["Algorithm", "Execute", "Store", "Compare"]),
        ("circuit_design", ["LogicGate", "FlipFlop", "Multiplexer"])
    ]
    
    for name, words in circuit_examples:
        print(f"\nCircuit: {name}")
        print(f"Input Words: {words}")
        
        try:
            # Convert words to (word, category) tuples
            items = []
            for word in words:
                for category, category_words in system.categories.items():
                    if word in category_words:
                        items.append((word, category))
                        break
            circuit = system.create_logic_circuit(name, items)
            print(f"  Inputs: {circuit.inputs[:5]}...")  # Show first 5 inputs
            print(f"  Operations: {circuit.operations}")
            print(f"  Outputs: {circuit.outputs}")
        except Exception as e:
            print(f"  Error creating circuit: {e}")

def demonstrate_request_processing(system: CompactEvolutionSystem):
    """Demonstrate full request processing"""
    print_separator("REQUEST PROCESSING")
    
    test_requests = [
        "Process the neural network with encryption and store in memory",
        "Execute binary search algorithm on the data structure",
        "Compile the code and debug using optimization techniques",
        "Establish TCP connection with SSL encryption for secure communication",
        "Apply convolutional layer to neural network with attention mechanism"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\nRequest {i}: {request}")
        result = system.process_request(request)
        
        print(f"  Status: {result['status']}")
        
        if result['status'] == 'APPROVE':
            print(f"  Identified Words: {result['identified_words']}")
            print(f"  Compact Expression: {result['compact_representation']['mathematical_expression']}")
            print(f"  Circuit Operations: {len(result['logic_circuit']['operations'])} operations")
            print(f"  Evolution Principle: {result['evolution_principle']}")
        else:
            print(f"  Reason: {result['reason']}")

def demonstrate_export_functionality(system: CompactEvolutionSystem):
    """Demonstrate data export functionality"""
    print_separator("EXPORT FUNCTIONALITY")
    
    print("Exporting category data...")
    categories = system.export_categories()
    
    # Show export structure for first category
    first_category = list(categories.keys())[0]
    first_data = categories[first_category]
    
    print(f"\nExample export for {first_category}:")
    print(f"  Total words: {len(first_data['words'])}")
    print(f"  Compact mappings: {len(first_data['compact_mappings'])}")
    
    # Show a few mappings
    print("\n  Sample mappings:")
    for word, mapping in list(first_data['compact_mappings'].items())[:3]:
        print(f"    {word}: {mapping}")
    
    # Export to JSON file
    export_file = "/tmp/compact_evolution_export.json"
    with open(export_file, 'w') as f:
        json.dump(categories, f, indent=2)
    print(f"\n  Full export saved to: {export_file}")

def demonstrate_race_condition_scheduler(system: CompactEvolutionSystem):
    """Demonstrate the 6pm race condition scheduler functionality"""
    print_separator("6PM RACE CONDITION SCHEDULER")
    
    print("The system includes a race condition scheduler that triggers")
    print("comprehensive word processing at 6pm intervals using all words")
    print("with random analyze cycles (2-4 range) as specified.")
    
    # Enable the scheduler
    system.enable_race_condition_scheduler(True)
    status = system.get_race_condition_status()
    
    print(f"\n📅 Scheduler Status:")
    print(f"  Enabled: {status['enabled']}")
    print(f"  Next 6pm trigger: {status['next_6pm_trigger']}")
    print(f"  Turn counter: {status['turn_counter']}")
    
    # Simulate a race condition
    print(f"\n🚀 Simulating 6pm race condition...")
    system.race_scheduler.race_condition_active = True
    system.race_scheduler.turn_counter += 1
    
    # Process a request during race condition
    result = system.process_request("Simulated 6pm turn processing")
    
    print(f"  Status: {result['status']}")
    print(f"  Total words processed: {len(result['identified_words'])}")
    
    if 'race_condition' in result:
        race_info = result['race_condition']
        print(f"  Race trigger: {race_info['trigger']}")
        print(f"  Turn counter: {race_info['turn_counter']}")
        print(f"  Words processed: {race_info['total_words_processed']}")
        print(f"  Analyze cycles: {race_info['analyze_cycles']}")
    
    # Show sample of processed words
    sample_words = result['identified_words'][:15]
    print(f"\n  Sample words (first 15): {sample_words}")
    
    # Verify random cycles
    race_words = system.race_scheduler.prepare_all_words_race(system.categories)
    word_counts = {}
    for word, category in race_words:
        word_counts[word] = word_counts.get(word, 0) + 1
    
    # Find examples of repeated words
    repeated_examples = [(word, count) for word, count in word_counts.items() if count > 1][:3]
    print(f"\n  Random cycle examples:")
    for word, count in repeated_examples:
        print(f"    '{word}' processed {count} times")
    
    print(f"\n✅ Race condition creates intentional processing conflicts")
    print(f"   using all {len(system.categories)} word categories for enhanced parallelism")

def demonstrate_mathematical_operations(system: CompactEvolutionSystem):
    """Demonstrate mathematical operations with compact representations"""
    print_separator("MATHEMATICAL OPERATIONS")
    
    # Simulate mathematical operations like in the simulation logs
    words = ["Memory", "Process", "NeuralNetwork", "Encryption"]
    # Convert words to (word, category) tuples
    items = []
    for word in words:
        for category, category_words in system.categories.items():
            if word in category_words:
                items.append((word, category))
                break
    compact_rep = system.get_compact_representation(items)
    
    labels = [item['label'] for item in compact_rep['compact_labels']]
    weights = compact_rep['weights']
    ratios = compact_rep['ratios']
    
    print("Compact labels and operations:")
    for i, (label, weight, ratio) in enumerate(zip(labels, weights, ratios)):
        print(f"  {label} = {compact_rep['compact_labels'][i]['original']}")
        print(f"    Weight: {weight}, Ratio: {ratio}")
    
    print(f"\nMathematical expressions:")
    print(f"  Basic sum: {' + '.join(labels)} = {len(labels)}")
    print(f"  Weighted sum: {' + '.join([f'{w}*{l}' for l, w in zip(labels, weights)])}")
    print(f"  Average ratio: ({' + '.join([str(r) for r in ratios])}) / {len(ratios)} = {sum(ratios)/len(ratios):.2f}")
    
    # Simulate operations like in simulation logs
    print(f"\nSimulation log style operations:")
    if len(labels) >= 2:
        print(f"  {labels[0]} + {labels[0]} = 2{labels[0]}")
        print(f"  2{labels[0]} / 4 = 0.5{labels[0]}")
        print(f"  0.5{labels[0]} * 2 = 1{labels[0]}")

def main():
    """Main demonstration function"""
    print("COMPACT EVOLUTION RESOURCE PRINCIPLES")
    print("Demonstration of English tech word categorization and")
    print("IA architecture mapping for logic circuit definition")
    
    # Initialize the system
    system = CompactEvolutionSystem()
    
    # Run all demonstrations
    demonstrate_categorization(system)
    demonstrate_subword_splitting(system)
    demonstrate_compact_representation(system)
    demonstrate_logic_circuits(system)
    demonstrate_request_processing(system)
    demonstrate_race_condition_scheduler(system)
    demonstrate_mathematical_operations(system)
    demonstrate_export_functionality(system)
    
    print_separator("DEMONSTRATION COMPLETE")
    print("The Compact Evolution Resource Principles system successfully:")
    print("✓ Categorizes English technical words")
    print("✓ Decomposes words into sub-components")
    print("✓ Creates compact representations with letters")
    print("✓ Maps to computer IA architecture concepts")
    print("✓ Generates logic circuits for request processing")
    print("✓ Implements 6pm race condition scheduler with all words")
    print("✓ Uses random analyze cycles (2-4 range) for enhanced parallelism")
    print("✓ Provides mathematical operations on compact forms")
    print("✓ Exports data for integration with existing systems")

if __name__ == "__main__":
    main()