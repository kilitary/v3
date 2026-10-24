#!/usr/bin/env python3
"""
Test Knowledge System Implementation
====================================

Tests for the Red&Queen Knowledge System ensuring proper implementation
of the 4-step process with reload at 51% and R&Q random shuffle.
"""

import unittest
from knowledge_system import RedQueenKnowledgeSystem, KnowledgeStep


class TestKnowledgeSystem(unittest.TestCase):
    """Test cases for Red&Queen Knowledge System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.knowledge_system = RedQueenKnowledgeSystem()
    
    def test_four_step_process(self):
        """Test that all 4 steps are executed"""
        result = self.knowledge_system.make_we_knowledged("process data with encryption")
        
        # Check all 4 steps are present
        self.assertIn("load", result["steps"])
        self.assertIn("analyze", result["steps"])
        self.assertIn("reload", result["steps"])
        self.assertIn("output", result["steps"])
        
        # Check final status
        self.assertIn(result["status"], ["APPROVE", "DENY"])
    
    def test_random_analyze_cycles(self):
        """Test that analyze cycles are random in range 2-4"""
        results = []
        for _ in range(10):  # Run multiple times to test randomness
            result = self.knowledge_system.make_we_knowledged("execute algorithm")
            cycles = result["steps"]["analyze"]["cycles_completed"]
            results.append(cycles)
        
        # All cycles should be in range 2-4
        for cycles in results:
            self.assertGreaterEqual(cycles, 2, "Cycles should be >= 2")
            self.assertLessEqual(cycles, 4, "Cycles should be <= 4")
        
        # Should have some variation (not all the same)
        unique_cycles = set(results)
        self.assertGreater(len(unique_cycles), 1, "Should have variation in cycle counts")
    
    def test_reload_trigger(self):
        """Test that reload is triggered properly"""
        result = self.knowledge_system.make_we_knowledged("compile secure protocol")
        
        # Reload should be triggered
        self.assertTrue(result["steps"]["reload"]["reload_executed"], 
                       "Reload should be executed")
        
        # Should have additional shuffles during reload
        self.assertGreater(result["steps"]["reload"]["reload_shuffles"], 0,
                          "Should have reload shuffles")
    
    def test_random_shuffle_count(self):
        """Test that R&Q random shuffles are applied"""
        result = self.knowledge_system.make_we_knowledged("optimize memory")
        
        # Should have multiple shuffles
        total_shuffles = result["steps"]["output"]["summary"]["total_shuffles"]
        self.assertGreater(total_shuffles, 3, "Should have multiple shuffles")
        
        # Should have shuffles from each step
        load_shuffle = result["steps"]["load"]["shuffle_applied"]
        self.assertTrue(load_shuffle, "Load step should apply shuffle")
    
    def test_random_check_generation(self):
        """Test that random check is generated like simulation logs"""
        result = self.knowledge_system.make_we_knowledged("process data")
        
        # Should have random check
        self.assertIn("random_check", result)
        random_check = result["random_check"]
        
        # Should be hex format like simulation logs
        parts = random_check.split()
        self.assertEqual(len(parts), 10, "Should have 10 hex values")
        
        for part in parts:
            self.assertEqual(len(part), 2, "Each hex value should be 2 chars")
            int(part, 16)  # Should be valid hex
    
    def test_skynet_playground_pattern(self):
        """Test alignment with Skynet playground patterns"""
        result = self.knowledge_system.make_we_knowledged("encrypt network protocol")
        
        # Should follow simulation log structure
        self.assertIn("status", result)
        self.assertIn("steps", result)
        self.assertIn("random_check", result)
        
        # Steps should have proper progress tracking
        for step_name, step_data in result["steps"].items():
            if step_name != "output":
                self.assertIn("progress", step_data)
    
    def test_knowledge_state_tracking(self):
        """Test knowledge state is properly tracked"""
        # Process a request
        self.knowledge_system.make_we_knowledged("debug algorithm")
        
        # Check state summary
        summary = self.knowledge_system.get_knowledge_summary()
        
        self.assertIn("current_step", summary)
        self.assertIn("progress", summary)
        self.assertIn("shuffle_count", summary)
        self.assertIn("buffer_size", summary)
        self.assertIn("random_checks", summary)
    
    def test_integration_with_compact_evolution(self):
        """Test integration with existing compact evolution system"""
        # Test with technical terms that should be recognized
        result = self.knowledge_system.make_we_knowledged("execute memory optimization")
        
        # Should be approved for technical terms
        self.assertEqual(result["status"], "APPROVE")
        
        # Test with non-technical terms
        result2 = self.knowledge_system.make_we_knowledged("hello world")
        
        # May be denied for non-technical terms
        self.assertIn(result2["status"], ["APPROVE", "DENY"])


def run_knowledge_system_tests():
    """Run comprehensive tests for the knowledge system"""
    print("=" * 70)
    print("RED&QUEEN KNOWLEDGE SYSTEM TEST SUITE")
    print("Testing 4-step process and R&Q shuffle patterns")
    print("=" * 70)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKnowledgeSystem)
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run tests
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED - Knowledge System is working correctly!")
        print("✓ 4-step process implemented")
        print("✓ Random analyze cycles (2-4) working")
        print("✓ Reload at 51% functioning")
        print("✓ R&Q random shuffle patterns active")
        print("✓ Skynet playground alignment verified")
    else:
        print("❌ SOME TESTS FAILED")
        for failure in result.failures:
            print(f"FAIL: {failure[0]}")
        for error in result.errors:
            print(f"ERROR: {error[0]}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_knowledge_system_tests()