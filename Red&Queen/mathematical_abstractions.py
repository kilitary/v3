#!/usr/bin/env python3
"""
Mathematical Abstractions for Compact Evolution Resource Principles
==================================================================

Provides mathematical formulations and dimensional analysis for the 8 categories
and overall system dimensionality calculations.
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from compact_evolution import CategoryType, CompactEvolutionSystem

@dataclass
class DimensionalVector:
    """Represents a multi-dimensional vector for category analysis"""
    category: CategoryType
    dimensions: List[float]
    magnitude: float
    unit_vector: List[float]
    entropy: float

@dataclass
class SystemDimensions:
    """Mathematical representation of system dimensions"""
    total_dimensions: int
    category_dimensions: Dict[CategoryType, int]
    interaction_matrix: List[List[float]]
    complexity_measure: float
    information_density: float

def vector_norm(vector: List[float]) -> float:
    """Calculate Euclidean norm of a vector"""
    return math.sqrt(sum(x * x for x in vector))

def vector_normalize(vector: List[float]) -> List[float]:
    """Normalize a vector to unit length"""
    norm = vector_norm(vector)
    return [x / norm for x in vector] if norm > 0 else [0.0] * len(vector)

def vector_dot(v1: List[float], v2: List[float]) -> float:
    """Calculate dot product of two vectors"""
    return sum(a * b for a, b in zip(v1, v2))

def matrix_eigenvalue_sum(matrix: List[List[float]]) -> float:
    """Approximate sum of absolute eigenvalues using trace and determinant"""
    n = len(matrix)
    if n == 0:
        return 0.0
    
    # For small matrices, use approximations
    trace = sum(matrix[i][i] for i in range(n))
    
    if n == 1:
        return abs(trace)
    elif n == 2:
        # For 2x2: eigenvalues can be calculated exactly
        a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
        det = a * d - b * c
        discriminant = trace * trace - 4 * det
        if discriminant >= 0:
            sqrt_disc = math.sqrt(discriminant)
            lambda1 = (trace + sqrt_disc) / 2
            lambda2 = (trace - sqrt_disc) / 2
            return abs(lambda1) + abs(lambda2)
        else:
            # Complex eigenvalues
            return abs(trace)
    else:
        # For larger matrices, use trace as approximation
        return abs(trace)

class MathematicalAbstractionEngine:
    """Engine for mathematical analysis of the Compact Evolution system"""
    
    def __init__(self, evolution_system: CompactEvolutionSystem):
        self.evolution_system = evolution_system
        self.n_categories = len(CategoryType)
        self.dimensional_vectors = {}
        self.system_dimensions = None
        self._calculate_mathematical_abstractions()
    
    def _calculate_mathematical_abstractions(self):
        """Calculate mathematical abstractions for all categories"""
        # Calculate dimensional vectors for each category
        for category in CategoryType:
            self.dimensional_vectors[category] = self._calculate_category_dimensions(category)
        
        # Calculate overall system dimensions
        self.system_dimensions = self._calculate_system_dimensions()
    
    def _calculate_category_dimensions(self, category: CategoryType) -> DimensionalVector:
        """Calculate dimensional representation for a category"""
        words = self.evolution_system.categories[category]
        n_words = len(words)
        
        # Create feature vector based on word properties
        features = []
        for word in words:
            if word in self.evolution_system.compact_mappings:
                compact_word = self.evolution_system.compact_mappings[word]
                word_features = [
                    len(word),                          # Length dimension
                    len(compact_word.sub_words),        # Decomposition dimension
                    compact_word.ratio,                 # Compression dimension
                    compact_word.weight,                # Importance dimension
                    len(compact_word.parameters),       # Parameter dimension
                    ord(compact_word.compact_label[0]) - ord('A')  # Label dimension
                ]
                features.append(word_features)
        
        if not features:
            # Default vector for empty categories
            dimensions = [0.0] * 6
            magnitude = 0.0
            unit_vector = [0.0] * 6
            entropy = 0.0
        else:
            # Calculate statistical measures (mean of features)
            n_features = len(features)
            dimensions = [sum(features[i][j] for i in range(n_features)) / n_features 
                         for j in range(6)]
            magnitude = vector_norm(dimensions)
            unit_vector = vector_normalize(dimensions)
            
            # Calculate information entropy
            word_lengths = [len(word) for word in words]
            if word_lengths:
                # Normalize to probabilities
                total_length = sum(word_lengths)
                probabilities = [l / total_length for l in word_lengths]
                entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
            else:
                entropy = 0.0
        
        return DimensionalVector(
            category=category,
            dimensions=dimensions,
            magnitude=magnitude,
            unit_vector=unit_vector,
            entropy=entropy
        )
    
    def _calculate_system_dimensions(self) -> SystemDimensions:
        """Calculate overall system dimensional properties"""
        # Total dimensions = sum of individual category dimensions
        total_dims = sum(len(self.dimensional_vectors[cat].dimensions) 
                        for cat in CategoryType)
        
        # Category-specific dimensions
        category_dims = {cat: len(self.dimensional_vectors[cat].dimensions) 
                        for cat in CategoryType}
        
        # Interaction matrix between categories
        interaction_matrix = self._calculate_interaction_matrix()
        
        # Complexity measure based on eigenvalues approximation
        complexity_measure = matrix_eigenvalue_sum(interaction_matrix)
        
        # Information density
        total_words = sum(len(self.evolution_system.categories[cat]) for cat in CategoryType)
        total_entropy = sum(self.dimensional_vectors[cat].entropy for cat in CategoryType)
        information_density = total_entropy / total_words if total_words > 0 else 0.0
        
        return SystemDimensions(
            total_dimensions=total_dims,
            category_dimensions=category_dims,
            interaction_matrix=interaction_matrix,
            complexity_measure=complexity_measure,
            information_density=information_density
        )
    
    def _calculate_interaction_matrix(self) -> List[List[float]]:
        """Calculate interaction matrix between categories"""
        n = self.n_categories
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        
        categories = list(CategoryType)
        
        for i, cat1 in enumerate(categories):
            for j, cat2 in enumerate(categories):
                if i == j:
                    # Diagonal: self-interaction (magnitude)
                    matrix[i][j] = self.dimensional_vectors[cat1].magnitude
                else:
                    # Off-diagonal: cross-category interaction (dot product)
                    vec1 = self.dimensional_vectors[cat1].unit_vector
                    vec2 = self.dimensional_vectors[cat2].unit_vector
                    matrix[i][j] = vector_dot(vec1, vec2)
        
        return matrix
    
    def get_dimensional_formula(self) -> Dict[str, str]:
        """Generate dimensional formulas for the system"""
        formulas = {}
        
        # Category-specific formulas
        for category in CategoryType:
            vec = self.dimensional_vectors[category]
            formula = self._generate_category_formula(category, vec)
            formulas[f"category_{category.value}"] = formula
        
        # System-wide formulas
        formulas["total_dimensions"] = f"D_total = Σ(D_i) = {self.system_dimensions.total_dimensions}"
        formulas["complexity"] = f"C_system = ||λ|| = {self.system_dimensions.complexity_measure:.3f}"
        formulas["information_density"] = f"ρ_info = H_total/N_words = {self.system_dimensions.information_density:.3f}"
        
        # Interaction formula
        formulas["interaction_strength"] = self._generate_interaction_formula()
        
        return formulas
    
    def _generate_category_formula(self, category: CategoryType, vec: DimensionalVector) -> str:
        """Generate mathematical formula for a category"""
        dims = vec.dimensions
        magnitude = vec.magnitude
        entropy = vec.entropy
        
        # Create symbolic representation
        dim_symbols = ['L', 'D', 'R', 'W', 'P', 'C']  # Length, Decomp, Ratio, Weight, Params, Compact
        
        formula_parts = []
        for i, (symbol, value) in enumerate(zip(dim_symbols, dims)):
            if value != 0:
                formula_parts.append(f"{value:.2f}·{symbol}")
        
        if formula_parts:
            formula = f"⟨{', '.join(formula_parts)}⟩"
        else:
            formula = "⟨0⟩"
        
        formula += f" || ||v|| = {magnitude:.3f}, H = {entropy:.3f}"
        
        return formula
    
    def _generate_interaction_formula(self) -> str:
        """Generate interaction strength formula"""
        matrix = self.system_dimensions.interaction_matrix
        
        # Calculate off-diagonal sum (total interaction strength)
        n = len(matrix)
        if n == 0:
            return "I_avg = 0"
        
        total_sum = sum(sum(row) for row in matrix)
        trace = sum(matrix[i][i] for i in range(n))
        off_diagonal_sum = total_sum - trace
        avg_interaction = off_diagonal_sum / (n * (n - 1)) if n > 1 else 0
        
        return f"I_avg = (Σᵢⱼ Mᵢⱼ - Tr(M))/(n²-n) = {avg_interaction:.3f}"
    
    def calculate_dimensional_evolution(self, words: List[str]) -> Dict:
        """Calculate dimensional evolution for a set of words"""
        if not words:
            return {"error": "No words provided"}
        
        # Find categories for words
        word_categories = {}
        for word in words:
            for category, category_words in self.evolution_system.categories.items():
                if word in category_words:
                    word_categories[word] = category
                    break
        
        if not word_categories:
            return {"error": "No recognized words found"}
        
        # Calculate evolution vector
        evolution_vector = [0.0] * 6  # 6-dimensional space
        total_magnitude = 0.0
        
        for word, category in word_categories.items():
            if word in self.evolution_system.compact_mappings:
                compact_word = self.evolution_system.compact_mappings[word]
                word_vector = [
                    len(word),
                    len(compact_word.sub_words),
                    compact_word.ratio,
                    compact_word.weight,
                    len(compact_word.parameters),
                    ord(compact_word.compact_label[0]) - ord('A')
                ]
                # Add to evolution vector
                for i in range(6):
                    evolution_vector[i] += word_vector[i]
                total_magnitude += vector_norm(word_vector)
        
        # Normalize
        n_words = len(word_categories)
        evolution_vector = [x / n_words for x in evolution_vector]
        avg_magnitude = total_magnitude / n_words
        
        # Calculate dimensional trajectory
        trajectory = {
            "evolution_vector": evolution_vector,
            "magnitude": float(avg_magnitude),
            "dimensionality": 6,
            "word_count": n_words,
            "categories_involved": list(set(word_categories.values())),
            "dimensional_formula": self._format_evolution_formula(evolution_vector, avg_magnitude)
        }
        
        return trajectory
    
    def _format_evolution_formula(self, vector: List[float], magnitude: float) -> str:
        """Format evolution formula for display"""
        dim_symbols = ['L', 'D', 'R', 'W', 'P', 'C']
        
        terms = []
        for i, (symbol, value) in enumerate(zip(dim_symbols, vector)):
            if abs(value) > 0.01:  # Only include significant terms
                terms.append(f"{value:.2f}·{symbol}")
        
        if terms:
            formula = f"E⃗ = ⟨{', '.join(terms)}⟩"
        else:
            formula = "E⃗ = ⟨0⟩"
        
        formula += f" || ||E⃗|| = {magnitude:.3f}"
        
        return formula
    
    def export_mathematical_analysis(self) -> Dict:
        """Export complete mathematical analysis"""
        return {
            "system_overview": {
                "total_categories": self.n_categories,
                "total_dimensions": self.system_dimensions.total_dimensions,
                "complexity_measure": self.system_dimensions.complexity_measure,
                "information_density": self.system_dimensions.information_density
            },
            "dimensional_vectors": {
                cat.value: {  # Convert enum to string
                    "dimensions": vec.dimensions,
                    "magnitude": vec.magnitude,
                    "unit_vector": vec.unit_vector,
                    "entropy": vec.entropy
                } for cat, vec in self.dimensional_vectors.items()
            },
            "interaction_matrix": self.system_dimensions.interaction_matrix,
            "dimensional_formulas": self.get_dimensional_formula(),
            "category_dimensions": {cat.value: dim for cat, dim in self.system_dimensions.category_dimensions.items()}  # Convert enum keys
        }

def main():
    """Demonstration of mathematical abstractions"""
    print("=== Mathematical Abstractions for Compact Evolution ===\n")
    
    # Initialize systems
    evolution_system = CompactEvolutionSystem()
    math_engine = MathematicalAbstractionEngine(evolution_system)
    
    # Display dimensional analysis
    print("DIMENSIONAL ANALYSIS:")
    print("=" * 50)
    
    formulas = math_engine.get_dimensional_formula()
    for name, formula in formulas.items():
        print(f"{name}: {formula}")
    
    print(f"\nSYSTEM DIMENSIONS:")
    print("=" * 50)
    sys_dims = math_engine.system_dimensions
    print(f"Total Dimensions: {sys_dims.total_dimensions}")
    print(f"Complexity Measure: {sys_dims.complexity_measure:.3f}")
    print(f"Information Density: {sys_dims.information_density:.3f}")
    
    print(f"\nCATEGORY DIMENSIONAL VECTORS:")
    print("=" * 50)
    for category, vec in math_engine.dimensional_vectors.items():
        print(f"{category.value}:")
        print(f"  Magnitude: {vec.magnitude:.3f}")
        print(f"  Entropy: {vec.entropy:.3f}")
        print(f"  Dimensions: {vec.dimensions}")
    
    print(f"\nINTERACTION MATRIX:")
    print("=" * 50)
    print(math_engine.system_dimensions.interaction_matrix)
    
    # Test dimensional evolution
    print(f"\nDIMENSIONAL EVOLUTION EXAMPLE:")
    print("=" * 50)
    test_words = ["Memory", "Process", "NeuralNetwork", "Encryption"]
    evolution = math_engine.calculate_dimensional_evolution(test_words)
    
    if "error" not in evolution:
        print(f"Words: {test_words}")
        print(f"Evolution Formula: {evolution['dimensional_formula']}")
        print(f"Magnitude: {evolution['magnitude']:.3f}")
        print(f"Categories: {[cat.value for cat in evolution['categories_involved']]}")

if __name__ == "__main__":
    main()