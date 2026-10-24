#!/usr/bin/env python3
"""
Enhanced Compact Evolution with Mathematical Abstractions
=========================================================

Demonstration of the enhanced system with mathematical formulations
and dimensional analysis for the 8 categories.
"""

from compact_evolution import CompactEvolutionSystem
from mathematical_abstractions import MathematicalAbstractionEngine
from knowledge_system import RedQueenKnowledgeSystem
from rq_random_utils import get_rq_random
import json
import os


def demonstrate_enhanced_system():
    """Demonstrate the complete enhanced system"""
    print("=" * 70)
    print("ENHANCED COMPACT EVOLUTION RESOURCE PRINCIPLES")
    print("Mathematical Abstractions & Dimensional Analysis")
    print("=" * 70)

    # Initialize systems
    evolution_system = CompactEvolutionSystem()
    math_engine = MathematicalAbstractionEngine(evolution_system)

    print("\n[SYSTEM] SYSTEM OVERVIEW:")
    sys_dims = math_engine.system_dimensions
    print(f"  Total Categories: {math_engine.n_categories}")
    print(f"  Total Dimensions: {sys_dims.total_dimensions}")
    print(f"  Complexity Measure: {sys_dims.complexity_measure:.3f}")
    print(f"  Information Density: {sys_dims.information_density:.3f}")

    print(f"\n[MATH] DIMENSIONAL FORMULAS:")
    formulas = math_engine.get_dimensional_formula()
    for name, formula in formulas.items():
        if name.startswith('category_'):
            category_name = name.replace('category_', '').replace('_', ' ').title()
            print(f"  {category_name}: {formula}")

    print(f"\n[SYSTEM] SYSTEM FORMULAS:")
    system_formulas = {k: v for k, v in formulas.items() if not k.startswith('category_')}
    for name, formula in system_formulas.items():
        print(f"  {name.replace('_', ' ').title()}: {formula}")

    print(f"\n[ANALYSIS] INTERACTION ANALYSIS:")
    matrix = sys_dims.interaction_matrix
    categories = list(evolution_system.categories.keys())

    print("  Strong interactions (>0.9):")
    for i, cat1 in enumerate(categories):
        for j, cat2 in enumerate(categories):
            if i != j and matrix[i][j] > 0.9:
                print(f"    {cat1.value} <-> {cat2.value}: {matrix[i][j]:.3f}")

    return evolution_system, math_engine


def test_enhanced_processing():
    """Test enhanced processing with mathematical analysis"""
    print(f"\n" + "=" * 70)
    print("ENHANCED REQUEST PROCESSING")
    print("=" * 70)

    evolution_system, math_engine = demonstrate_enhanced_system()

    # Configure axes for demonstration
    evolution_system.enable_hyperthreading(True, cores=2, threads_per_core=2)
    evolution_system.configure_time_axis(timeslice_ms=5, dataset_size=16, chunk_size=4)

    test_requests = [
        "process neural network with memory optimization and encryption",
        "execute algorithm using data structure with circuit components",
        "compile secure network protocol with authentication"
    ]

    for i, request in enumerate(test_requests, 1):
        print(f"\n[REQUEST] REQUEST {i}: {request}")

        # Standard processing
        result = evolution_system.process_request(request)

        if result['status'] == 'APPROVE':
            words = result['identified_words']
            compact_expr = result['compact_representation']['mathematical_expression']

            print(f"  Status: {result['status']}")
            print(f"  Words: {words}")
            print(f"  Compact: {compact_expr}")

            # Hyperthreading execution plan (compact)
            ep = result['execution_plan']
            print(
                f"  [EXEC] HT={'ON' if ep['hyperthreading'] else 'OFF'} C={ep['cores']} T/C={ep['threads_per_core']} TotalT={ep['total_threads']}")
            # Show one line per thread with up to two ops
            for tid, ops in ep['assignment'].items():
                preview = ops[:2]
                suffix = ' ...' if len(ops) > 2 else ''
                print(f"    {tid}: {preview}{suffix}")

            # Time axis timeline excerpts
            tp = result['time_axis_plan']
            print(f"  [TIME] slice={tp['timeslice_ms']}ms dataset={tp['dataset_size']} chunk={tp['chunk_size']}")
            for tid, segments in tp['timeline'].items():
                seg_preview = segments[:2]
                print(f"    {tid}: {seg_preview} ...")

            # Enhanced mathematical analysis
            evolution = math_engine.calculate_dimensional_evolution(words)
            if 'error' not in evolution:
                print(f"  [DIMENSIONAL] Dimensional Formula: {evolution['dimensional_formula']}")
                print(f"  [MAGNITUDE] Magnitude: {evolution['magnitude']:.3f}")
                print(f"  [DIMENSION] Dimensionality: {evolution['dimensionality']}")
                print(f"  [CATEGORIES] Categories: {[cat.value for cat in evolution['categories_involved']]}")

                # Calculate mathematical operations like in simulation logs
                labels = [item['label'] for item in result['compact_representation']['compact_labels']]
                if len(labels) >= 2:
                    A = labels[0]
                    print(f"  [OPERATIONS] {A} + {A} = 2{A}, 2{A}/4 = 0.5{A}, 0.5{A}x2 = {A}")
        else:
            print(f"  Status: {result['status']} - {result['reason']}")


def export_complete_analysis():
    """Export complete mathematical analysis"""
    print(f"\n" + "=" * 70)
    print("COMPLETE MATHEMATICAL ANALYSIS EXPORT")
    print("=" * 70)

    evolution_system = CompactEvolutionSystem()
    math_engine = MathematicalAbstractionEngine(evolution_system)

    # Export analysis
    analysis = math_engine.export_mathematical_analysis()

    # Save to file
    export_file = "tmp/mathematical_analysis_export.json"
    os.makedirs(os.path.dirname(export_file), exist_ok=True)
    with open(export_file, 'w') as f:
        json.dump(analysis, f, indent=2, default=str)

    print(f"[FILE] Complete analysis exported to: {export_file}")

    # Show summary
    print(f"\n[SUMMARY] ANALYSIS SUMMARY:")
    overview = analysis['system_overview']
    print(f"  Categories: {overview['total_categories']}")
    print(f"  Dimensions: {overview['total_dimensions']}")
    print(f"  Complexity: {overview['complexity_measure']:.3f}")
    print(f"  Info Density: {overview['information_density']:.3f}")

    print(f"\n[DATA] CATEGORY MAGNITUDES:")
    for cat_name, vec_data in analysis['dimensional_vectors'].items():
        magnitude = vec_data['magnitude']
        entropy = vec_data['entropy']
        print(f"  {cat_name.replace('_', ' ').title():20}: Magnitude={magnitude:.3f}, Entropy={entropy:.3f}")


def demonstrate_categorical_mathematics():
    """Demonstrate mathematical properties of each category"""
    print(f"\n" + "=" * 70)
    print("CATEGORICAL MATHEMATICAL PROPERTIES")
    print("=" * 70)

    evolution_system = CompactEvolutionSystem()
    math_engine = MathematicalAbstractionEngine(evolution_system)

    for category, vec in math_engine.dimensional_vectors.items():
        print(f"\n[CATEGORY] {category.value.upper().replace('_', ' ')}:")

        # Words in category
        words = evolution_system.categories[category]
        preview = ', '.join(words[:3]) + ("..." if len(words) > 3 else "")
        print(f"  Words: {len(words)} ({preview})")

        # Mathematical properties (compact)
        dims = '[' + ', '.join(f'{x:.2f}' for x in vec.dimensions) + ']'
        print(f"  [DIMENSIONS] Dimensions: {dims}")
        print(f"  [MAGNITUDE] Magnitude: {vec.magnitude:.3f}")
        print(f"  [ENTROPY] Entropy: {vec.entropy:.3f}")

        # Unit vector (normalized direction)
        unit = '[' + ', '.join(f'{x:.3f}' for x in vec.unit_vector) + ']'
        print(f"  [VECTOR] Unit Vector: {unit}")

        # Find strongest dimensional component
        max_dim_idx = vec.dimensions.index(max(vec.dimensions)) if vec.dimensions else 0
        dim_names = ['Length', 'Decomposition', 'Ratio', 'Weight', 'Parameters', 'Compact']
        print(f"  [DOMINANT] Dominant: {dim_names[max_dim_idx]} ({vec.dimensions[max_dim_idx]:.2f})")


def demonstrate_knowledge_integration():
    """Demonstrate integration of Knowledge System with existing components"""
    print(f"\n" + "=" * 70)
    print("KNOWLEDGE SYSTEM INTEGRATION")
    print("4-Step Process: Load → Analyze → Reload @ 51% → Output")
    print("=" * 70)

    # Initialize systems
    evolution_system = CompactEvolutionSystem()
    math_engine = MathematicalAbstractionEngine(evolution_system)
    knowledge_system = RedQueenKnowledgeSystem()

    print(f"\n[INTEGRATION] SYSTEMS INITIALIZED:")
    print(f"  ✓ Compact Evolution System")
    print(f"  ✓ Mathematical Abstraction Engine")
    print(f"  ✓ Red&Queen Knowledge System")
    
    # Show R&Q Random System info
    rq_system = get_rq_random()
    rq_info = rq_system.get_system_info()
    print(f"  ✓ R&Q Random System ({rq_info['seed_info']['type']})")
    print(f"    Seed: {rq_info['seed_info']['seed']:08X}")
    print(f"    Operations: {rq_info['operations_performed']}")

    # Test knowledge system with mathematical integration
    test_request = "optimize parallel memory processing with secure encryption algorithms"
    
    print(f"\n[REQUEST] Processing: {test_request}")
    print("-" * 50)
    
    # Process through knowledge system (includes compact evolution)
    knowledge_result = knowledge_system.make_we_knowledged(test_request)
    
    # Get mathematical analysis if successful
    if knowledge_result["status"] == "APPROVE":
        # Extract words from the knowledge system processing
        evolution_result = evolution_system.process_request(test_request)
        if evolution_result["status"] == "APPROVE":
            words = evolution_result["identified_words"]
            math_analysis = math_engine.calculate_dimensional_evolution(words)
            
            print(f"\n[MATHEMATICS] DIMENSIONAL ANALYSIS:")
            if 'error' not in math_analysis:
                print(f"  Formula: {math_analysis['dimensional_formula']}")
                print(f"  Magnitude: {math_analysis['magnitude']:.3f}")
                print(f"  Dimensionality: {math_analysis['dimensionality']}")
                print(f"  Categories: {[cat.value for cat in math_analysis['categories_involved']]}")
    
    # Display integration summary
    print(f"\n[SUMMARY] KNOWLEDGE INTEGRATION:")
    print(f"  Status: {knowledge_result['status']}")
    print(f"  Steps Completed: {len(knowledge_result['steps'])}/4")
    print(f"  Random Check: {knowledge_result['random_check']}")
    print(f"  Total Shuffles: {knowledge_result['steps']['output']['summary']['total_shuffles']}")
    
    return knowledge_result


def main():
    """Main demonstration function"""
    print("COMPACT EVOLUTION RESOURCE PRINCIPLES")
    print("Enhanced with Mathematical Abstractions and Dimensional Analysis")
    print("Taking math and 8 categories abstractly using mathematical formulations")

    # Run all demonstrations
    test_enhanced_processing()
    demonstrate_categorical_mathematics()
    export_complete_analysis()
    demonstrate_knowledge_integration()  # New integration demo

    print(f"\n" + "=" * 70)
    print("ENHANCED SYSTEM DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("Mathematical abstractions applied to 8 categories")
    print("Dimensional formulas calculated for system components")
    print("Interaction matrix computed for category relationships")
    print("Information theory metrics (entropy, complexity) measured")
    print("Enhanced request processing with dimensional analysis")
    print("Complete mathematical framework for compact evolution")
    print("✓ Red&Queen Knowledge System with 4-step process")
    print("✓ Random analyze cycles (2-4) with R&Q shuffle patterns")


if __name__ == "__main__":
    main()
