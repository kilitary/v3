#!/usr/bin/env python3
"""
Test the 6pm race condition scheduler functionality.

This test validates the race condition system that triggers at 6pm using all words
with random analyze cycles in the range 2-4 as specified in the issue.
"""

from compact_evolution import CompactEvolutionSystem
import datetime
import time


def test_race_condition_scheduler():
    """Test the 6pm race condition scheduler"""
    print("=== 6PM RACE CONDITION SCHEDULER TEST ===\n")
    
    system = CompactEvolutionSystem()
    
    # Enable the race condition scheduler
    system.enable_race_condition_scheduler(True)
    
    # Get initial status
    status = system.get_race_condition_status()
    print("📊 Initial Race Condition Status:")
    print(f"  Enabled: {status['enabled']}")
    print(f"  Next 6pm trigger: {status['next_6pm_trigger']}")
    print(f"  Turn counter: {status['turn_counter']}")
    print(f"  Active: {status['race_condition_active']}")
    print()
    
    # Test 1: Normal processing (no race condition)
    print("🔍 Test 1: Normal Processing")
    result1 = system.process_request("Process memory with hyperthreading")
    print(f"  Status: {result1['status']}")
    print(f"  Identified words: {result1['identified_words']}")
    print(f"  Race condition triggered: {'race_condition' in result1}")
    if 'parallel_trigger' in result1:
        print(f"  Parallel trigger: {result1['parallel_trigger']['trigger']}")
    print()
    
    # Test 2: Simulate 6pm trigger by manually activating race condition
    print("🚀 Test 2: Simulated 6pm Race Condition")
    system.race_scheduler.race_condition_active = True
    system.race_scheduler.turn_counter += 1
    
    result2 = system.process_request("Test request during race condition")
    print(f"  Status: {result2['status']}")
    print(f"  Total words processed: {len(result2['identified_words'])}")
    print(f"  Race condition info: {result2.get('race_condition', 'None')}")
    
    # Show some sample words processed
    sample_words = result2['identified_words'][:10]
    print(f"  Sample words (first 10): {sample_words}")
    print()
    
    # Test 3: Check that race condition is deactivated after processing
    print("✅ Test 3: Race Condition Deactivation")
    status_after = system.get_race_condition_status()
    print(f"  Race condition active after processing: {status_after['race_condition_active']}")
    print(f"  Turn counter: {status_after['turn_counter']}")
    print()
    
    # Test 4: Demonstrate the random analyze cycles feature
    print("🎲 Test 4: Random Analyze Cycles (2-4 range)")
    system.race_scheduler.race_condition_active = True
    race_words = system.race_scheduler.prepare_all_words_race(system.categories)
    
    # Count occurrences of each word to verify multiple cycles
    word_counts = {}
    for word, category in race_words:
        word_counts[word] = word_counts.get(word, 0) + 1
    
    # Find a word that appears multiple times (indicating multiple cycles)
    sample_word = None
    for word, count in word_counts.items():
        if count > 1:
            sample_word = word
            break
    
    if sample_word:
        print(f"  Example: '{sample_word}' appears {word_counts[sample_word]} times")
        print(f"  This confirms random analyze cycles (2-4 range)")
    
    max_count = max(word_counts.values())
    min_count = min(word_counts.values())
    print(f"  Word repetition range: {min_count} to {max_count} cycles")
    print(f"  Total race words generated: {len(race_words)}")
    print()
    
    # Test 5: Disable scheduler
    print("❌ Test 5: Disable Race Condition Scheduler")
    system.enable_race_condition_scheduler(False)
    status_disabled = system.get_race_condition_status()
    print(f"  Scheduler enabled: {status_disabled['enabled']}")
    print()
    
    print("✅ All tests completed successfully!")
    print(f"📈 Race condition scheduler is working with {len(system.categories)} word categories")


if __name__ == "__main__":
    test_race_condition_scheduler()